import sys
from typing import Literal
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

        if keys[pygame.K_UP]:
            self.move("up")
        if keys[pygame.K_DOWN]:
            self.move("down")

    def move(self, direction: Literal["up", "down"]):
        if direction == "up" and self.rect.y > WALL_WIDTH:
            self.rect.y -= self.SPEED
        if direction == "down" and self.rect.y < HEIGHT - self.rect.height - WALL_WIDTH:
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
    def __init__(self, color, radius):
        super().__init__()

        self.image = pygame.Surface([radius * 2, radius * 2])
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect = self.rect.move(self.speed)


class Game:
    def __init__(self, framerate=60):
        pygame.init()

        self.screen = pygame.display.set_mode(SIZE)
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()

        self.paddle = Paddle(color=WHITE, width=10, height=50, left_position=PADDLE_OFFSET)
        self.ball = Ball(color=WHITE, radius=10)
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
        self.score = 0
        self.top_score = 0

        self.reset()

    def reset(self):
        self.completed = False
        self.num_ticks = 0
        self.num_paddle_hits = 0
        self.score = 0

        self.paddle.rect.y = HEIGHT // 2 - self.paddle.rect.height // 2
        self.ball.rect.x = WIDTH // 2
        self.ball.rect.y = HEIGHT // 2
        self.ball.speed = random.choice([[5, 5], [-5, 5], [5, -5], [-5, -5]])

    def run(self):
        while True:
            self.tick()
            self.clock.tick(self.framerate)

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Check for game over
        if self.ball.rect.left < 0:
            self.screen.fill(color=RED)
            pygame.display.flip()
            self.completed = True
            return

        # Check for collisions
        if pygame.sprite.spritecollide(self.ball, [self.wall_right], False):
            self.ball.speed[0] *= -1
        if pygame.sprite.spritecollide(self.ball, [self.wall_top, self.wall_bottom], False):
            self.ball.speed[1] *= -1
        if pygame.sprite.spritecollide(self.ball, [self.paddle], False):
            self.ball.speed[0] *= -1
            # Ensure the ball is outside the paddle, thereby preventing multiple hits
            self.ball.rect.x = PADDLE_OFFSET + self.paddle.rect.width * 2
            self.num_paddle_hits += 1

        # Redraw the screen
        self.sprites.update()
        self.screen.fill(color=BLACK)
        self.sprites.draw(self.screen)

        # Render stats
        self.score = self.num_paddle_hits * 50 + self.num_ticks // 50
        score_text = self.font.render(f"Score:         {self.score:09d}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        self.top_score = max(self.score, self.top_score)
        top_score_text = self.font.render(f"Top Score: {self.top_score:09d}", True, WHITE)
        self.screen.blit(top_score_text, (10, 25))

        pygame.display.flip()
        self.num_ticks += 1


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
