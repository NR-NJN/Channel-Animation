import pygame
import random
import math
import sys
import pygame.gfxdraw
from perlin_noise import PerlinNoise

 
pygame.init()

 
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Lava Lamp")
clock = pygame.time.Clock()

 
BACKGROUND_COLOR = (10, 15, 30)
LAVA_COLOR_BASE = (200, 50, 10)
LAVA_COLOR_HIGHLIGHT = (255, 150, 20)
LAVA_COLOR_SPECULAR = (255, 255, 220)
GLOW_COLOR = (255, 100, 0)

 
class Blob:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.x_speed = random.uniform(0.5, 1.5) * random.choice([-1, 1])
        self.y_speed = random.uniform(0.5, 1.5) * random.choice([-1, 1])
        self.radius = random.randint(70, 110)
        self.num_points = 40
        self.rest_points = self._generate_circle_points()
        self.scale_x, self.scale_y = 1.0, 1.0
        self.target_scale_x, self.target_scale_y = 1.0, 1.0
        self.noise = PerlinNoise(octaves=4, seed=random.randint(0, 10000))
        self.noise_time = random.uniform(0, 100)
        self.deformation_factor = 0.2

    def _generate_circle_points(self):
        return [
            (self.radius * math.cos(i / self.num_points * 2 * math.pi),
             self.radius * math.sin(i / self.num_points * 2 * math.pi))
            for i in range(self.num_points)
        ]

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        hit_wall = False
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.x_speed *= -1
            hit_wall = True
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.y_speed *= -1
            hit_wall = True
        if hit_wall:
            self.target_scale_x, self.target_scale_y = 1.4, 0.6
        else:
            self.target_scale_x, self.target_scale_y = 1.0, 1.0
        self.scale_x += (self.target_scale_x - self.scale_x) * 0.1
        self.scale_y += (self.target_scale_y - self.scale_y) * 0.1
        self.noise_time += 0.005

    def draw(self, surface):
         
         
         
        
        base_points = []
        highlight_points = []
        specular_points = []

        for i, p in enumerate(self.rest_points):
            angle = (i / self.num_points) * 2 * math.pi
            noise_val = self.noise([math.cos(angle) * 0.5, math.sin(angle) * 0.5, self.noise_time])
            dynamic_radius = self.radius * (1 + noise_val * self.deformation_factor)
            
            deformed_x = dynamic_radius * math.cos(angle)
            deformed_y = dynamic_radius * math.sin(angle)

             
            base_points.append((
                self.x + deformed_x * self.scale_x,
                self.y + deformed_y * self.scale_y
            ))

             
            highlight_points.append((
                self.x - 5 + (deformed_x * 0.9) * self.scale_x,
                self.y - 5 + (deformed_y * 0.9) * self.scale_y
            ))

             
            specular_points.append((
                self.x - self.radius * 0.4 + (deformed_x * 0.25) * self.scale_x,
                self.y - self.radius * 0.4 + (deformed_y * 0.25) * self.scale_y
            ))

         
        pygame.gfxdraw.filled_polygon(surface, base_points, LAVA_COLOR_BASE)
        pygame.gfxdraw.aapolygon(surface, base_points, LAVA_COLOR_BASE)
        
        pygame.gfxdraw.filled_polygon(surface, highlight_points, LAVA_COLOR_HIGHLIGHT)
        pygame.gfxdraw.aapolygon(surface, highlight_points, LAVA_COLOR_HIGHLIGHT)
        
        pygame.gfxdraw.filled_polygon(surface, specular_points, LAVA_COLOR_SPECULAR)
        pygame.gfxdraw.aapolygon(surface, specular_points, LAVA_COLOR_SPECULAR)

 
blobs = [Blob() for _ in range(7)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False

    screen.fill(BACKGROUND_COLOR)
    for blob in blobs:
        blob.update()
        blob.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
