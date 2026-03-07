from __future__ import annotations
from typing import Optional
import numpy as np

class Tensor:
    def __init__(self, data: np.ndarray, requires_grad=False, operation=None):
        # Payload
        self.data = data
        # Metadata
        self.requires_grad = requires_grad
        if self.requires_grad:
            self.grad = np.zeros_like(data, dtype=np.float32)
        self.operation = operation  # What operation cls created this tensor
        self.children = []          # What other tensors are created from this tensor

    # This method is called by the operation backward()
    def backward(self, 
                 grad_: Optional[np.ndarray] = None,    # The downstream operator pass this gradient for you
                 z: Optional[Tensor] = None):           # Which child tensor is passing the gradient
        if not self.requires_grad:
            return "Cannot backpropagate on a tensor that does not require gradients."
        
        if grad_ is None:           # Called only the first time from loss.backward()
            grad_ = np.ones_like(self.data, dtype=np.float32)   # Set a tiny nudge of ones
            
        self.grad += grad_          # Aggregate gradients from that children (but possibly not all yet)
        
        if z is not None:           # NOT called only the first time
            self.children.remove(z) # I heard the gradient from you, no need to wait for you anymore
        
        if self.operation:
            if not self.children:   # Received grad_ from all children, ready to pass grad upstream
                self.operation.backward(self.grad, self)

    def zero_grad(self):
        ''' Sets the gradient of this tensor to zero. '''
        if self.requires_grad:
            self.grad = np.zeros_like(self.data)
            
    # Some basic operators, more operators must be called via their classes below
    def __add__(self, other: Tensor) -> Tensor:
        op = Add()
        return op.forward(self, other)

    def __neg__(self) -> Tensor:
        op = Neg()
        return op.forward(self)

    def __sub__(self, other: Tensor) -> Tensor:
        return self + (-other)
    
    def __mul__(self, other: Tensor) -> Tensor:
        op = Mul()
        return op.forward(self, other)
    
# Paramaters are exact the same as Tensors except they always require gradients to be updated.
class Parameter(Tensor):
    ''' Subclass of Tensor which always tracks gradients. '''
    def __init__(self, data, requires_grad = True, operation = None) -> None:
        super().__init__(data, requires_grad=requires_grad, operation=operation)


# These are just operators
class Add:
    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        # Record which two tensors were added
        self.parents = (a, b)
        
        # Create result tensor z
        requires_grad = a.requires_grad or b.requires_grad
        data = a.data + b.data
        z = Tensor(data, requires_grad=requires_grad, operation=self) 
        
        # Side effects to a, b
        a.children.append(z)
        b.children.append(z)

        return z
        
    def backward(self, dz: np.ndarray, z: Tensor):
        a, b = self.parents
        
        if a.requires_grad:
            da_ = dz
            a.backward(da_, z)
        if b.requires_grad:
            db_ = dz
            b.backward(db_, z)

class Neg:
    def forward(self, a: Tensor) -> Tensor:
        # Record which tensor was negated
        self.parent = a
        
        # Create result tensor z
        requires_grad = a.requires_grad
        data = -a.data
        z = Tensor(data, requires_grad=requires_grad, operation=self) 
        
        # Side effects to a
        a.children.append(z)

        return z
        
    def backward(self, dz: np.ndarray, z: Tensor):
        a = self.parent
        
        if a.requires_grad:
            da_ = -dz
            a.backward(da_, z)

class Mul:
    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        # Record which two tensors were multiplied
        self.parents = (a, b)
        
        # Create result tensor z
        requires_grad = a.requires_grad or b.requires_grad
        data = a.data * b.data
        z = Tensor(data, requires_grad=requires_grad, operation=self) 
        
        # Side effects to a, b
        a.children.append(z)
        b.children.append(z)

        return z
        
    def backward(self, dz: np.ndarray, z: Tensor):
        a, b = self.parents
        
        if a.requires_grad:
            da_ = dz * b.data
            a.backward(da_, z)
        if b.requires_grad:
            db_ = dz * a.data
            b.backward(db_, z)
            
class Exp:
    def forward(self, a: Tensor) -> Tensor:
        # Record which tensor was exponentiated
        self.parent = a
        
        # Create result tensor z
        requires_grad = a.requires_grad
        data = np.exp(a.data)
        z = Tensor(data, requires_grad=requires_grad, operation=self) 
        
        # Side effects to a
        a.children.append(z)

        return z
        
    def backward(self, dz: np.ndarray, z: Tensor):
        a = self.parent
        
        if a.requires_grad:
            da_ = dz * z.data   # since d(exp(a))/da = exp(a)
            a.backward(da_, z)
            
class Log:
    def forward(self, a: Tensor) -> Tensor:
        # Record which tensor was logged
        self.parent = a
        
        # Create result tensor z
        requires_grad = a.requires_grad
        data = np.log(a.data)
        z = Tensor(data, requires_grad=requires_grad, operation=self) 
        
        # Side effects to a
        a.children.append(z)

        return z
        
    def backward(self, dz: np.ndarray, z: Tensor):
        a = self.parent
        
        if a.requires_grad:
            da_ = dz / a.data   # since d(log(a))/da = 1/a
            a.backward(da_, z)