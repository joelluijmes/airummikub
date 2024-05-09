import abc
from src.pong import Game


class BaseAgent:
    @abc.abstractmethod
    def run_game(self, game: Game, framerate: int) -> int:
        raise NotImplementedError("Method run_game not implemented")

    def run_simulation(self, num_games: int):
        scores = []
        framerate = 1000
        game = Game(framerate=framerate)

        for _ in range(num_games):
            self.run_game(game, framerate=framerate)
            scores.append(game.score)

            game.reset()

        print(f"Average score: {sum(scores) / len(scores)}")
        print(f"Max score: {max(scores)}")
        print(f"Min score: {min(scores)}")
        print("Press any key to exit.")
        input()
