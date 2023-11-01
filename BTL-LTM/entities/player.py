class Player:
    width = height = 50

    def __init__(self, startx, starty, color=(255, 0, 0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color
        self.is_jumping = False
        self.jump_count = 10
        self.bullets = []
        self.lives = 3

    def draw(self, g):
        pygame.draw.rect(g, self.color, (self.x, self.y, self.width, self.height), 0)
        for bullet in self.bullets:
            bullet.draw(g)

    def move(self, dirn):
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            if not self.is_jumping:
                self.is_jumping = True
        else:
            self.y += self.velocity

    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

    def shoot(self):
        self.bullets.append(Bullet(self.x, self.y, self.color))

    def hit(self):
        self.lives -= 1
