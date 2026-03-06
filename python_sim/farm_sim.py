import argparse
import json
import math
import random
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

try:
    import pygame
except ImportError:
    print("pygame is not installed. Install it with: pip install pygame")
    sys.exit(1)


TILE_UNIT_AREA = 0.1  # Each farmland tile represents 0.1 sq units.
TILE_SIZE = 28
HUD_WIDTH = 320
FPS = 60


CROP_PROFILES = {
    "rice": {
        "optimal_min": 55,
        "optimal_max": 85,
        "dry_penalty": 0.75,
        "wet_penalty": 0.25,
        "label": "Rice",
    },
    "wheat": {
        "optimal_min": 40,
        "optimal_max": 70,
        "dry_penalty": 0.50,
        "wet_penalty": 0.45,
        "label": "Wheat",
    },
    "maize": {
        "optimal_min": 45,
        "optimal_max": 75,
        "dry_penalty": 0.60,
        "wet_penalty": 0.40,
        "label": "Maize",
    },
}


WEATHER_CONFIG = {
    "sunny": {"evap": 12.0, "rain_gain": 0.0, "color": (255, 220, 120)},
    "cloudy": {"evap": 6.0, "rain_gain": 0.0, "color": (180, 190, 205)},
    "rainy": {"evap": 2.0, "rain_gain": 8.0, "color": (125, 165, 230)},
}


@dataclass
class Tile:
    x: int
    y: int
    tile_type: str
    moisture: float = 50.0
    health: float = 75.0
    irrigation_on: bool = False


