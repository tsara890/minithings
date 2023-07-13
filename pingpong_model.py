import torch
import torch.nn as nn
import torch.optim as optim
import os

class DQN(nn.Module):
    def __init__(self, input_shape, hidden_units, output_shape):
        super().__init__()
        self.linear_layer_block = nn.Sequential(nn.Linear(in_features=input_shape, out_features=hidden_units), nn.ReLU(), nn.Linear(in_features=hidden_units, out_features=output_shape))
        
    def forward(self, x):
        return self.linear_layer_block(x)
    
class DQN_trainer:
    def __init__(self, lr, gamma, model):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            state = state.unsqueeze(dim=0)
            action = action.unsqueeze(dim=0)
            reward = reward.unsqueeze(dim=0)
            next_state = next_state.unsqueeze(dim=0)

            game_over = (game_over, )

        pred = self.model(state) #Q value

        target = pred.clone()
        #Bellman equation: Q_new = r + gamma*max(model(next_predicted_Q))

        for idx in range(len(game_over)):
            Q_new = reward[idx] #no next predicted Q -> Q_new = r + 0
            if not game_over[idx]:
                Q_new = reward[idx] + self.gamma*torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = Q_new
            #when putting into loss_fn(target, pred) -> target is Q_new and pred is Q!!!

        loss = self.loss_fn(target, pred)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


            