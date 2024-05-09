import random
from src.pong import Game
from .base import BaseAgent


class RandomAgent(BaseAgent):
    def run_game(self, game: Game, framerate: int):
        while not game.completed:
            game.tick()

            direction = random.choice(["up", "down", None])
            if direction is not None:
                game.paddle.move(direction)

            if framerate:
                game.clock.tick(framerate)


if __name__ == "__main__":
    agent = RandomAgent()
    agent.run_simulation(100)
