import pygame

class RigidBody:
    def __init__(self, position, width, height, velocity=(0, 0), mass=1):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.mass = mass
        self.force = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.angle = 0  # 初始角度
        self.angular_velocity = 0  # 初始角速度

    def apply_force(self, force, point=None):
        self.force += force

    def get_vertices(self):
        x, y = self.position.x, self.position.y
        w, h = self.width, self.height
        return [
            (x, y),
            (x + w, y),
            (x + w, y + h),
            (x, y + h)
        ]

    def update(self, dt):
        # 线性运动
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.force = pygame.Vector2(0, 0)
 
