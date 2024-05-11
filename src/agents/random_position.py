import random
from src.pong import Game
from .base import BaseAgent


class RandomDirectionAgent(BaseAgent):
    def run_game(self, game: Game, framerate: int):

        target_destination = random.randint(0, game.screen.get_height() - game.paddle.rect.height)
        margin = game.paddle.rect.height // 2

        while not game.completed:
            game.tick()

            if random.random() >= 0.3:
                if game.paddle.rect.y < target_destination:
                    game.paddle.move("down")
                elif game.paddle.rect.y > target_destination:
                    game.paddle.move("up")

            if abs(game.paddle.rect.y - target_destination) < margin:
                target_destination = random.randint(0, game.screen.get_height() - game.paddle.rect.height)

            if framerate:
                game.clock.tick(framerate)


if __name__ == "__main__":
    agent = RandomDirectionAgent()
    agent.run_simulation(100)
