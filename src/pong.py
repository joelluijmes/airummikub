import sys
import pygame
import random


SIZE = WIDTH, HEIGHT = 800, 600
PADDLE_OFFSET = 25
WALL_WIDTH = 10

WHITE = 255, 255, 255

BLACK = 0, 0, 0
RED = 255, 0, 0


class Paddle(pygame.sprite.Sprite):
    SPEED = 8

    def __init__(self, color, width, height, left_position):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.rect.left = left_position

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.rect.y > WALL_WIDTH:
            self.rect.y -= self.SPEED
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height - WALL_WIDTH:
            self.rect.y += self.SPEED


class Wall(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, x, y):
        super().__init__()

        self.image = pygame.Surface([radius * 2, radius * 2])
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # self.speed = random.choice([[5, 5], [-5, 5], [5, -5], [-5, -5]])
        self.speed = [0, 0]

    def update(self):
        self.rect = self.rect.move(self.speed)


class Game:
    def __init__(self, framerate=60):
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.paddle = Paddle(color=WHITE, width=10, height=50, left_position=PADDLE_OFFSET)
        self.ball = Ball(color=WHITE, radius=10, x=WIDTH // 2, y=HEIGHT // 2)
        self.wall_top = Wall(color=WHITE, width=WIDTH, height=WALL_WIDTH, x=0, y=0)
        self.wall_bottom = Wall(color=WHITE, width=WIDTH, height=WALL_WIDTH, x=0, y=HEIGHT - 10)
        self.wall_right = Wall(color=WHITE, width=WALL_WIDTH, height=HEIGHT, x=WIDTH - WALL_WIDTH, y=0)

        self.sprites = pygame.sprite.Group(
            self.paddle,
            self.ball,
            self.wall_top,
            self.wall_bottom,
            self.wall_right,
        )

        self.framerate = framerate

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Check for game over
            if self.ball.rect.left < 0:
                self.screen.fill(color=RED)
                pygame.display.flip()
                self.clock.tick(60)
                continue

            # Check for collisions
            if pygame.sprite.spritecollide(self.ball, [self.wall_right], False):
                self.ball.speed[0] *= -1
            if pygame.sprite.spritecollide(self.ball, [self.wall_top, self.wall_bottom], False):
                self.ball.speed[1] *= -1
            if pygame.sprite.spritecollide(self.ball, [self.paddle], False):
                self.ball.speed[0] *= -1

            # Redraw the screen
            self.sprites.update()
            self.screen.fill(color=BLACK)
            self.sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.framerate)


def main():
    pygame.init()

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
