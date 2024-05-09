import sys
import pygame


SIZE = WIDTH, HEIGHT = 800, 600
PADDLE_OFFSET = 25
WALL_WIDTH = 10

WHITE = 255, 255, 255

BLACK = 0, 0, 0
RED = 255, 0, 0


class Paddle(pygame.sprite.Sprite):
    SPEED = 5

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

        self.speed = [5, 5]

    def update(self):
        self.rect = self.rect.move(self.speed)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)

    sprites = pygame.sprite.Group()
    paddle = Paddle(color=WHITE, width=10, height=50, left_position=PADDLE_OFFSET)
    sprites.add(paddle)
    ball = Ball(color=WHITE, radius=10, x=WIDTH // 2, y=HEIGHT // 2)
    sprites.add(ball)

    wall_top = Wall(color=WHITE, width=WIDTH, height=WALL_WIDTH, x=0, y=0)
    wall_bottom = Wall(color=WHITE, width=WIDTH, height=WALL_WIDTH, x=0, y=HEIGHT - 10)
    wall_right = Wall(color=WHITE, width=WALL_WIDTH, height=HEIGHT, x=WIDTH - WALL_WIDTH, y=0)

    sprites.add(wall_top)
    sprites.add(wall_bottom)
    sprites.add(wall_right)

    clock = pygame.time.Clock()

    # Enter the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Check for game over
        if ball.rect.left < 0 or ball.rect.right > WIDTH:
            screen.fill(color=RED)
            pygame.display.flip()
            clock.tick(60)
            continue

        # Process movements
        sprites.update()

        # Draw everything
        screen.fill(color=BLACK)
        sprites.draw(screen)

        # Check wall collisions, they are just perpendicular to the ball's speed
        if pygame.sprite.spritecollide(ball, [wall_right], False):
            ball.speed[0] *= -1
        if pygame.sprite.spritecollide(ball, [wall_top, wall_bottom], False):
            ball.speed[1] *= -1

        # Check paddle collision, here we check where the ball is hitting the paddle
        if pygame.sprite.spritecollide(ball, [paddle], False):
            # This doesn't seem to work, lets go with basic version
            ball.speed[0] *= -1

            # intersection_point = pygame.sprite.collide_mask(ball, paddle)
            # if intersection_point:
            #     relative_intersect_y = (paddle.rect.y + paddle.rect.height // 2) - intersection_point[1]
            #     normalized_intersect_y = relative_intersect_y / (paddle.rect.height // 2)

            #     # Calculate the bounce angle based on the collision position
            #     bounce_angle = normalized_intersect_y * math.radians(75)

            #     # Calculate the new velocity components
            #     speed = 5
            #     ball.speed[0] = -speed * math.cos(bounce_angle)
            #     ball.speed[1] = speed * math.sin(bounce_angle)

        # Update the display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
