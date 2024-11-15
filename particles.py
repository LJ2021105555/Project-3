import pygame
import random

class Particle:
    def __init__(self, position, velocity, lifespan):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.lifespan = lifespan
        self.alive = True

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.alive = False

    def draw(self, screen):
        color = (255, 165, 0) if self.lifespan > 1 else (255, 69, 0)
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), 3)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, position, count=10):
        for _ in range(count):
            velocity = pygame.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))
            self.particles.append(Particle(position, velocity, random.uniform(1, 3)))

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
 