class FarmSimulation:
    def __init__(self, farmer_name: str, crop: str, land_area: float, location: str = "", weather_api_base: str = "http://localhost:3000"):
        self.farmer_name = farmer_name
        self.crop_key = crop.lower().strip() if crop else "rice"
        self.crop = CROP_PROFILES.get(self.crop_key, CROP_PROFILES["rice"])
        self.crop_name = self.crop["label"]
        self.land_area = max(0.1, float(land_area))
        self.location = location.strip()
        self.weather_api_base = weather_api_base.rstrip("/")

        self.farmland_tiles_target = max(1, round(self.land_area / TILE_UNIT_AREA))
        self.grid_w = max(8, math.ceil(math.sqrt(self.farmland_tiles_target)) + 2)
        self.grid_h = max(8, math.ceil(self.farmland_tiles_target / (self.grid_w - 2)) + 2)

        self.screen_w = self.grid_w * TILE_SIZE + HUD_WIDTH
        self.screen_h = self.grid_h * TILE_SIZE

        pygame.init()
        pygame.display.set_caption("Precision Farm Simulator (pygame)")
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)
        self.small_font = pygame.font.SysFont("consolas", 14)

        self.tiles = []
        self.farmland_positions = []
        self._build_map()

        self.player_x = 1
        self.player_y = 1
        self.weather = "sunny"
        self.weather_timer = 0.0
        self.weather_interval = 6.0
        self.weather_fetch_timer = 0.0
        self.weather_fetch_interval = 90.0
        self.weather_source = "simulation"
        self.weather_description = "simulated"
        self.running = True
        self.selected_tile = None

    def _build_map(self):
        self.tiles = [[Tile(x, y, "path") for x in range(self.grid_w)] for y in range(self.grid_h)]

        self.tiles[1][1].tile_type = "house"
        self.tiles[1][2].tile_type = "water"

        count = 0
        for y in range(1, self.grid_h - 1):
            for x in range(3, self.grid_w - 1):
                if count < self.farmland_tiles_target:
                    self.tiles[y][x] = Tile(x, y, "farmland", moisture=random.uniform(40, 70), health=75)
                    self.farmland_positions.append((x, y))
                    count += 1
                else:
                    self.tiles[y][x] = Tile(x, y, "path")

        for y in range(self.grid_h):
            for x in range(self.grid_w):
                if x == 0 or y == 0 or x == self.grid_w - 1 or y == self.grid_h - 1:
                    self.tiles[y][x] = Tile(x, y, "path")

    def _tile_color(self, tile: Tile):
        if tile.tile_type == "house":
            return (180, 120, 80)
        if tile.tile_type == "water":
            return (80, 150, 220)
        if tile.tile_type == "path":
            return (145, 120, 90)

        if tile.moisture < 30:
            return (155, 105, 65)
        if tile.moisture > 75:
            return (45, 80, 140)
        return (85, 145, 78)

    def _health_color(self, health: float):
        if health >= 70:
            return (80, 220, 100)
        if health >= 40:
            return (245, 210, 80)
        return (235, 100, 85)

    def _update_weather(self, dt: float):
        self.weather_fetch_timer += dt
        if self.location and self.weather_fetch_timer >= self.weather_fetch_interval:
            self.weather_fetch_timer = 0.0
            self._try_fetch_project_weather()

        self.weather_timer += dt
        if self.weather_timer >= self.weather_interval:
            self.weather_timer = 0.0
            # Keep real weather stable when sourced from backend; otherwise simulate.
            if self.weather_source != "project-api":
                self.weather = random.choice(list(WEATHER_CONFIG.keys()))

    def _map_project_weather_to_state(self, weather_obj: dict) -> str:
        icon = str(weather_obj.get("icon", "")).lower()
        desc = str(weather_obj.get("description", "")).lower()
        rainfall = float(weather_obj.get("rainfall", 0) or 0)
        cloudiness = float(weather_obj.get("cloudiness", 0) or 0)

        if rainfall > 0 or "rain" in icon or "rain" in desc or "drizzle" in desc or "storm" in desc:
            return "rainy"
        if cloudiness >= 55 or "cloud" in icon or "cloud" in desc or "mist" in desc or "haze" in desc:
            return "cloudy"
        return "sunny"

    def _try_fetch_project_weather(self):
        # Reuse project's backend weather endpoint so pygame reflects app weather data.
        url = f"{self.weather_api_base}/api/weather/{urllib.parse.quote(self.location)}"
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                payload = response.read().decode("utf-8")
            data = json.loads(payload)
            weather_obj = data.get("weather", {})
            if weather_obj:
                self.weather = self._map_project_weather_to_state(weather_obj)
                self.weather_source = "project-api"
                self.weather_description = str(weather_obj.get("description", "live"))
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
            self.weather_source = "simulation"
            self.weather_description = "simulated"

    def _update_tiles(self, dt: float):
        cfg = WEATHER_CONFIG[self.weather]
        for x, y in self.farmland_positions:
            tile = self.tiles[y][x]

            tile.moisture -= cfg["evap"] * dt
            tile.moisture += cfg["rain_gain"] * dt

            if tile.irrigation_on:
                tile.moisture += 15.0 * dt

            if tile.moisture < 35:
                tile.irrigation_on = True
            elif tile.moisture > 70:
                tile.irrigation_on = False

            tile.moisture = max(0.0, min(100.0, tile.moisture))

            if tile.moisture < self.crop["optimal_min"]:
                tile.health -= self.crop["dry_penalty"] * dt * 10
            elif tile.moisture > self.crop["optimal_max"]:
                tile.health -= self.crop["wet_penalty"] * dt * 10
            else:
                tile.health += 0.45 * dt * 10

            tile.health = max(0.0, min(100.0, tile.health))

    def _move_player(self, keys):
        nx, ny = self.player_x, self.player_y
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            ny -= 1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            ny += 1
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            nx -= 1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            nx += 1

        if 0 <= nx < self.grid_w and 0 <= ny < self.grid_h:
            if self.tiles[ny][nx].tile_type != "path" or (nx, ny) == (1, 1):
                self.player_x, self.player_y = nx, ny

    def _nearest_farm_tile(self):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            tx, ty = self.player_x + dx, self.player_y + dy
            if 0 <= tx < self.grid_w and 0 <= ty < self.grid_h:
                tile = self.tiles[ty][tx]
                if tile.tile_type == "farmland":
                    return tile
        return None

    def _draw_world(self):
        self.screen.fill((22, 28, 34))
        world_rect = pygame.Rect(0, 0, self.grid_w * TILE_SIZE, self.grid_h * TILE_SIZE)
        pygame.draw.rect(self.screen, (40, 65, 40), world_rect)

        for y in range(self.grid_h):
            for x in range(self.grid_w):
                tile = self.tiles[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
                pygame.draw.rect(self.screen, self._tile_color(tile), rect)

                if tile.tile_type == "farmland":
                    hc = self._health_color(tile.health)
                    cx = x * TILE_SIZE + TILE_SIZE // 2
                    cy = y * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(self.screen, hc, (cx, cy), 4)

                    if tile.irrigation_on:
                        pygame.draw.circle(self.screen, (70, 190, 255), (cx + 8, cy - 8), 3)

        px = self.player_x * TILE_SIZE + TILE_SIZE // 2
        py = self.player_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.rect(self.screen, (245, 235, 180), pygame.Rect(px - 6, py - 6, 12, 12))
        pygame.draw.rect(self.screen, (130, 90, 65), pygame.Rect(px - 5, py + 2, 10, 4))

    def _draw_hud(self):
        x0 = self.grid_w * TILE_SIZE
        hud = pygame.Rect(x0, 0, HUD_WIDTH, self.screen_h)
        pygame.draw.rect(self.screen, (28, 33, 44), hud)

        lines = [
            f"Farmer: {self.farmer_name}",
            f"Crop: {self.crop_name}",
            f"Location: {self.location or 'N/A'}",
            f"Land Area: {self.land_area:.2f}",
            f"Tile Unit: {TILE_UNIT_AREA:.1f}",
            f"Farm Tiles: {self.farmland_tiles_target}",
            f"Weather: {self.weather}",
            f"Weather Src: {self.weather_source}",
        ]

        avg_m = self._avg_moisture()
        need_i = self._farms_needing_irrigation()
        lines += [
            f"Avg Moisture: {avg_m:.1f}%",
            f"Need Irrigation: {need_i}",
            f"Desc: {self.weather_description[:28]}",
            "",
            "Controls:",
            "WASD / Arrows -> move",
            "E -> inspect nearby tile",
            "Q -> clear inspection",
            "ESC -> quit",
        ]

        yy = 16
        for i, txt in enumerate(lines):
            font = self.font if i < 8 else self.small_font
            color = (225, 235, 245) if i != 5 else WEATHER_CONFIG[self.weather]["color"]
            surf = font.render(txt, True, color)
            self.screen.blit(surf, (x0 + 14, yy))
            yy += 24 if i < 8 else 20

        if self.selected_tile is not None:
            yb = self.screen_h - 180
            box = pygame.Rect(x0 + 12, yb, HUD_WIDTH - 24, 160)
            pygame.draw.rect(self.screen, (42, 52, 68), box, border_radius=8)
            pygame.draw.rect(self.screen, (110, 185, 120), box, width=2, border_radius=8)

            t = self.selected_tile
            data = [
                "Selected Farm Tile",
                f"Pos: ({t.x}, {t.y})",
                f"Moisture: {t.moisture:.1f}%",
                f"Health: {t.health:.1f}%",
                f"Irrigation: {'ON' if t.irrigation_on else 'OFF'}",
            ]
            yy = yb + 12
            for idx, txt in enumerate(data):
                surf = self.small_font.render(txt, True, (236, 244, 252) if idx == 0 else (212, 228, 240))
                self.screen.blit(surf, (x0 + 20, yy))
                yy += 26

    def _avg_moisture(self):
        vals = [self.tiles[y][x].moisture for x, y in self.farmland_positions]
        return sum(vals) / len(vals) if vals else 0.0

    def _farms_needing_irrigation(self):
        return sum(1 for x, y in self.farmland_positions if self.tiles[y][x].moisture < 35.0)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_e:
                        self.selected_tile = self._nearest_farm_tile()
                    elif event.key == pygame.K_q:
                        self.selected_tile = None

            keys = pygame.key.get_pressed()
            self._move_player(keys)
            self._update_weather(dt)
            self._update_tiles(dt)

            self._draw_world()
            self._draw_hud()
            pygame.display.flip()

        pygame.quit()


def parse_user_data(users_file: Path, username: str):
    with users_file.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if username not in data:
        raise ValueError(f"User '{username}' not found in {users_file}")

    user = data[username]
    land_area = float(user.get("farmSize", 1.0))
    crop = str(user.get("crop", "Rice"))
    name = str(user.get("name", username))
    location = str(user.get("location", "")).strip()
    return name, crop, land_area, location


def main():
    parser = argparse.ArgumentParser(description="Precision Farm Simulator (pygame)")
    parser.add_argument("--username", type=str, default="", help="Username key from users.json")
    parser.add_argument("--users-file", type=str, default="data/users.json", help="Path to users.json")
    parser.add_argument("--farm-size", type=float, default=None, help="Land area override")
    parser.add_argument("--crop", type=str, default=None, help="Crop override")
    parser.add_argument("--name", type=str, default="Farmer", help="Farmer display name override")
    parser.add_argument("--location", type=str, default="", help="Location override")
    parser.add_argument("--weather-api-base", type=str, default="http://localhost:3000", help="Project backend base URL")
    args = parser.parse_args()

    name = args.name
    crop = args.crop or "Rice"
    land_area = args.farm_size if args.farm_size is not None else 1.0
    location = args.location

    if args.username:
        users_path = Path(args.users_file)
        if not users_path.is_absolute():
            users_path = Path.cwd() / users_path
        name, crop, land_area, location = parse_user_data(users_path, args.username)

        if args.farm_size is not None:
            land_area = args.farm_size
        if args.crop:
            crop = args.crop
        if args.name and args.name != "Farmer":
            name = args.name
        if args.location:
            location = args.location

    sim = FarmSimulation(name, crop, land_area, location=location, weather_api_base=args.weather_api_base)
    # Initial weather sync from project backend before the first frame.
    if location:
        sim._try_fetch_project_weather()
    sim.run()


if __name__ == "__main__":
    main()
