"""Reproduce the original Section3.3 pure-state sphere illustration."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "mqc-bloch-sphere-3-3"
import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parents[1]
fig = plt.figure(figsize=(7.2,5.8),facecolor="white")
ax = fig.add_subplot(projection="3d")
u,v = np.meshgrid(np.linspace(0,2*np.pi,49),np.linspace(0,np.pi,25))
ax.plot_wireframe(np.cos(u)*np.sin(v),np.sin(u)*np.sin(v),np.cos(v),
                  rstride=3,cstride=4,color="#b8c5d5",linewidth=.5,alpha=.5)
for coordinate,label in enumerate(["x","y","z"]):
    endpoint = np.zeros(3);endpoint[coordinate]=1.26
    ax.quiver(0,0,0,*endpoint,color="#34445a",linewidth=1,arrow_length_ratio=.06)
    ax.text(*(endpoint*1.05),label,fontsize=12,color="#34445a")
ax.text(0,0,1.06,r"$|0\rangle$",fontsize=12)
ax.text(0,0,-1.17,r"$|1\rangle$",fontsize=12)
theta,phi = np.pi/3,np.pi/2
point = np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
ax.quiver(0,0,0,*point,color="#c45618",linewidth=2.5,arrow_length_ratio=.09)
ax.scatter(*point,color="#c45618",s=36,depthshade=False)
ax.text(*(point+np.array([-.12,.02,.12])),r"$\psi$",fontsize=12,color="#a64412")
t = np.linspace(0,theta,70)
ax.plot(.42*np.sin(t)*np.cos(phi),.42*np.sin(t)*np.sin(phi),.42*np.cos(t),color="#c45618",linewidth=1.8)
ax.text(.03,.24,.36,r"$\theta$",fontsize=13,color="#a64412")
f = np.linspace(0,phi,70)
ax.plot(.35*np.cos(f),.35*np.sin(f),0*f,color="#235e9b",linewidth=1.6)
ax.text(.28,.27,-.06,r"$\phi$",fontsize=13,color="#235e9b")
ax.plot([point[0],point[0]],[point[1],point[1]],[0,point[2]],linestyle="--",color="#c45618",alpha=.6)
ax.set(xlim=(-1.28,1.28),ylim=(-1.28,1.28),zlim=(-1.28,1.28))
ax.set_box_aspect((1,1,1),zoom=1.22);ax.view_init(elev=20,azim=28);ax.set_axis_off()
fig.suptitle("Pure qubit Bloch coordinates",fontsize=16,y=.96,color="#24364a")
fig.text(.5,.04,r"$\theta=\pi/3$, $\phi=\pi/2$:  $|\psi\rangle=(\sqrt{3}/2)|0\rangle+(i/2)|1\rangle$",ha="center",fontsize=12)
fig.subplots_adjust(left=0,right=1,bottom=.08,top=.92)
fig.savefig(root/'docs/assets/figures/bloch-pure-state.svg',bbox_inches="tight",metadata={"Date":None})
fig.savefig('/private/tmp/mqc-bloch-sphere-preview.png',dpi=170,bbox_inches="tight")
print('Saved original Bloch-sphere illustration.')
