"""
Complex Snake Game with Advanced Features
==========================================
Features:
- Multiple difficulty levels
- Special food types with different effects
- Power-ups and obstacles
- Lives system
- Score tracking with high scores
- Smooth animations and visual effects
- Pause/resume functionality
"""

import pygame
import random
import json
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 128, 0)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    INSTRUCTIONS = 5

# Difficulty Levels
class Difficulty(Enum):
    EASY = {"speed": 8, "obstacles": 0, "name": "Easy"}
    MEDIUM = {"speed": 12, "obstacles": 5, "name": "Medium"}
    HARD = {"speed": 16, "obstacles": 10, "name": "Hard"}

# Food Types
class FoodType(Enum):
    NORMAL = {"color": GREEN, "points": 10, "growth": 1}
    GOLDEN = {"color": GOLD, "points": 50, "growth": 1}
    SPEED_BOOST = {"color": CYAN, "points": 20, "growth": 0}
    SLOW_DOWN = {"color": PURPLE, "points": 15, "growth": 0}

# Power-up Types
class PowerUpType(Enum):
    INVINCIBILITY = {"color": ORANGE, "duration": 5000, "name": "Invincibility"}
    SCORE_MULTIPLIER = {"color": YELLOW, "duration": 10000, "name": "2x Score"}

