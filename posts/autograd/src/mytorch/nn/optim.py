import numpy as np

class SGD:
    def __init__(self, params, lr=1e-3, reg=0) -> None:
        ''' 
        @param params (list): The list of all Parameter tensors to be updated, usually set to module.parameters().
        @param lr (float): Learning rate.
        @param reg (float): Regularization scalar (Controling L2 regularization strength).
        '''
        self.params = params
        self.lr = lr
        self.reg = reg
        

    def step(self):
        ''' Updates all parameters in self.params. '''
        for param in self.params:
            param.data = param.data - (self.lr * param.grad) - (self.lr * self.reg * param.data)

    def zero_grad(self):
        ''' Sets all the gradients of self.params to zero. '''
        for param in self.params:
            param.zero_grad()

class Adam:
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.99), eps=1e-8, reg=0) -> None:
        '''
        @param params (list): The list of all Parameter tensors to be updated, usually set to module.parameters().
        @param lr (float): Learning rate.
        @param betas (tuple): two scalar floats controling how slowly the optimizer changes the "m" and "v" attributes.
        @param eps (float): scalar added to denominator to stop it from ever going to zero.
        @param reg (float): scalar controling strength l2 regularization.
        '''
        self.params = params
        self.lr = lr
        self.reg = reg
        self.b1 = betas[0]
        self.b2 = betas[1]
        self.eps = eps
        self.reg = reg
        for param in self.params:   # Create new "m" and "v" attributes and init to zero (which is actually biased at the start of training, but yeah)
            param.m = np.zeros(param.shape)
            param.v = np.zeros(param.shape)

    def step(self):
        ''' Updates all parameters in self.params. '''
        for param in self.params:
            param.m = (param.m * self.b1 + (1 - self.b1) * param.grad) 
            param.v = (param.v * self.b2 + (1 - self.b2) * np.square(param.grad))

            param.data = param.data - (self.lr * param.m) / (np.sqrt(param.v) + self.eps) - self.reg * self.lr * param.data

    def zero_grad(self):
        ''' Sets all the gradients of self.params to zero. '''
        for param in self.params:
            param.zero_grad()