import abc
from src.pong import Game


class BaseAgent:
    @abc.abstractmethod
    def run_game(self, game: Game, framerate: int) -> int:
        raise NotImplementedError("Method run_game not implemented")

    def run_simulation(self, num_games: int):
        scores = []
        game = Game()

        for _ in range(num_games):
            score = self.run_game(game, framerate=60)
            scores.append(score)

            game.reset()