@dataclass
class Position:
    x: int
    y: int
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class Particle:
    """Visual particle effect"""
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 30
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(1, self.size - 0.1)
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / 30))
            color = tuple(min(255, c + alpha // 2) for c in self.color)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class Snake:
    """Snake class with movement and collision detection"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [
            Position(start_x, start_y),
            Position(start_x - 1, start_y),
            Position(start_x - 2, start_y)
        ]
        self.direction = Position(1, 0)
        self.next_direction = Position(1, 0)
        self.growing = False
    
    def change_direction(self, new_direction: Position):
        # Prevent 180-degree turns
        if (new_direction.x != -self.direction.x or 
            new_direction.y != -self.direction.y):
            self.next_direction = new_direction
    
    def move(self):
        self.direction = self.next_direction
        head = self.body[0]
        new_head = Position(
            (head.x + self.direction.x) % GRID_WIDTH,
            (head.y + self.direction.y) % GRID_HEIGHT
        )
        
        self.body.insert(0, new_head)
        
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
    
    def grow(self):
        self.growing = True
    
    def check_self_collision(self) -> bool:
        head = self.body[0]
        return head in self.body[1:]
    
    def check_obstacle_collision(self, obstacles: List[Position]) -> bool:
        head = self.body[0]
        return head in obstacles
    
    def draw(self, screen):
        # Draw snake with gradient effect
        for i, segment in enumerate(self.body):
            # Calculate color gradient from head to tail
            ratio = i / len(self.body)
            color = (
                int(0 + (100 * ratio)),
                int(255 - (100 * ratio)),
                int(0 + (50 * ratio))
            )
            
            rect = pygame.Rect(
                segment.x * GRID_SIZE,
                segment.y * GRID_SIZE,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )
            pygame.draw.rect(screen, color, rect, border_radius=5)
            
            # Draw eyes on head
            if i == 0:
                eye_size = 3
                eye_offset = GRID_SIZE // 4
                left_eye = (segment.x * GRID_SIZE + eye_offset, 
                           segment.y * GRID_SIZE + eye_offset)
                right_eye = (segment.x * GRID_SIZE + GRID_SIZE - eye_offset, 
                            segment.y * GRID_SIZE + eye_offset)
                pygame.draw.circle(screen, WHITE, left_eye, eye_size)
                pygame.draw.circle(screen, WHITE, right_eye, eye_size)

class Food:
    """Food class with different types"""
    def __init__(self, food_type: FoodType, obstacles: List[Position], snake_body: List[Position]):
        self.type = food_type
        self.position = self.generate_position(obstacles, snake_body)
    
    def generate_position(self, obstacles: List[Position], snake_body: List[Position]) -> Position:
        while True:
            pos = Position(
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if pos not in obstacles and pos not in snake_body:
                return pos
    
    def draw(self, screen):
        color = self.type.value["color"]
        center = (
            self.position.x * GRID_SIZE + GRID_SIZE // 2,
            self.position.y * GRID_SIZE + GRID_SIZE // 2
        )
        pygame.draw.circle(screen, color, center, GRID_SIZE // 2 - 2)
        
        # Add shine effect
        shine_pos = (center[0] - 3, center[1] - 3)
        pygame.draw.circle(screen, WHITE, shine_pos, 3)

class PowerUp:
    """Power-up class"""
    def __init__(self, power_type: PowerUpType, obstacles: List[Position], snake_body: List[Position]):
        self.type = power_type
        self.position = self.generate_position(obstacles, snake_body)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000  # 8 seconds
    
    def generate_position(self, obstacles: List[Position], snake_body: List[Position]) -> Position:
        while True:
            pos = Position(
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if pos not in obstacles and pos not in snake_body:
                return pos
    
    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def draw(self, screen):
        color = self.type.value["color"]
        rect = pygame.Rect(
            self.position.x * GRID_SIZE + 2,
            self.position.y * GRID_SIZE + 2,
            GRID_SIZE - 4,
            GRID_SIZE - 4
        )
        pygame.draw.rect(screen, color, rect, border_radius=3)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=3)

class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Complex Snake Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
        
        self.state = GameState.MENU
        self.difficulty = Difficulty.MEDIUM
        self.high_score = self.load_high_score()
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = Snake()
        self.score = 0
        self.lives = 3
        self.level = 1
        self.obstacles = self.generate_obstacles()
        self.food = Food(FoodType.NORMAL, self.obstacles, self.snake.body)
        self.power_up: Optional[PowerUp] = None
        self.particles: List[Particle] = []
        
        # Active effects
        self.invincible = False
        self.invincible_end = 0
        self.score_multiplier = 1
        self.multiplier_end = 0
        self.speed_boost_end = 0
        self.slow_down_end = 0
        
        self.last_move_time = 0
        self.move_delay = 1000 // self.difficulty.value["speed"]
    
    def generate_obstacles(self) -> List[Position]:
        obstacles = []
        num_obstacles = self.difficulty.value["obstacles"]
        
        for _ in range(num_obstacles):
            while True:
                pos = Position(
                    random.randint(0, GRID_WIDTH - 1),
                    random.randint(0, GRID_HEIGHT - 1)
                )
                # Avoid center area where snake starts
                if (abs(pos.x - GRID_WIDTH // 2) > 5 or 
                    abs(pos.y - GRID_HEIGHT // 2) > 5):
                    if pos not in obstacles:
                        obstacles.append(pos)
                        break
        
        return obstacles
    
    def load_high_score(self) -> int:
        try:
            if os.path.exists("snake_highscore.json"):
                with open("snake_highscore.json", "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except:
            pass
        return 0
    
    def save_high_score(self):
        try:
            with open("snake_highscore.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    self.handle_menu_input(event.key)
                elif self.state == GameState.PLAYING:
                    self.handle_game_input(event.key)
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.INSTRUCTIONS:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
        
        return True
    
    def handle_menu_input(self, key):
        if key == pygame.K_1:
            self.difficulty = Difficulty.EASY
            self.reset_game()
            self.state = GameState.PLAYING
        elif key == pygame.K_2:
            self.difficulty = Difficulty.MEDIUM
            self.reset_game()
            self.state = GameState.PLAYING
        elif key == pygame.K_3:
            self.difficulty = Difficulty.HARD
            self.reset_game()
            self.state = GameState.PLAYING
        elif key == pygame.K_i:
            self.state = GameState.INSTRUCTIONS
        elif key == pygame.K_ESCAPE:
            return False
    
    def handle_game_input(self, key):
        if key == pygame.K_UP or key == pygame.K_w:
            self.snake.change_direction(Position(0, -1))
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.snake.change_direction(Position(0, 1))
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.snake.change_direction(Position(-1, 0))
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.snake.change_direction(Position(1, 0))
        elif key == pygame.K_p or key == pygame.K_ESCAPE:
            self.state = GameState.PAUSED
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Update active effects
        if self.invincible and current_time > self.invincible_end:
            self.invincible = False
        
        if self.score_multiplier > 1 and current_time > self.multiplier_end:
            self.score_multiplier = 1
        
        # Calculate current speed
        current_delay = self.move_delay
        if current_time < self.speed_boost_end:
            current_delay = self.move_delay // 2
        elif current_time < self.slow_down_end:
            current_delay = self.move_delay * 2
        
        # Move snake
        if current_time - self.last_move_time > current_delay:
            self.last_move_time = current_time
            self.snake.move()
            
            # Check collisions
            head = self.snake.body[0]
            
            # Check food collision
            if head == self.food.position:
                self.eat_food()
            
            # Check power-up collision
            if self.power_up and head == self.power_up.position:
                self.collect_power_up()
            
            # Check self collision
            if self.snake.check_self_collision():
                self.lose_life()
            
            # Check obstacle collision
            if not self.invincible and self.snake.check_obstacle_collision(self.obstacles):
                self.lose_life()
        
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
        # Spawn power-ups randomly
        if self.power_up is None and random.random() < 0.002:
            power_type = random.choice(list(PowerUpType))
            self.power_up = PowerUp(power_type, self.obstacles, self.snake.body)
        
        # Remove expired power-ups
        if self.power_up and self.power_up.is_expired():
            self.power_up = None
    
    def eat_food(self):
        food_data = self.food.type.value
        
        # Add score
        points = food_data["points"] * self.score_multiplier
        self.score += points
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        # Grow snake
        for _ in range(food_data["growth"]):
            self.snake.grow()
        
        # Apply special effects
        current_time = pygame.time.get_ticks()
        if self.food.type == FoodType.SPEED_BOOST:
            self.speed_boost_end = current_time + 5000
        elif self.food.type == FoodType.SLOW_DOWN:
            self.slow_down_end = current_time + 5000
        
        # Create particles
        for _ in range(10):
            particle = Particle(
                self.food.position.x * GRID_SIZE + GRID_SIZE // 2,
                self.food.position.y * GRID_SIZE + GRID_SIZE // 2,
                food_data["color"]
            )
            self.particles.append(particle)
        
        # Generate new food (with chance for special food)
        rand = random.random()
        if rand < 0.1:
            food_type = FoodType.GOLDEN
        elif rand < 0.2:
            food_type = FoodType.SPEED_BOOST
        elif rand < 0.3:
            food_type = FoodType.SLOW_DOWN
        else:
            food_type = FoodType.NORMAL
        
        self.food = Food(food_type, self.obstacles, self.snake.body)
        
        # Level up every 200 points
        new_level = (self.score // 200) + 1
        if new_level > self.level:
            self.level = new_level
            self.move_delay = max(50, self.move_delay - 10)
    
    def collect_power_up(self):
        if not self.power_up:
            return
        
        current_time = pygame.time.get_ticks()
        power_data = self.power_up.type.value
        
        if self.power_up.type == PowerUpType.INVINCIBILITY:
            self.invincible = True
            self.invincible_end = current_time + power_data["duration"]
        elif self.power_up.type == PowerUpType.SCORE_MULTIPLIER:
            self.score_multiplier = 2
            self.multiplier_end = current_time + power_data["duration"]
        
        # Create particles
        for _ in range(15):
            particle = Particle(
                self.power_up.position.x * GRID_SIZE + GRID_SIZE // 2,
                self.power_up.position.y * GRID_SIZE + GRID_SIZE // 2,
                power_data["color"]
            )
            self.particles.append(particle)
        
        self.power_up = None
    
    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
        else:
            # Reset snake position but keep score
            self.snake.reset()
            self.invincible = True
            self.invincible_end = pygame.time.get_ticks() + 3000
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == GameState.INSTRUCTIONS:
            self.draw_instructions()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Title
        title = self.font_large.render("SNAKE GAME", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render("Select Difficulty:", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Difficulty options
        options = [
            ("1 - Easy", 280),
            ("2 - Medium", 340),
            ("3 - Hard", 400),
            ("I - Instructions", 480),
            ("ESC - Quit", 540)
        ]
        
        for text, y in options:
            option = self.font_medium.render(text, True, YELLOW)
            option_rect = option.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(option, option_rect)
        
        # High score
        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, GOLD)
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game(self):
        # Draw grid (subtle)
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            rect = pygame.Rect(
                obstacle.x * GRID_SIZE,
                obstacle.y * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(self.screen, GRAY, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        # Draw food
        self.food.draw(self.screen)
        
        # Draw power-up
        if self.power_up:
            self.power_up.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw snake
        self.snake.draw(self.screen)
        
        # Draw HUD
        self.draw_hud()
    
    def draw_hud(self):
        # Score
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # High score
        high_score_text = self.font_tiny.render(f"High: {self.high_score}", True, GOLD)
        self.screen.blit(high_score_text, (10, 45))
        
        # Lives
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, RED)
        self.screen.blit(lives_text, (WINDOW_WIDTH - 150, 10))
        
        # Level
        level_text = self.font_small.render(f"Level: {self.level}", True, CYAN)
        self.screen.blit(level_text, (WINDOW_WIDTH - 150, 45))
        
        # Active effects
        y_offset = 80
        current_time = pygame.time.get_ticks()
        
        if self.invincible:
            remaining = (self.invincible_end - current_time) // 1000
            effect_text = self.font_tiny.render(f"Invincible: {remaining}s", True, ORANGE)
            self.screen.blit(effect_text, (10, y_offset))
            y_offset += 25
        
        if self.score_multiplier > 1:
            remaining = (self.multiplier_end - current_time) // 1000
            effect_text = self.font_tiny.render(f"2x Score: {remaining}s", True, YELLOW)
            self.screen.blit(effect_text, (10, y_offset))
            y_offset += 25
        
        if current_time < self.speed_boost_end:
            remaining = (self.speed_boost_end - current_time) // 1000
            effect_text = self.font_tiny.render(f"Speed Boost: {remaining}s", True, CYAN)
            self.screen.blit(effect_text, (10, y_offset))
            y_offset += 25
        
        if current_time < self.slow_down_end:
            remaining = (self.slow_down_end - current_time) // 1000
            effect_text = self.font_tiny.render(f"Slow Down: {remaining}s", True, PURPLE)
            self.screen.blit(effect_text, (10, y_offset))
    
    def draw_pause_overlay(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = self.font_small.render("Press P or ESC to resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(resume_text, resume_rect)
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # High score
        if self.score == self.high_score and self.score > 0:
            new_high_text = self.font_small.render("NEW HIGH SCORE!", True, GOLD)
            new_high_rect = new_high_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(new_high_text, new_high_rect)
        
        # Instructions
        restart_text = self.font_small.render("Press ENTER to restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_small.render("Press ESC for menu", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 140))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_instructions(self):
        # Title
        title = self.font_large.render("INSTRUCTIONS", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            ("Controls:", 120, WHITE),
            ("Arrow Keys or WASD - Move snake", 160, YELLOW),
            ("P or ESC - Pause game", 190, YELLOW),
            ("", 220, WHITE),
            ("Food Types:", 250, WHITE),
            ("Green - Normal food (+10 points)", 290, GREEN),
            ("Gold - Bonus food (+50 points)", 320, GOLD),
            ("Cyan - Speed boost (+20 points)", 350, CYAN),
            ("Purple - Slow down (+15 points)", 380, PURPLE),
            ("", 410, WHITE),
            ("Power-ups:", 440, WHITE),
            ("Orange - Invincibility (5 seconds)", 480, ORANGE),
            ("Yellow - 2x Score multiplier (10 seconds)", 510, YELLOW),
            ("", 540, WHITE),
            ("Press ESC to return to menu", 570, WHITE)
        ]
        
        for text, y, color in instructions:
            if text:
                instruction = self.font_tiny.render(text, True, color)
                instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, y))
                self.screen.blit(instruction, instruction_rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
