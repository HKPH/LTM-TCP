class Bullet:
    def __init__(self, x, y, color, direction=1):
        self.x = x
        self.y = y
        self.color = color
        self.vel = 10 * direction
        self.radius = 5

    def draw(self, g):
        pygame.draw.circle(g, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vel
