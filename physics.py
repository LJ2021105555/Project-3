import pygame

class PhysicsEngine:
    def __init__(self, gravity=(0, 9.8)):
        self.gravity = pygame.Vector2(gravity)

    def apply_gravity(self, obj):
        if obj.mass > 0:
            obj.apply_force(self.gravity * obj.mass)

    def triple_product(self, a, b, c):
        """
        计算三重积，用于找到垂直方向。
        """
        return b * (a.dot(c)) - c * (a.dot(b))

    def gjk_collision(self, obj1, obj2):
        """
        使用 GJK 算法检测两个凸多边形的碰撞。
        obj1 和 obj2 需要提供方法 get_vertices()，返回多边形顶点列表。
        """
        def support(obj1, obj2, direction):
            """计算 Minkowski 差的支撑点。"""
            farthest_in_obj1 = max(obj1.get_vertices(), key=lambda v: pygame.Vector2(v).dot(direction))
            farthest_in_obj2 = max(obj2.get_vertices(), key=lambda v: pygame.Vector2(v).dot(-direction))
            return pygame.Vector2(farthest_in_obj1) - pygame.Vector2(farthest_in_obj2)

        # 初始方向任意选择
        direction = pygame.Vector2(1, 0)

        # 第一个支撑点
        simplex = [support(obj1, obj2, direction)]

        # 反向朝原点
        direction = -simplex[0]

        while True:
            # 添加新的支撑点
            new_point = support(obj1, obj2, direction)
            if new_point.dot(direction) <= 0:
                # 新点不能更接近原点，说明未碰撞
                return False

            simplex.append(new_point)

            if self.handle_simplex(simplex, direction):
                # 处理单形，确定是否包含原点
                return True

    def handle_simplex(self, simplex, direction):
        """
        处理单形。
        如果包含原点，返回 True。
        如果不包含原点，则更新方向。
        """
        if len(simplex) == 2:  # 线段
            b, a = simplex
            ab = b - a
            ao = -a
            if ab.dot(ao) > 0:
                direction.update(self.triple_product(ab, ao, ab))
            else:
                simplex.pop(0)
                direction.update(ao)
        elif len(simplex) == 3:  # 三角形
            c, b, a = simplex
            ab = b - a
            ac = c - a
            ao = -a

            # 检查 AC 方向
            ac_perp = self.triple_product(ab, ac, ac)
            if ac_perp.dot(ao) > 0:
                simplex.pop(1)  # 移除 B 点
                direction.update(ac_perp)
            else:
                # 检查 AB 方向
                ab_perp = self.triple_product(ac, ab, ab)
                if ab_perp.dot(ao) > 0:
                    simplex.pop(0)  # 移除 C 点
                    direction.update(ab_perp)
                else:
                    # 原点在三角形内部
                    return True
        return False

    def resolve_collision(self, obj1, obj2):
        """
        简单弹性碰撞响应，交换法线方向的速度分量。
        """
        normal = (obj2.position - obj1.position).normalize()
        relative_velocity = obj1.velocity - obj2.velocity

        # 计算沿法线方向的速度分量
        velocity_along_normal = relative_velocity.dot(normal)
        if velocity_along_normal > 0:
            return  # 如果分离，不需要处理碰撞

        # 计算弹性系数（假设完全弹性碰撞）
        restitution = 1.0

        # 碰撞速度
        impulse = -(1 + restitution) * velocity_along_normal
        impulse /= (1 / obj1.mass) + (1 / obj2.mass)

        # 应用冲量
        impulse_vector = impulse * normal
        obj1.velocity += impulse_vector / obj1.mass
        obj2.velocity -= impulse_vector / obj2.mass

    def update(self, objects, dt):
        for obj in objects:
            self.apply_gravity(obj)
            obj.update(dt)

 
