from ..tensor import *

class Module:
    ''' General Module superclass'''
    def __init__(self):
        pass

    def __call__(self, x):
        return self.forward(x)

    def parameters(self):
        '''
        Look inside all layers (which are subclasses of Module) and return all parameter tensors in a list.
        @returns params (list): A list of parameter tensors in the model.
        '''
        params = []
        for _, param in self.__dict__.items():
            if isinstance(param, Module):
                params += param.parameters()    # Usually called the first time, but probably not here second time
            elif isinstance(param, Parameter):
                params.append(param)            # If it's a Parameter, add it to the list
            elif isinstance(param, Tensor):
                if param.requires_grad:
                    params.append(param)        # Tensors with requires_grad = True are also parameters
        return params


    def train(self):
        ''' Sets module's mode to train (Do NOT mean implement training!), which influences layers like Dropout (Not implemented in this demo)'''
        self.mode = 'train'
        for _, param in self.__dict__.items():
            if isinstance(param, Module):
                param.train()

    def eval(self):
        ''' Sets module's mode to inference, which influences layers like Dropout (Not implemented in this demo)'''
        self.mode = 'eval'
        for _, param in self.__dict__.items():
            if isinstance(param, Module):
                param.eval()

class Linear(Module):
    def __init__(self, in_size: int = 1, out_size: int = 1, bias: bool = True):
        '''
        @param in_size (int): size of the last dimention of the input array (only support 1 in this demo).
        @param out_size (int): size of the last dimention of the output array (only support 1 in this demo).
        @param bias (bool): whether to include a bias term.
        '''
        super().__init__()
        self.W = Tensor(np.random.randn(in_size, out_size) / np.sqrt(in_size), requires_grad=True)
        self.b = Tensor(np.zeros(out_size), requires_grad=True)
        self.has_bias = bias

    def forward(self, x):
        z = x * self.W 
        if self.has_bias:
            z += self.b
        return z


class ReLU(Module):
    def __init__(self):
        super().__init__()

    def forward(self, z):
        mask = Tensor(np.where(z.data < 0, 0, 1))
        z = z * mask
        return z


class MSELoss(Module):
    def __init__(self):
        super().__init__()

    def forward(self, y_pred, y_true):
        return ((y_pred - y_true) ** 2).mean()