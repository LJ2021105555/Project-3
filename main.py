import pygame
from objects import RigidBody
from physics import PhysicsEngine
from particles import ParticleSystem
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TIME_STEP

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

engine = PhysicsEngine()
particles = ParticleSystem()

rigid_body1 = RigidBody((300, 200), 50, 50, velocity=(100, 0), mass=10)
rigid_body2 = RigidBody((600, 200), 50, 50, velocity=(-100, 0), mass=20)
objects = [rigid_body1, rigid_body2]

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    engine.update(objects, TIME_STEP)

    if engine.gjk_collision(rigid_body1, rigid_body2):
        engine.resolve_collision(rigid_body1, rigid_body2)
        particles.emit(rigid_body1.position, count=20)

    particles.update(TIME_STEP)

    screen.fill((255, 255, 255))
    for obj in objects:
        pygame.draw.rect(screen, (0, 0, 255), (obj.position.x, obj.position.y, obj.width, obj.height))
    particles.draw(screen)
    pygame.display.flip()

pygame.quit()
 
