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

# Ensure we can import modules from this directory
sys.path.insert(0, str(Path(__file__).parent))

try:
    import pygame
except ImportError:
    print("pygame is not installed. Install it with: pip install pygame")
    sys.exit(1)

from ml_irrigation_predictor import load_predictor
from graphics_enhanced import EnhancedGraphicsEngine


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
    "sunny": {
        "evap": 12.0,
        "rain_gain": 0.0,
        "color": (255, 220, 120),
        "temp": 32,
        "humidity": 35,
        "rainfall": 0.0,
    },
    "cloudy": {
        "evap": 6.0,
        "rain_gain": 0.0,
        "color": (180, 190, 205),
        "temp": 22,
        "humidity": 55,
        "rainfall": 0.0,
    },
    "rainy": {
        "evap": 2.0,
        "rain_gain": 8.0,
        "color": (125, 165, 230),
        "temp": 18,
        "humidity": 85,
        "rainfall": 5.0,
    },
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
        
        # Initialize current weather conditions from config
        cfg = WEATHER_CONFIG[self.weather]
        self.current_temp = cfg.get("temp", 25)
        self.current_humidity = cfg.get("humidity", 50)
        self.current_rainfall = cfg.get("rainfall", 0.0)
        
        # Initialize ML irrigation predictor
        try:
            self.ml_predictor = load_predictor()
            self.use_ml_irrigation = True
        except Exception as e:
            print(f"Warning: Could not load ML predictor: {e}")
            print("Falling back to simple irrigation logic")
            self.ml_predictor = None
            self.use_ml_irrigation = False
        
        # AI decision tracking for HUD display
        self.ai_decision_message = ""
        self.ai_decision_timer = 0.0
        
        # Initialize enhanced graphics engine
        self.graphics = EnhancedGraphicsEngine(
            self.screen, self.grid_w, self.grid_h, TILE_SIZE, HUD_WIDTH
        )

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
        
        # Update current weather conditions from config
        cfg = WEATHER_CONFIG[self.weather]
        self.current_temp = cfg.get("temp", 25)
        self.current_humidity = cfg.get("humidity", 50)
        self.current_rainfall = cfg.get("rainfall", 0.0)

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

            # Use ML-based irrigation if available
            if self.use_ml_irrigation and self.ml_predictor is not None:
                try:
                    decision, amount, reasoning = self.ml_predictor.predict(
                        crop=self.crop_key,
                        farm_area=self.land_area,
                        temperature=self.current_temp,
                        humidity=self.current_humidity,
                        rainfall=self.current_rainfall,
                        soil_moisture=tile.moisture,
                        location=self.location or "General",
                    )
                    
                    # Apply ML-based irrigation
                    if decision == 1 and amount > 0:
                        liters_per_tile = amount / len(self.farmland_positions)
                        tile.moisture += (liters_per_tile / 100) * dt
                        # Store message for HUD display
                        self.ai_decision_message = reasoning
                        self.ai_decision_timer = 4.0
                except Exception as e:
                    # Fallback to simple logic if ML prediction fails
                    if tile.irrigation_on:
                        tile.moisture += 15.0 * dt
            else:
                # Simple fallback irrigation logic
                if tile.irrigation_on:
                    tile.moisture += 15.0 * dt

            # Simple threshold-based irrigation trigger (used when ML not available)
            if not self.use_ml_irrigation or self.ml_predictor is None:
                if tile.moisture < 35:
                    tile.irrigation_on = True
                elif tile.moisture > 70:
                    tile.irrigation_on = False

            tile.moisture = max(0.0, min(100.0, tile.moisture))

            # Frame-rate independent health model tuned for stable crop health.
            if tile.moisture < self.crop["optimal_min"]:
                deficit = min(1.0, (self.crop["optimal_min"] - tile.moisture) / 25.0)
                tile.health -= self.crop["dry_penalty"] * dt * 2.5 * deficit
            elif tile.moisture > self.crop["optimal_max"]:
                excess = min(1.0, (tile.moisture - self.crop["optimal_max"]) / 25.0)
                tile.health -= self.crop["wet_penalty"] * dt * 2.0 * excess
            else:
                tile.health += 0.9 * dt

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
        """Draw world using enhanced graphics engine."""
        self.screen.fill((22, 28, 34))
        world_rect = pygame.Rect(0, 0, self.grid_w * TILE_SIZE, self.grid_h * TILE_SIZE)
        pygame.draw.rect(self.screen, (40, 65, 40), world_rect)

        # Draw all non-farmland tiles
        self.graphics.draw_other_tiles(self.screen, self.tiles)
        
        # Draw farmland tiles with enhanced rendering
        self.graphics.draw_farmland(self.screen, self.tiles, self.farmland_positions)
        
        # Draw weather effects
        self.graphics.draw_weather_effects(self.screen, self.weather)

        # Draw player character
        px = self.player_x * TILE_SIZE + TILE_SIZE // 2
        py = self.player_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.rect(self.screen, (245, 235, 180), pygame.Rect(px - 6, py - 6, 12, 12))
        pygame.draw.rect(self.screen, (130, 90, 65), pygame.Rect(px - 5, py + 2, 10, 4))

    def _draw_hud(self):
        """Draw HUD using enhanced graphics engine."""
        self.graphics.update(0.016)  # Update animations
        
        # Prepare game state dict for graphics engine
        avg_m = self._avg_moisture()
        avg_h = self._avg_health()
        
        game_state = {
            "farmer_name": self.farmer_name,
            "crop_name": self.crop_name,
            "land_area": self.land_area,
            "location": self.location or "N/A",
            "weather": self.weather,
            "current_temp": self.current_temp,
            "current_humidity": self.current_humidity,
            "current_rainfall": self.current_rainfall,
            "weather_source": self.weather_source,
            "avg_moisture": avg_m,
            "avg_health": avg_h,
            "ai_decision_message": self.ai_decision_message if self.ai_decision_timer > 0 else "",
        }
        
        self.graphics.draw_enhanced_hud(self.screen, game_state)
        
        # Draw selected tile info if any
        x0 = self.grid_w * TILE_SIZE
        if self.selected_tile is not None:
            self.graphics.draw_selected_tile_info(
                self.screen, self.selected_tile,
                x0 + HUD_WIDTH - 150,
                self.screen_h - 20,
                140
            )
        
        # Update AI message timer
        if self.ai_decision_timer > 0:
            self.ai_decision_timer -= 0.016

    def _avg_moisture(self):
        vals = [self.tiles[y][x].moisture for x, y in self.farmland_positions]
        return sum(vals) / len(vals) if vals else 0.0
    
    def _avg_health(self):
        vals = [self.tiles[y][x].health for x, y in self.farmland_positions]
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
