import random
from typing import Literal

import pygame

from src.pong import Game

from .base import BaseAgent


class QLearningAgent(BaseAgent):
    actions = ["up", "down", None]  # noqa: RUF012
    q_table = {}  # noqa: RUF012

    exploration_rate = 1.0
    exploration_decay = 0.975
    learning_rate = 0.1
    discount_factor = 0.99

    def run_game(self, game: Game, framerate: int) -> None:
        while not game.completed:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                game.clock.tick(framerate)

            # Get the next action
            state = self.get_current_state()
            if state not in self.q_table:
                self.q_table[state] = [0] * len(self.actions)

            action = self.get_action(state)

            # Take the action
            game.paddle.move(action)
            reward = game.tick()

            # Get the next state
            next_state = self.get_current_state()
            if next_state not in self.q_table:
                self.q_table[next_state] = [0] * len(self.actions)

            current_q_value = self.q_table[state][self.actions.index(action)]
            next_max_q_value = max(self.q_table[next_state])

            # Update the q-value
            q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * next_max_q_value - current_q_value)
            self.q_table[state][self.actions.index(action)] = q_value

        # Update the exploration rate
        self.exploration_rate *= self.exploration_decay

    def get_current_state(self) -> tuple:
        return (
            self.game.paddle.rect.y // 5,
            self.game.ball.rect.y // 5,
            self.game.ball.speed[1],
        )

    def get_action(self, state: tuple) -> Literal["up", "down"] | None:
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        else:
            return self.actions[self.q_table[state].index(max(self.q_table[state]))]


if __name__ == "__main__":
    agent = QLearningAgent()
    agent.run_simulation(10000)
