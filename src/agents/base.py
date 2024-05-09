import abc
from src.pong import Game


class BaseAgent:
    @abc.abstractmethod
    def run_game(self, game: Game, framerate: int) -> int:
        raise NotImplementedError("Method run_game not implemented")

    def run_simulation(self, num_games: int):
        scores = []
        framerate = 60
        game = Game(framerate=framerate)

        for _ in range(num_games):
            score = self.run_game(game, framerate=framerate)
            scores.append(score)

            game.reset()
