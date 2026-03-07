"""
Enhanced graphics module for farm_sim.py
Provides improved rendering with:
- Animated crop tiles with health/moisture visualization
- Weather particle effects (rain, sun rays)
- Enhanced HUD with stat bars and panels
- Better color schemes and animations
"""

import pygame
import math
import random
from typing import List, Tuple, Optional


class ParticleEffect:
    """Single particle for weather effects."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, lifetime: float, color: Tuple[int, int, int], size: int = 2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
    
    def update(self, dt: float) -> bool:
        """Update particle. Returns True if still alive."""
        self.lifetime -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        return self.lifetime > 0
    
    def draw(self, surface: pygame.Surface):
        """Draw particle with fade effect."""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        fade_color = tuple(int(c * alpha / 255) for c in self.color)
        pygame.draw.circle(surface, fade_color, (int(self.x), int(self.y)), self.size)


class WeatherEffectSystem:
    """Manages weather particle effects."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.particles: List[ParticleEffect] = []
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def spawn_rain(self, count: int = 5):
        """Spawn rain particles."""
        for _ in range(count):
            x = random.randint(0, self.screen_width)
            y = random.randint(-50, 0)
            vx = random.uniform(-2, 2)
            vy = random.uniform(150, 250)
            self.particles.append(ParticleEffect(x, y, vx, vy, 3.0, (100, 150, 200), size=1))
    
    def spawn_sun_rays(self, origin_x: float, origin_y: float, count: int = 3):
        """Spawn sun ray particles."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 80)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(ParticleEffect(origin_x, origin_y, vx, vy, 2.0, (255, 220, 100), size=2))
    
    def update(self, dt: float):
        """Update all particles, removing dead ones."""
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, surface: pygame.Surface):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface)


class TileRenderer:
    """Enhanced tile rendering with animations and visualizations."""
    
    # Color schemes for different tile states
    COLORS = {
        "house": (180, 120, 80),
        "water": (80, 150, 220),
        "path": (145, 120, 90),
        "farmland_dry": (155, 105, 65),
        "farmland_wet": (45, 80, 140),
        "farmland_healthy": (85, 145, 78),
    }
    
    CROP_SYMBOLS = {
        "rice": "🌾",
        "wheat": "🌾",
        "maize": "🌽",
        "tomato": "🍅",
        "cotton": "◎",
        "potato": "◉",
        "onion": "○",
        "sugarcane": "↻",
    }
    
    def __init__(self, tile_size: int):
        self.tile_size = tile_size
        self.animation_time = 0.0
    
    def update(self, dt: float):
        """Update animation state."""
        self.animation_time += dt
    
    def get_farmland_color(self, moisture: float, health: float) -> Tuple[int, int, int]:
        """Get color based on moisture and health."""
        if moisture < 30:
            # Dry soil - brown
            return self._lerp_color((155, 105, 65), (120, 80, 40), min(1, 30 / max(moisture, 1)))
        elif moisture > 75:
            # Wet soil - blue
            blue_intensity = (moisture - 75) / 25
            return self._lerp_color((85, 145, 78), (45, 80, 140), blue_intensity)
        else:
            # Healthy - green
            return (85, 145, 78)
    
    @staticmethod
    def _lerp_color(c1: Tuple[int, int, int], c2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """Linear interpolation between colors."""
        t = max(0, min(1, t))
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )
    
    def draw_tile(self, surface: pygame.Surface, x: int, y: int, tile_x: int, tile_y: int, 
                  tile_type: str, moisture: float = 50, health: float = 75, irrigation_on: bool = False):
        """Draw an enhanced tile."""
        rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        
        # Draw main tile color
        if tile_type == "farmland":
            color = self.get_farmland_color(moisture, health)
        else:
            color = self.COLORS.get(tile_type, (100, 100, 100))
        
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (60, 60, 60), rect, width=1)
        
        # Draw moisture bar indicator for farmland
        if tile_type == "farmland":
            bar_height = 3
            bar_rect = pygame.Rect(x, y + self.tile_size - bar_height, self.tile_size, bar_height)
            pygame.draw.rect(surface, (40, 40, 40), bar_rect)
            
            moisture_width = int(self.tile_size * (moisture / 100))
            pygame.draw.rect(surface, (100, 180, 255), (x, y + self.tile_size - bar_height, moisture_width, bar_height))
            
            # Irrigation indicator
            if irrigation_on:
                pulse = math.sin(self.animation_time * 4) * 0.5 + 0.5
                indent = 1 + int(pulse * 2)
                indicator_rect = pygame.Rect(
                    x + indent, y + indent,
                    self.tile_size - indent * 2, self.tile_size - indent * 2
                )
                pygame.draw.rect(surface, (100, 255, 100), indicator_rect, width=2)


class HUDPanel:
    """Enhanced HUD panel with better layout and visualization."""
    
    def __init__(self, x: int, y: int, width: int, height: int, font_large: pygame.font.Font, font_small: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font_large = font_large
        self.font_small = font_small
        self.bg_color = (28, 33, 44)
        self.border_color = (60, 120, 180)
    
    def draw_background(self, surface: pygame.Surface):
        """Draw panel background with border."""
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, width=3)
    
    def draw_stat_bar(self, surface: pygame.Surface, x: int, y: int, width: int, height: int,
                      label: str, value: float, max_value: float = 100, color: Tuple[int, int, int] = (100, 200, 100)):
        """Draw a stat bar with label and value."""
        # Label
        label_surf = self.font_small.render(f"{label}:", True, (200, 200, 200))
        surface.blit(label_surf, (x, y))
        
        # Background bar
        bar_rect = pygame.Rect(x + 80, y, width - 80, height)
        pygame.draw.rect(surface, (40, 40, 40), bar_rect)
        pygame.draw.rect(surface, (100, 100, 100), bar_rect, width=1)
        
        # Value bar
        bar_width = int((bar_rect.width - 4) * (value / max_value))
        value_rect = pygame.Rect(x + 82, y + 2, bar_width, height - 4)
        pygame.draw.rect(surface, color, value_rect)
        
        # Value text
        value_text = f"{value:.0f}%"
        value_surf = self.font_small.render(value_text, True, (255, 255, 255))
        surface.blit(value_surf, (x + width - 40, y))
    
    def draw_section_title(self, surface: pygame.Surface, x: int, y: int, title: str):
        """Draw a section title."""
        title_surf = self.font_large.render(title, True, (100, 200, 255))
        surface.blit(title_surf, (x, y))
        
        # Underline
        pygame.draw.line(surface, (100, 200, 255), (x, y + 24), (x + len(title) * 12, y + 24), width=2)


class EnhancedGraphicsEngine:
    """Main graphics engine that integrates all enhanced rendering."""
    
    def __init__(self, screen: pygame.Surface, grid_w: int, grid_h: int, tile_size: int, hud_width: int):
        self.screen = screen
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.tile_size = tile_size
        self.hud_width = hud_width
        
        self.tile_renderer = TileRenderer(tile_size)
        self.weather_effects = WeatherEffectSystem(
            grid_w * tile_size,
            grid_h * tile_size
        )
        
        self.font_large = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 16)
        self.font_small = pygame.font.SysFont("consolas", 13)
        
        x0 = grid_w * tile_size
        self.hud_panel = HUDPanel(x0, 0, hud_width, grid_h * tile_size, self.font_large, self.font_small)
    
    def update(self, dt: float):
        """Update all graphics systems."""
        self.tile_renderer.update(dt)
        self.weather_effects.update(dt)
    
    def draw_farmland(self, surface: pygame.Surface, tiles: list, farmland_positions: list):
        """Draw all farmland tiles with enhanced rendering."""
        for x, y in farmland_positions:
            tile = tiles[y][x]
            screen_x = x * self.tile_size
            screen_y = y * self.tile_size
            
            self.tile_renderer.draw_tile(
                surface, screen_x, screen_y, x, y,
                "farmland", tile.moisture, tile.health, tile.irrigation_on
            )
    
    def draw_other_tiles(self, surface: pygame.Surface, tiles: list):
        """Draw non-farmland tiles."""
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                tile = tiles[y][x]
                if tile.tile_type in ("house", "water", "path"):
                    screen_x = x * self.tile_size
                    screen_y = y * self.tile_size
                    
                    self.tile_renderer.draw_tile(
                        surface, screen_x, screen_y, x, y, tile.tile_type
                    )
    
    def draw_weather_effects(self, surface: pygame.Surface, weather: str):
        """Draw weather particle effects."""
        if weather == "rainy":
            self.weather_effects.spawn_rain(2)
        elif weather == "sunny":
            self.weather_effects.spawn_sun_rays(50, 30, 1)
        
        self.weather_effects.draw(surface)
    
    def draw_enhanced_hud(self, surface: pygame.Surface, game_state: dict):
        """Draw enhanced HUD with stat panels."""
        self.hud_panel.draw_background(surface)
        
        x0 = self.grid_w * self.tile_size
        x = x0 + 12
        y = 12
        
        # Farm Info Section
        self.hud_panel.draw_section_title(surface, x, y, "FARM INFO")
        y += 28
        
        info_lines = [
            f"Farmer: {game_state.get('farmer_name', 'N/A')}",
            f"Crop: {game_state.get('crop_name', 'N/A')}",
            f"Area: {game_state.get('land_area', 0):.1f} units",
            f"Location: {game_state.get('location', 'N/A')}",
        ]
        
        for line in info_lines:
            text_surf = self.font_small.render(line, True, (200, 220, 240))
            surface.blit(text_surf, (x, y))
            y += 18
        
        y += 8
        
        # Stats Section
        self.hud_panel.draw_section_title(surface, x, y, "FARM STATS")
        y += 28
        
        self.hud_panel.draw_stat_bar(surface, x, y, self.hud_width - 24, 14,
                                     "Avg Moisture", game_state.get('avg_moisture', 50),
                                     color=(100, 180, 255))
        y += 20
        
        self.hud_panel.draw_stat_bar(surface, x, y, self.hud_width - 24, 14,
                                     "Avg Health", game_state.get('avg_health', 75),
                                     color=(100, 255, 100))
        y += 20
        
        # Weather Section
        y += 8
        self.hud_panel.draw_section_title(surface, x, y, "WEATHER")
        y += 28
        
        weather_lines = [
            f"Condition: {game_state.get('weather', 'N/A').upper()}",
            f"Temp: {game_state.get('current_temp', 25)}°C",
            f"Humidity: {game_state.get('current_humidity', 50)}%",
            f"Rainfall: {game_state.get('current_rainfall', 0):.1f}mm",
            f"Source: {game_state.get('weather_source', 'simulation')}",
        ]
        
        for line in weather_lines:
            text_surf = self.font_small.render(line, True, (200, 220, 240))
            surface.blit(text_surf, (x, y))
            y += 16
        
        # AI Decision Section
        y += 8
        if game_state.get('ai_decision_message'):
            self.hud_panel.draw_section_title(surface, x, y, "AI SYSTEM")
            y += 28
            
            # Wrap AI message
            ai_msg = game_state.get('ai_decision_message', '')
            words = ai_msg.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 < 35:
                    current_line += word + " "
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word + " "
            if current_line:
                lines.append(current_line)
            
            for line in lines[:3]:
                text_surf = self.font_small.render(line.strip(), True, (100, 220, 100))
                surface.blit(text_surf, (x, y))
                y += 16
        
        # Controls Section
        y += 16
        self.hud_panel.draw_section_title(surface, x, y, "CONTROLS")
        y += 28
        
        controls = [
            "WASD/Arrows - Move",
            "E - Inspect Tile",
            "Q - Clear Selection",
            "ESC - Quit",
        ]
        
        for ctrl in controls:
            text_surf = self.font_small.render(ctrl, True, (150, 200, 220))
            surface.blit(text_surf, (x, y))
            y += 16
    
    def draw_selected_tile_info(self, surface: pygame.Surface, tile, x: int, y: int, width: int):
        """Draw selected tile information panel."""
        if tile is None:
            return
        
        panel_height = 140
        box = pygame.Rect(x, y - panel_height - 20, width, panel_height)
        pygame.draw.rect(surface, (42, 52, 68), box, border_radius=8)
        pygame.draw.rect(surface, (110, 185, 120), box, width=2, border_radius=8)
        
        py = y - panel_height - 10
        
        title_surf = self.font_medium.render("TILE INFO", True, (150, 255, 180))
        surface.blit(title_surf, (x + 12, py))
        
        py += 28
        
        info = [
            f"Position: ({tile.x}, {tile.y})",
            f"Type: {tile.tile_type}",
            f"Moisture: {tile.moisture:.1f}%",
            f"Health: {tile.health:.1f}%",
            f"Irrigation: {'ON' if tile.irrigation_on else 'OFF'}",
        ]
        
        for line in info:
            text_surf = self.font_small.render(line, True, (220, 240, 250))
            surface.blit(text_surf, (x + 20, py))
            py += 18
