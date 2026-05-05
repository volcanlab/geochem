import numpy as np
from typing import Union, List, Optional

def closure1(cn: Union[List[float], np.ndarray], k: float = 1.0) -> np.ndarray:
    """
    Inputs 
        cn is a composition (a list or a vector)
        k  is the constant sum of all components that we want
    Return
        a composition whose components sum to k
    """
    cn = np.asarray(cn, dtype=float)  #make sure cn is a numpy array
    s  = np.sum(cn)      #sum of components of c1
    
    #verify that cn is a true composition
    iscomposition = True
    if np.min(cn) < 0:
        iscomposition = False
    
    if iscomposition:
        res = cn * k / s
    else:
        raise ValueError(f"Error: the input vector {cn} is not a composition (contains negative values)")
    return res

def closure(c1: Union[List[float], np.ndarray], k: float = 1.0) -> np.ndarray:
    """
    x = closure(c1, k=1)
    
    Applies a closure constant, k, to compositions. 
    
    Input:
      c1 is a composition, a vector, or a matrix (Numpy array) of compositions in the rows. 
      If c1 is a matrix, the closure constant is applied to all the rows. 
    Return:
      x: a composition or matrix of compositions. Numpy array. 
    """
    ## Size of the data, numpy array
    N, D = 0, 0
    
    if isinstance(c1, np.ndarray):
        ls = len(c1.shape)
        if ls == 2:
            N, D = c1.shape
        else:
            D = c1.size 
    else:
        c1 = np.array(c1, dtype=float)
        D  = c1.size
    
    ## closure
    
    if N == 0:                 # vector
        x = closure1(c1, k)
        x = x.reshape(D)
    else:
        x = np.zeros((N,D))    # matrix
        for i in range(N):
            x[i,:] = closure1(c1[i,:], k)
        if N==1:
            x=x.reshape(D)
    return x

def geom(x: Union[List[float], np.ndarray]) -> float:
    """
    g = geom(x)
    
    g is the geometric mean of the vector x
    """
    x = np.asarray(x, dtype=np.float64)  
    g = np.exp(np.mean(np.log(x))) #equivalent
    return g

def centrec(X: np.ndarray) -> np.ndarray:
    """
    c = centrec(X)
    
    c is the center (centre) of the set of compositional data in Numpy array X,
      with n rows (samples) and D columns (components)
    c is a composition with same closure as the samples in X
    """
    _, D = X.shape 
    c = np.zeros(D)
    
    for i in range(D):
        c[i] = geom(X[:,i])
        
    c = closure(c, X[0,:].sum())
    
    return c.reshape(1, c.size)

def pertur(c1: Union[List[float], np.ndarray], c2: Union[List[float], np.ndarray], k: Optional[float] = None) -> np.ndarray:
    """
    x = pertur(c1, c2, k=None)

    Positive perturbation of compositions in c1 with composition c2. 
    Compositions in c1 and c2 share the same closure constant
    
    Input
      c1 is a composition (list or 1D numpy array) or a 2D numpy array with
        compositions in the rows
      c2 is a composition (list or 1D numpy array)
      k closure constant. if None it uses the closure constant of c2
    Returns:
      x composition(s) from positive perturbation of c1 with c2 (and closure)
    """
    def pertur1(a1: np.ndarray, a2: np.ndarray, k: Optional[float] = None) -> np.ndarray:
        """
        Inputs
          a1 and a2, two compositions (lists or numpy arrays)
          k closure constant. if None it uses the closure constant of a1
        Returns:
          a composition from positive perturbation of a1 with a2 (and closure)
        """
        a1 = np.asarray(a1, dtype=float)
        a2 = np.asarray(a2, dtype=float)
        
        if k is None:
            k = float(a1.sum())
        res = a1.reshape(1, a1.size) * a2.reshape(1, a2.size)
        
        return closure(res, k)

    ## Size of the data, numpy array
    N, D = 0, 0
    
    if isinstance(c1, np.ndarray):
        ls = len(c1.shape)
        if ls == 2:
            N, D = c1.shape
        else:
            D = c1.size 
    else:
        c1 = np.array(c1, dtype=float)
        D  = c1.size
    
    c2 = np.asarray(c2, dtype=float)
    
    ## Perturbation
    
    if N == 0:               #vector
        x = pertur1(c1, c2, k)
    else:
        x = np.zeros((N, D))  #matrix
        for i in range(N):
            x[i,:] = pertur1(c1[i,:], c2, k)
        if N==1:
            x=x.reshape(D)
    return x

