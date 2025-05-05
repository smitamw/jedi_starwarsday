import pygame
import asyncio
import platform
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jedi Animation")
clock = pygame.time.Clock()

# Jedi properties
jedi_pos = [100, HEIGHT - 100]
walk_speed = 3
walk_frame = 0
walk_frames = 4  # Simple 4-frame walk cycle
saber_angle = 0
saber_swing_speed = 5
direction = 1  # 1 for right, -1 for left

def setup():
    pass  # Initialization already done above

def draw_jedi(surface, x, y, frame, saber_angle, direction):
    # Draw Jedi body (simple shapes)
    # Head
    pygame.draw.circle(surface, (200, 150, 100), (int(x), int(y - 50)), 20)
    # Robe
    pygame.draw.rect(surface, (139, 69, 19), (int(x - 20), int(y - 30), 40, 60))
    
    # Legs (simple animation)
    leg_offset = math.sin(frame * 0.5) * 10 * direction
    pygame.draw.line(surface, BLACK, (x - 10, y), (x - 10 + leg_offset, y + 30), 5)
    pygame.draw.line(surface, BLACK, (x + 10, y), (x + 10 - leg_offset, y + 30), 5)
    
    # Arms
    pygame.draw.line(surface, (139, 69, 19), (x - 20, y - 30), (x - 30, y - 10), 5)
    
    # Lightsaber (rotating)
    saber_length = 50
    saber_end_x = x + 30 + math.cos(math.radians(saber_angle)) * saber_length * direction
    saber_end_y = y - 20 + math.sin(math.radians(saber_angle)) * saber_length
    pygame.draw.line(surface, GREEN, (x + 20 * direction, y - 20), (saber_end_x, saber_end_y), 5)
    # Saber glow effect
    pygame.draw.line(surface, (144, 238, 144), (x + 20 * direction, y - 20), (saber_end_x, saber_end_y), 9)

def update_loop():
    global jedi_pos, walk_frame, saber_angle, direction, saber_swing_speed
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
    
    # Update Jedi position
    jedi_pos[0] += walk_speed * direction
    if jedi_pos[0] > WIDTH - 50 or jedi_pos[0] < 50:
        direction *= -1  # Reverse direction at screen edges
    
    # Update animation frames
    walk_frame += 0.1
    if walk_frame >= walk_frames:
        walk_frame = 0
    
    # Update lightsaber swing
    saber_angle += saber_swing_speed
    if saber_angle > 45 or saber_angle < -45:
        saber_swing_speed *= -1
    
    # Draw
    screen.fill(BLACK)
    draw_jedi(screen, jedi_pos[0], jedi_pos[1], walk_frame, saber_angle, direction)
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())