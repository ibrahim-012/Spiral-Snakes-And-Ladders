import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Get screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spiral Snakes & Ladders")

# Colors
BLUE = (100, 149, 237)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
MAX_COLOR = (255, 100, 100)  # Light red
MIN_COLOR = (100, 255, 100)  # Light green

# Game constants
NUM_RINGS = 3
TILES_PER_RING = 10
TILE_RADIUS = 30
PLAYER_MARKER_RADIUS = 15
FONT_SIZE = 24
STATUS_HEIGHT = 70

# Font
font = pygame.font.SysFont('Arial', FONT_SIZE)
bold_font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)

class Tile:
    def __init__(self, ring, index):
        self.ring = ring
        self.index = index
        self.snake_or_ladder = None  # (ring, index) or None
        self.center = None
        self.radius = TILE_RADIUS

class Board:
    def __init__(self, num_rings=3, tiles_per_ring=10):
        self.num_rings = num_rings
        self.tiles_per_ring = tiles_per_ring
        self.tiles = self._init_board()
        self._add_sample_snakes_ladders()
        self._calculate_positions()

    def _init_board(self):
        return {(r, i): Tile(r, i) for r in range(self.num_rings) for i in range(self.tiles_per_ring)}

    def _add_sample_snakes_ladders(self):
        # Snakes - denoted by red arrows
        self.tiles[(0, 4)].snake_or_ladder = (1, 5)
        self.tiles[(1, 2)].snake_or_ladder = (2, 3)

        # Ladders - denoted by green arrows
        self.tiles[(2, 6)].snake_or_ladder = (1, 7)
        self.tiles[(2, 9)].snake_or_ladder = (1, 0)
        self.tiles[(1, 8)].snake_or_ladder = (0, 7)

    def _calculate_positions(self):
        center_x, center_y = SCREEN_WIDTH // 2, (SCREEN_HEIGHT + STATUS_HEIGHT) // 2
        ring_spacing = min(SCREEN_WIDTH, SCREEN_HEIGHT - STATUS_HEIGHT) // (2 * self.num_rings + 2)
        
        for ring in range(self.num_rings):
            radius = (ring + 1) * ring_spacing
            for i in range(self.tiles_per_ring):
                angle = 2 * math.pi * i / self.tiles_per_ring
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                tile = self.tiles[(ring, i)]
                tile.center = (x, y)

    def get_next_position(self, position, direction, steps):
        r, i = position
        tiles_in_ring = self.tiles_per_ring
        new_index = (i + steps) % tiles_in_ring if direction == "CW" else (i - steps + tiles_in_ring) % tiles_in_ring
        new_pos = (r, new_index)
        return self.tiles[new_pos].snake_or_ladder or new_pos

    def draw(self, screen, current_pos):
    # Draw arrows first (behind tiles)
        for (r, i), tile in self.tiles.items():
            if tile.snake_or_ladder:
                target_r, target_i = tile.snake_or_ladder
                target_tile = self.tiles[(target_r, target_i)]
                color = GREEN if target_r < r else RED  # Ladder if moving inward, snake if outward

                # Offset line start and end so it doesn't overlap the tile centers
                start = self._offset_point(tile.center, target_tile.center, tile.radius)
                end = self._offset_point(target_tile.center, tile.center, tile.radius)

                pygame.draw.line(screen, color, start, end, 3)
                self._draw_arrow(screen, start, end, color)

        # Draw tiles on top
        for (r, i), tile in self.tiles.items():
            color = YELLOW if (r, i) == current_pos else LIGHT_BLUE
            pygame.draw.circle(screen, color, tile.center, tile.radius)
            pygame.draw.circle(screen, BLACK, tile.center, tile.radius, 2)

            # Draw tile number
            text = font.render(str(i), True, BLACK)
            text_rect = text.get_rect(center=tile.center)
            screen.blit(text, text_rect)

    def _offset_point(self, start, end, offset):
        dx, dy = end[0] - start[0], end[1] - start[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return start
        ratio = offset / dist
        return (start[0] + dx * ratio, start[1] + dy * ratio)


    def _draw_arrow(self, screen, start, end, color):
        angle = math.atan2(end[1]-start[1], end[0]-start[0])
        arrow_size = 10
        
        # Calculate arrow points
        p1 = (end[0] - arrow_size * math.cos(angle - math.pi/6),
            end[1] - arrow_size * math.sin(angle - math.pi/6))
        p2 = (end[0] - arrow_size * math.cos(angle + math.pi/6),
            end[1] - arrow_size * math.sin(angle + math.pi/6))
        
        pygame.draw.polygon(screen, color, [end, p1, p2])

class GameState:
    def __init__(self, start_pos):
        self.position = start_pos

    def is_goal(self):
        return self.position == (0, 0)

class MaxPlayer:
    def __init__(self, board):
        self.board = board

    def heuristic(self, position):
        ring, index = position
        
        if position == (0, 0):
            return float('inf')
        
        ring_progress = (self.board.num_rings - ring) * 50
        
        ladder_dist = self._distance_to_nearest_ladder(position)
        ladder_bonus = (10 - ladder_dist) * 3 if ladder_dist < 4 else 0
        
        snake_dist = self._distance_to_nearest_snake(position)
        snake_penalty = (10 - snake_dist) * 5 if snake_dist < 3 else 0
        
        goal_dist = index if ring == 0 else float('inf')
        goal_progress = (self.board.tiles_per_ring - goal_dist) if ring == 0 else 0
        
        return ring_progress + ladder_bonus - snake_penalty + goal_progress

    def _distance_to_nearest_ladder(self, position):
        min_dist = float('inf')
        for (r, i), tile in self.board.tiles.items():
            if tile.snake_or_ladder and tile.snake_or_ladder[0] < r:
                dist = min((i - position[1]) % self.board.tiles_per_ring,
                          (position[1] - i) % self.board.tiles_per_ring)
                if dist < min_dist:
                    min_dist = dist
        return min_dist if min_dist != float('inf') else 999

    def _distance_to_nearest_snake(self, position):
        min_dist = float('inf')
        for (r, i), tile in self.board.tiles.items():
            if tile.snake_or_ladder and tile.snake_or_ladder[0] > r:
                dist = min((i - position[1]) % self.board.tiles_per_ring,
                          (position[1] - i) % self.board.tiles_per_ring)
                if dist < min_dist:
                    min_dist = dist
        return min_dist if min_dist != float('inf') else 999

    def expectimax(self, position):
        directions = ["CW", "CCW"]
        best_value = float('-inf')
        best_direction = None

        for direction in directions:
            expected_value = 0
            for roll in range(1, 7):
                next_pos = self.board.get_next_position(position, direction, roll)
                expected_value += self.heuristic(next_pos)
            expected_value /= 6
            if expected_value > best_value:
                best_value = expected_value
                best_direction = direction

        return best_direction

class MinPlayer:
    def __init__(self, board):
        self.board = board
        self.max_player = MaxPlayer(board)

    def heuristic(self, position):
        return -self.max_player.heuristic(position)

    def choose_worst_direction(self, position):
        directions = ["CW", "CCW"]
        worst_value = float('inf')
        worst_direction = None

        for direction in directions:
            expected_value = 0
            would_reach_goal = False
            
            for roll in range(1, 4):
                next_pos = self.board.get_next_position(position, direction, roll)
                
                if position[0] == 0 and next_pos == (0, 0):
                    would_reach_goal = True
                    break
                
                expected_value += self.heuristic(next_pos)
            
            if would_reach_goal:
                continue
                
            expected_value /= 3
            if expected_value < worst_value:
                worst_value = expected_value
                worst_direction = direction

        if worst_direction is None:
            return random.choice(directions)
        
        return worst_direction

def draw_status(screen, turn_count, current_player, last_player=None, last_roll=None, last_direction=None):
    status_rect = pygame.Rect(20, 20, SCREEN_WIDTH - 40, STATUS_HEIGHT)
    pygame.draw.rect(screen, GRAY, status_rect)
    pygame.draw.rect(screen, BLACK, status_rect, 2)
    
    # Current turn information (top line)
    turn_text = f"Turn: {turn_count} | Current Player: "
    player_text = "MAX" if current_player == "MAX" else "MIN"
    player_color = MAX_COLOR if current_player == "MAX" else MIN_COLOR
    
    turn_surface = font.render(turn_text, True, BLACK)
    player_surface = bold_font.render(player_text, True, player_color)
    
    screen.blit(turn_surface, (status_rect.x + 20, status_rect.y + 10))
    screen.blit(player_surface, (status_rect.x + 20 + turn_surface.get_width(), status_rect.y + 10))
    
    # Last move information (bottom line)
    if last_player is not None:
        last_text = f"Last: {last_player}"
        last_color = MAX_COLOR if last_player == "MAX" else MIN_COLOR
        last_surface = font.render(last_text, True, last_color)
        screen.blit(last_surface, (status_rect.x + 20, status_rect.y + 35))
    
    if last_roll is not None:
        roll_text = f"Roll: {last_roll}"
        roll_surface = font.render(roll_text, True, BLACK)
        screen.blit(roll_surface, (status_rect.x + 200, status_rect.y + 35))
    
    if last_direction is not None:
        dir_text = f"Direction: {last_direction}"
        dir_surface = font.render(dir_text, True, BLACK)
        screen.blit(dir_surface, (status_rect.x + 325, status_rect.y + 35))

def main():
    board = Board()
    state = GameState((2, 0))
    max_player = MaxPlayer(board)
    min_player = MinPlayer(board)
    
    MAX_TURNS_ALLOWED = 10
    max_turn_count = 1
    current_player = "MAX"
    last_player = None
    last_roll = None
    last_direction = None
    game_over = False
    message = ""
    
    clock = pygame.time.Clock()
    auto_advance = False
    advance_timer = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE and not game_over:
                    auto_advance = not auto_advance
                elif event.key == pygame.K_RETURN and not auto_advance and not game_over:
                    # Manual advance
                    if current_player == "MAX":
                        last_direction = max_player.expectimax(state.position)
                        last_roll = random.randint(1, 6)
                        next_pos = board.get_next_position(state.position, last_direction, last_roll)
                        state.position = next_pos
                        last_player = "MAX"
                        
                        if state.is_goal():
                            message = f"MAX wins by reaching the goal in {max_turn_count + 1} moves!"
                            game_over = True
                        else:
                            current_player = "MIN"
                    else:
                        last_direction = min_player.choose_worst_direction(state.position)
                        last_roll = random.randint(1, 3)
                        next_pos = board.get_next_position(state.position, last_direction, last_roll)
                        state.position = next_pos
                        last_player = "MIN"
                        
                        if state.is_goal():
                            message = "MAX wins (unexpectedly) after MIN's sabotage!"
                            game_over = True
                        else:
                            current_player = "MAX"
                            max_turn_count += 1
                            if max_turn_count > MAX_TURNS_ALLOWED:
                                message = "MIN wins! MAX failed to reach the goal within 10 moves."
                                game_over = True
        
        # Auto-advance logic
        if auto_advance and not game_over:
            advance_timer += clock.get_rawtime()
            if advance_timer > 500:  # 1 second delay
                advance_timer = 0
                if current_player == "MAX":
                    last_direction = max_player.expectimax(state.position)
                    last_roll = random.randint(1, 6)
                    next_pos = board.get_next_position(state.position, last_direction, last_roll)
                    state.position = next_pos
                    last_player = "MAX"
                    
                    if state.is_goal():
                        message = f"MAX wins by reaching the goal in {max_turn_count + 1} moves!"
                        game_over = True
                    else:
                        current_player = "MIN"
                else:
                    last_direction = min_player.choose_worst_direction(state.position)
                    last_roll = random.randint(1, 3)
                    next_pos = board.get_next_position(state.position, last_direction, last_roll)
                    state.position = next_pos
                    last_player = "MIN"
                    
                    if state.is_goal():
                        message = "MAX wins (unexpectedly) after MIN's sabotage!"
                        game_over = True
                    else:
                        current_player = "MAX"
                        max_turn_count += 1
                        
                        if max_turn_count >= MAX_TURNS_ALLOWED:
                            message = "MIN wins! MAX failed to reach the goal within 10 moves."
                            game_over = True
        
        # Drawing
        screen.fill(WHITE)
        board.draw(screen, state.position)
        draw_status(screen, max_turn_count, current_player, last_player, last_roll, last_direction)

        if game_over:
            # Position the message box at the bottom of the screen
            msg_width = SCREEN_WIDTH // 2
            msg_height = 100
            msg_x = (SCREEN_WIDTH - msg_width) // 2
            msg_y = SCREEN_HEIGHT - msg_height - 20  # 20px padding from bottom

            msg_rect = pygame.Rect(msg_x, msg_y, msg_width, msg_height)
            pygame.draw.rect(screen, GRAY, msg_rect)
            pygame.draw.rect(screen, BLACK, msg_rect, 2)

            # Center message text in the box
            text = font.render(message, True, BLACK)
            screen.blit(text, (msg_rect.centerx - text.get_width() // 2, msg_rect.top + 10))

            restart_text = font.render("Press ESC to quit", True, BLACK)
            screen.blit(restart_text, (msg_rect.centerx - restart_text.get_width() // 2, msg_rect.top + 50))

        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()