def power(c1: Union[List[float], np.ndarray], p: float = 1.0, k: Optional[float] = None) -> np.ndarray:
    """
    x = power(c1, p=1, k=None)
    
    Applies the power operation to compositions. 
    
    Inputs
      c1: composition, a vector or a matrix (Numpy array) of compositions in the rows.
      p:  scale number or powering factor
      k:  closure constant, if None it becomes the sum of c1
    
    Return
      x composition or matrix of compositions. Numpy array.
    """
    def power1(cn: np.ndarray, p: float = 1.0, k: Optional[float] = None) -> np.ndarray:
        """
        Inputs
          cn: composition
          p:  scale number or powering factor
          k:  closure constant, if None it becomes the sum of c1
        Return: a composition 
        """
        cn = np.asarray(cn, dtype=float)
        if k is None:
            k = float(cn.sum())
        return closure(cn**p, k)

    ## Size of the data, numpy array
    N, D = 0, 0
    
    if isinstance(c1, np.ndarray):
        ls = len(c1.shape)
        if ls == 2:
            N, D = c1.shape
        else:
            D = c1.size 
    else:
        c1 = np.array(c1, dtype=float)
        D  = c1.size
    
    ## powering
    
    if N == 0:               #vector
        x = power1(c1, p, k)
    else:
        x = np.zeros((N, D))  #matrix
        for i in range(N):
            x[i,:] = power1(c1[i,:], p, k)
        if N==1:
            x=x.reshape(D)
    return x

def alr(c1: Union[List[float], np.ndarray], ind: int = 0) -> np.ndarray:
    """
    x = alr(c1, ind=0)
    
    Input:
      c1   composition, a vector or a matrix (Numpy array) of compositions in the rows.
      ind  is the index number of the denominator in the log-ratio
    Return:
      x is the aditive log-ratio transform of c1 (vector or matrix)
    """
    def alr1(cn: np.ndarray, ind: int = 0) -> np.ndarray:
        """
        Inputs
          cn   is a composition
          ind  is the index number of the denominator in the log-ratio
        Return
          the aditive log-ratio transform of c1
        """
        cn = np.asarray(cn, dtype=float)
        
        cn = np.log(cn/cn[ind])
        cn = np.delete(cn, ind)
            
        return cn.reshape(1, cn.size)

    ## Size of the data, numpy array
    N, D = 0, 0
    
    if isinstance(c1, np.ndarray):
        ls = len(c1.shape)
        if ls == 2:
            N, D = c1.shape
        else:
            D = c1.size 
    else:
        c1 = np.array(c1, dtype=float)
        D  = c1.size
    
    ## alr
    
    if N == 0:                 # vector
        x = alr1(c1, ind)
    else:
        x = np.zeros((N, D-1))    # matrix
        for i in range(N):
            x[i,:] = alr1(c1[i,:], ind)
        if N==1:
            x=x.reshape(D-1)
    return x

def clr(c1: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    x = clr(c1)
    
    Input:
      c1 composition, a vector or a matrix (Numpy array) of compositions in the rows.
    Return:
      x is the center log-ratio transform of c1 (vector or matrix)
    """
    def clr1(cn: np.ndarray) -> np.ndarray:
        """
        Input: cn is a composition
        Return: the center log-ratio transform of cn
        """
        cn = np.asarray(cn, dtype=float)
        gm = geom(cn)
        
        cn  = np.log(cn/gm)    
        return cn.reshape(1, cn.size)

    ## Size of the data, numpy array
    N, D = 0, 0
    
    if isinstance(c1, np.ndarray):
        ls = len(c1.shape)
        if ls == 2:
            N, D = c1.shape
        else:
            D = c1.size 
    else:
        c1 = np.array(c1, dtype=float)
        D  = c1.size
    
    ## clr
    
    if N == 0:                 # vector
        x = clr1(c1)
    else:
        x = np.zeros((N, D))    # matrix
        for i in range(N):
            x[i,:] = clr1(c1[i,:])
        if N==1:
            x=x.reshape(D)
    return x
