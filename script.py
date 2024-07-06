import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation,FFMpegWriter,writers
import argparse
from utils import solve

def create_lambda_with_globals(s):
    return eval("lambda x,y,t:"+s,globals())


parser = argparse.ArgumentParser()
parser.add_argument("-v","--video",type=str,default="")
parser.add_argument("-x","--fx",type=str,default="np.cos(y)")
parser.add_argument("-y","--fy",type=str,default="np.sin(x)")
parser.add_argument("-s","--fps",type=int,default=32)
parser.add_argument("-i","--ti",type=float,default=0)
parser.add_argument("-t","--tf",type=float,default=1)
parser.add_argument("-n","--n_time_steps",type=int,default=100)
parser.add_argument("-p","--n_points",type=int,default=9)
parser.add_argument("-m","--space_min",type=float,default=-5)
parser.add_argument("-M","--space_max",type=float,default=5)
args = parser.parse_args()

video_name=args.video
dx = create_lambda_with_globals(args.fx)
dy = create_lambda_with_globals(args.fy)
fps_v = args.fps
t0 = args.ti
t1 = args.tf
n = args.n_time_steps


#Definimos las coordenadas iniciales para las variables
res = args.n_points

smin = args.space_min
smax = args.space_max

pmin = args.space_min
pmax = args.space_max

p0 = np.linspace(pmin,pmax,res)
p1 = np.linspace(pmin,pmax,res)

#Espacio de puntos incial
x0,y0 = np.meshgrid(p0,p1)

#Para graficar el campo vectorial
xv,yv = x0,y0
vdx = dx(xv,yv,0)
vdy = dy(xv,yv,0)


x0 = x0.reshape(-1)
y0 = y0.reshape(-1)

h = (t1-t0)/n

x,y,t = solve(n,h,dx,dy,x0,y0,t0,res)

size_scat = 10
print("Iniciando graficacion")
plt.style.use("dark_background")
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot()
ax.axis("off")
def animate(i):
    if i%10==0 and not video_name=="":
        print("{}%".format(100*i/n))
    ax.clear()
    ax.axis("off")
    ax.set_xlim(smin,smax)
    ax.set_ylim(smin,smax)
    ax.quiver(xv,yv,vdx,vdy,color="steelblue",alpha=0.3)
    for k in range(res*res):
        ax.plot(x[:i+1,k],y[:i+1,k],c="skyblue",linewidth=0.5,alpha=0.8)
        ax.scatter(x[i,k],y[i,k],c="deepskyblue",s=size_scat)
func = FuncAnimation(fig,animate,frames=n,interval=0.1)
if not video_name=="":
    ffmpeg_writer = writers['ffmpeg']
    writer = ffmpeg_writer(fps=fps_v, codec='mpeg4')

    # Guardar la animación como archivo MP4
    func.save(video_name, writer=writer,dpi=350)
else:
    plt.show()
