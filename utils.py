import numpy as np

#Usamos el método de Euler para resolver las ecuaciones acopladas
def solve(n,h,fx,fy,x0,y0,t0,res):
    
    x = np.zeros(shape=(n,res*res))
    y = np.zeros(shape=(n,res*res))
    x[0] = x0
    y[0] = y0
    t = [t0]
    for i in range(n-1):
        t.append(t[i]+h)
        x[i+1]=x[i]+h*fx(x[i],y[i],t[i])
        y[i+1]=y[i]+h*fy(x[i],y[i],t[i])
    return x,y,t