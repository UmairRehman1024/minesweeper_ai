import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_dims, n_actions, conv_units, dense_units):
        super(Linear_QNet, self).__init__()

        # Q-network 1
        self.conv_layers = nn.Sequential(
            nn.Conv2d(input_dims[0], conv_units, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(conv_units, conv_units, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(conv_units, conv_units, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(conv_units, conv_units, kernel_size=3, padding=1),
            nn.ReLU()
        )

        # Calculate the size of the flattened output
        conv_output_size = conv_units * input_dims[1] * input_dims[2]
        # 32 * 8 * 8


        self.flatten = nn.Flatten(0,2)

        self.fc_layers1 = nn.Sequential(
            nn.Linear(conv_output_size, dense_units),
            nn.ReLU()
        )

        self.fc_layers2 = nn.Sequential(
            nn.Linear(dense_units, n_actions)


        )


        # 
    def forward(self, x):
        x = self.conv_layers(x)
        x = self.flatten(x)
        x = self.fc_layers1(x)
        x = self.fc_layers2(x)
        return x

        
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
    
    def load_model(model, file_name='model.pth'):
        # Load the model's state dictionary from the file
        model_folder_path = './model'
        file_path = os.path.join(model_folder_path, file_name)
        
        if os.path.exists(file_path):
            print(f"Loading model from {file_path}")
            model.load_state_dict(torch.load(file_path))
            model.eval()  # Set the model to evaluation mode
            return model
        else:
            print(f"Model file '{file_path}' not found. Using a fresh model.")
            return model



class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()



    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        target = pred.clone()
        for idx in range(done):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()