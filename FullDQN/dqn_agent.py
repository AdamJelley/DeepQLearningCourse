import numpy as np
import torch as T
from deep_q_network import DeepQNetwork
from replay_memory import ReplayBuffer

class DQNAgent();
    def __init__(self, gamma, epsilon, lr, n_actions, , input_dims, mem_size, batch_size, eps_min=0.01,
                eps_dec=5e-7, replace=1000, algo=None, env_name=None, checkpoint_dir='tmp/dqn')

        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.n_actions = n_actions
        self.input_dims = input_dims
        self.batch_size = batch_size
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        self.replace_target_cnt = replace
        self.algo = algo
        self.env_name = env_name
        self.checkpoint_dir = checkpoint_dir
        self.action_space = [i for i in range(n_actions)]
        self.learn_step_counter = 0

        self.memory = ReplayBuffer(mem_size, input_dims, n_actions)
        
        self.q_eval = DeepQNetwork(self.lr, self.n_actions, input_dims=self.input_dims,
                                    name = self.env_name+'_'+self.algo+'_q_eval', 
                                    checkpoint_dir=self.checkpoint_dir)

        self.q_next = DeepQNetwork(self.lr, self.n_actions, input_dims=self.input_dims,
                            name = self.env_name+'_'+self.algo+'_q_next', 
                            checkpoint_dir=self.checkpoint_dir)

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = T.tensor([observation], dtype=T.float).to(self.q_eval.device)
            actions = self.q_eval.forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)
        return action

    