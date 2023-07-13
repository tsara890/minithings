#Reference: https://www.youtube.com/watch?v=L8ypSXwyBds&t=1358s

import torch
from collections import deque
import random
import numpy as np

from pingpong_game import Game, Paddle_dir, Point
from pingpong_model import DQN, DQN_trainer

MAX_MEMORY = 10_000
BATCH_SIZE = 100
LR = 0.001

class DQN_agent:
    def __init__(self):
        self.n_games = 0
        self.gamma = 0.9
        self.epsilon = 0
        self.model = DQN(input_shape=12, hidden_units=256, output_shape=3)
        self.trainer = DQN_trainer(lr=LR, gamma=self.gamma, model=self.model)
        self.memory = deque(maxlen=MAX_MEMORY)

    def get_state(self, game):
        #direction of board
        #location of ball (x less than x of board, x in range of board, x greater than end of board)
        paddle_x = game.paddle.x
        ball_x, ball_y = game.ball.x, game.ball.y
        ball_dir_vertical = game.ball_move_val_y
        ball_dir_horizontal = game.ball_move_val_x

        #[ball_left, ball_straight, ball_right,
        # dir_left, dir_stay, dir_right]

        state = [
            ball_x < paddle_x, #ball is left
            ball_x in range(int(paddle_x), int(paddle_x + 100 + 1)), #ball is straight,
            ball_x > (paddle_x + 100),

            ball_y < game.h/2, #ball not in paddle's half
            ball_y > game.h/2, #ball is in paddle's half

            #ball_dir
            ball_dir_vertical > 0 and ball_dir_horizontal > 0, #D & R
            ball_dir_vertical < 0 and ball_dir_horizontal < 0, #U & L
            ball_dir_vertical < 0 and ball_dir_horizontal > 0, #U & R
            ball_dir_vertical > 0 and ball_dir_horizontal < 0, #D & L

            game.direction == Paddle_dir.LEFT,
            game.direction == Paddle_dir.STAY,
            game.direction == Paddle_dir.RIGHT
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, k=BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)


    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        if random.randint(0, 200) > self.epsilon:
            final_move = [0, 0, 0]
            random_idx = random.randint(0, 2)
            final_move[random_idx] = 1
        
        else:
            final_move = [0, 0, 0]
            state = torch.tensor(state, dtype=torch.float)
            pred = self.model(state)
            idx = pred.argmax().item()
            final_move[idx] = 1
        
        return final_move
    
def train():
    record = 0
    agent = DQN_agent()
    game = Game()

    while True:
        state = agent.get_state(game=game)
        action = agent.get_action(state=state)

        reward, game_over, score = game.play_step(action)
        new_state= agent.get_state(game=game)
        #print(state)

        agent.train_short_memory(state, action, reward, new_state, game_over)

        agent.remember(state, action, reward, new_state, game_over)

        if game_over:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
        
            if score > record:
                record = score
                agent.model.save()

            print(f"Game: {agent.n_games} Score: {score} Record: {record}")


if __name__ == "__main__":
    train()




    
    
    
    


