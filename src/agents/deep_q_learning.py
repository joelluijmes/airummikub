import random
from collections import deque
from typing import Literal

import pygame
import torch
import torch.nn as nn
import torch.nn.functional as F

from src.pong import Game

from .base import BaseAgent

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DQN(nn.Module):
    def __init__(self, n_state: int, n_actions: int):
        super().__init__()

        self.fc1 = nn.Linear(n_state, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, n_actions)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network."""
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class DeepQLearningAgent(BaseAgent):
    actions = ["up", "down", None]

    def __init__(self):
        self.batch_size = 32
        self.gamma = 0.99
        self.eps = 1.0
        self.eps_min = 0.01
        self.eps_decay = 0.975
        self.tau = 1e-3
        self.lr = 1e-4

        self.n_state = 4  # paddle y, ball x, ball y, ball speed_y
        self.n_actions = len(self.actions)

        self.policy_net = DQN(self.n_state, self.n_actions).to(device)
        self.target_net = DQN(self.n_state, self.n_actions).to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = torch.optim.AdamW(self.policy_net.parameters(), lr=self.lr)
        self.memory = deque(maxlen=10000)

    def run_game(self, game: Game, framerate: int) -> None:

        while not game.completed:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                game.clock.tick(framerate)

            # Get the next action
            state = self.get_current_state()
            action = self.get_action(state)

            # Take the action
            game.paddle.move(action)

            # Get the reward
            reward = game.tick()

            # Store the transition in the memory
            next_state = self.get_current_state()
            self.memory.append((state, self.actions.index(action), reward, next_state, game.completed))

            # Replay
            self.replay()
            self.update_target_net()

    def get_current_state(self) -> tuple:
        return (
            self.game.paddle.rect.y,
            self.game.ball.rect.x,
            self.game.ball.rect.y,
            self.game.ball.speed[1],
        )

    def get_action(self, state: tuple) -> Literal["up", "down"] | None:
        # Epsilon-greedy policy
        self.eps = max(self.eps_min, self.eps * self.eps_decay)
        if random.random() < self.eps:
            return random.choice(self.actions)

        state_tensor = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        q_values = self.policy_net(state_tensor)
        return self.actions[torch.argmax(q_values).item()]

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        # Sample a batch from the memory
        mini_batch = random.sample(self.memory, self.batch_size)

        # Prepare the tensors
        states, actions, rewards, next_states, dones = zip(*mini_batch)
        states = torch.tensor(states, device=device, dtype=torch.float32)
        actions = torch.tensor(actions, device=device, dtype=torch.int64)
        rewards = torch.tensor(rewards, device=device, dtype=torch.float32)
        next_states = torch.tensor(next_states, device=device, dtype=torch.float32)
        dones = torch.tensor(dones, device=device, dtype=torch.float32)

        # Run the mini-batch through the network
        current_q_values = self.policy_net(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.target_net(next_states).max(1)[0]
        expected_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        # Compute the loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(current_q_values, expected_q_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_net(self) -> None:
        """Update the target network with the policy network."""
        for target_param, policy_param in zip(self.target_net.parameters(), self.policy_net.parameters()):
            target_param.data.copy_(self.tau * policy_param.data + (1.0 - self.tau) * target_param.data)


if __name__ == "__main__":
    agent = DeepQLearningAgent()
    agent.run_simulation(10000)
