import torch
import random
import numpy as np
from collections import deque
from game import MinesweeperGameAI, ROWS, COLS
from helper import plot

from model import Linear_QNet, QTrainer


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.002


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
        model = Linear_QNet(3*ROWS*COLS, 512, ROWS*COLS)
        self.model = Linear_QNet.load_model(model)
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
        self.epsilon = 500 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            # Explore: Choose a random action with probability epsilon
            while True:
                # row = random.randint(0, ROWS - 1)
                # col = random.randint(0, COLS - 1)
                move = random.randint(0, ROWS*COLS - 1)
                row = move // COLS
                col = move % COLS
                if not game.playerGrid.grid[row][col].revealed:
                    break
            return move
        else:
            # Exploit: Use the model to predict row and col
            state0 = torch.tensor(state, dtype=torch.float)
            # prediction = self.model(state0)
            # print(f"prediction: {prediction}")
            # row, col = prediction[0].item(), prediction[1].item()

            # # Ensure the predicted values are within the valid range
            # # row = min(max(0, row), ROWS - 1)
            # # col = min(max(0, col), COLS - 1)
            # print( f"row: {row}, col: {col}")

            moves = self.model(state0)
            moves = moves.flatten()
            # print(f"moves: {moves}")
            # moves = moves.detach().numpy()
            # moves[board!=-0.125] = np.min(moves) # set already clicked tiles to min value

            lowestValueIndex = moves.argmin()
            for i in range(len(moves)):
                if game.playerGrid.grid[i//COLS][i%COLS].revealed:
                    moves[i] = moves[lowestValueIndex]
            move = torch.argmax(moves).item()
            
            return move

            while True:
                prediction = self.model(state0)
                row = prediction // COLS
                col = prediction % COLS

                #check if row and col is valid and not revealed
                if not game.playerGrid.grid[row][col].revealed and row >= 0 or row < ROWS or col >= 0 or col < COLS:
                    break
            
            print( f"row: {row}, col: {col}")



            return (int(row), int(col))
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    

    

    


                
        
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    # numOfFoundPath = 0
    numOfWin = 0
    agent = Agent()
    game = MinesweeperGameAI()
    while True:
        try:
            # get old state
            state_old = agent.get_state(game)

            # get move
            final_move = agent.get_action(state_old, game)

            #self.gameOver, self.win, self.numOfFoundPath, reward

            # perform move and get new state
            done, reward, numOfFoundPath = game.play_step(final_move)
            state_new = agent.get_state(game)

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

            if done:
                if game.win:
                    print("Win")
                    numOfWin += 1
                game.reset()
                agent.n_games += 1
                agent.train_long_memory()

                if numOfFoundPath > record:
                    record = numOfFoundPath
                    agent.model.save()

                print('Game', agent.n_games, 'numOfFoundPath', numOfFoundPath, 'Record:', record, 'numOfWin:', numOfWin)

                plot_scores.append(numOfFoundPath)
                total_score += numOfFoundPath
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

        except Exception as e:
            print(f"Caught an exception: {e}")
            print(e.__cause__)

            try:
                game.reset()  # Reset the game when path generation fails
            except Exception as e:
                print(f"Caught an exception: {e}")
                print(e.__cause__)
                game.reset()
            










if __name__ == '__main__':
    train()


#Q[state][action] = Q[state][action] + alpha * (reward + gamma * max(Q[new_state]) - Q[state][action])
