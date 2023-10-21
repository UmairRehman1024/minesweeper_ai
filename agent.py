import torch
import random
import numpy as np
from collections import deque
from game import MinesweeperGameAI, ROWS, COLS

from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(4*ROWS*COLS, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    
    
    def get_state(self, game):
        playerGrid = game.playerGrid

        state = []

        for row in range(game.ROWS):
            for col in range(game.COLS):
                square = playerGrid.grid[row][col]

                if square.revealed:
                    state.append(1)  # Square is revealed
                else:
                    state.append(0)  # Square is unrevealed

                if square.markedBomb:
                    state.append(1)  # Square is marked as a bomb
                else:
                    state.append(0)  # Square is not marked as a bomb

                state.append(square.numOfBombs)  # Number of bombs adjacent to the square

                if square.path and square.revealed:
                    state.append(1)  # Square is part of the path
                elif  not square.path and square.revealed:
                    state.append(0)  # Square is not part of the path
                else:
                    state.append(-1)  # Square is unrevealed

        return state


    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            # Explore: Choose a random action with probability epsilon
            
            action = random.randint(0, 1)
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            return action, (row, col)
        else:
            # Exploit: Choose the action with the highest Q-value
            q_values = self.model.predict(state)  # Use your Q-network to predict Q-values
            return action_with_highest_q_value(q_values)
        
    


                
        
def train():
 
    agent = Agent()
    game = MinesweeperGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

#self.gameOver, self.win, self.numOfFoundPath, reward

        # perform move and get new state
        done, reward = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()






if __name__ == '__main__':
    train()


#Q[state][action] = Q[state][action] + alpha * (reward + gamma * max(Q[new_state]) - Q[state][action])
