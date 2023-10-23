import torch
import random
import numpy as np
from collections import deque
from game import MinesweeperGameAI, ROWS, COLS

from model import Linear_QNet, QTrainer


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class square:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(3*ROWS*COLS, 256, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    
    
    def get_state(self, game):
        playerGrid = game.playerGrid

        state = []

        for row in range(ROWS):
            for col in range(COLS):
                square = playerGrid.grid[row][col]

                if square.revealed:
                    state.append(1)  # Square is revealed
                else:
                    state.append(0)  # Square is unrevealed

                # if square.markedBomb:
                #     state.append(1)  # Square is marked as a bomb
                # else:
                #     state.append(0)  # Square is not marked as a bomb

                state.append(square.numOfBombs)  # Number of bombs adjacent to the square

                if square.path and square.revealed:
                    state.append(1)  # Square is part of the path
                elif  not square.path and square.revealed:
                    state.append(0)  # Square is not part of the path
                else:
                    state.append(-1)  # Square is unrevealed

        return state


    def get_action(self, state, game):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            # Explore: Choose a random action with probability epsilon
            
            while True:
                row = random.randint(0, ROWS - 1)
                col = random.randint(0, COLS - 1)
                if not game.playerGrid.grid[row][col].revealed:
                    break
            return (row, col)
        else:
            # Exploit: Choose the action with the highest Q-value
            # q_values = self.model.predict(state)  # Use your Q-network to predict Q-values
            # return action_with_highest_q_value(q_values)
            state0 = torch.tensor(state, dtype=torch.float)
            q_values = self.model(state0)
            chosen_action = torch.argmax(q_values).item()
            
            # Convert the chosen action to row and column
            row = chosen_action // COLS
            col = chosen_action % COLS
            return (row, col)
    
    def remember(self, state, row, col, reward, next_state, done):
        self.memory.append((state, row,col, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, rows, cols, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, rows, cols, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, row, col, reward, next_state, done):
        self.trainer.train_step(state, row, col, reward, next_state, done)
    

    

    


                
        
def train():
 
    agent = Agent()
    game = MinesweeperGameAI()
    while True:
        try:
            # get old state
            state_old = agent.get_state(game)

            # get move
            square.row, square.col = agent.get_action(state_old, game)

    #self.gameOver, self.win, self.numOfFoundPath, reward

            # perform move and get new state
            done, reward = game.play_step(square)
            state_new = agent.get_state(game)

            # train short memory
            agent.train_short_memory(state_old, square.row, square.col, reward, state_new, done)


            # remember
            agent.remember(state_old, square.row, square.col, reward, state_new, done)

            if done:
                game.reset()
                agent.n_games += 1
                agent.train_long_memory()
        except Exception as e:
            print(f"Caught an exception: {e}")
            game.reset()  # Reset the game when path generation fails








if __name__ == '__main__':
    train()


#Q[state][action] = Q[state][action] + alpha * (reward + gamma * max(Q[new_state]) - Q[state][action])
