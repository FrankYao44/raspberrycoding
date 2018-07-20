#import logging
#import pdb
#logging.basicConfig(level=logging.INFO)
def calculate(n,L=[1,1]):
    '''
    this is a function which is able to return a iterator which for the List b
    >>> m=calculate(3)
    >>> next(m)
    [1, 2, 1]
    >>> next(m)
    Traceback (most recent call last):
        ...
    StopIteration
    
    '''
    for b in range(1,n-1): 
      #  logging.info("n=%d"%n)
        M=[L[a]+L[a+1]  for a in range(b)]
   #     pdb.set_trace()
        L=[1]+M+[1]
        #logging.info("L=%s"%L)
        yield L
def pasical(n):
    """
    this is main function to output pasical numbers
    >>> pasical(1)
    [1]
    >>> pasical(2)
    [1, 1]
    >>> pasical(3)
    [1, 2, 1]
    >>> pasical("q")
    Traceback (most recent call last):
    ...
    ValueError


    """  
    if  not isinstance(n,int):
        raise ValueError
    if n==1:
        return [1]        
    elif n==2:
        return [1,1]
    m=list(calculate(n))
    m=[[1]]+[[1,1]]+m
    #logging.info("m=%s"%m)
    return m[n-1]
if __name__=="__main__":
    import doctest
    doctest.testmod()
    print(pasical(30))
    


