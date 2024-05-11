import abc
from src.pong import Game


class BaseAgent:
    game: Game

    @abc.abstractmethod
    def run_game(self, game: Game, framerate: int) -> int:
        raise NotImplementedError("Method run_game not implemented")

    def run_simulation(self, num_games: int):
        scores = []
        framerate = 60
        self.game = Game(framerate=framerate)

        for _ in range(num_games):
            self.run_game(self.game, framerate=framerate)
            scores.append(self.game.score)

            self.game.reset()

        print(f"Average score: {sum(scores) / len(scores)}")
        print(f"Max score: {max(scores)}")
        print(f"Min score: {min(scores)}")
        print("Press any key to exit.")
        input()
