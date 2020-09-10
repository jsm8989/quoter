import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import math
import itertools
import matplotlib.lines as mlines
import bltools as blt
from matplotlib.patches import Rectangle

q_list = np.linspace(0,1,20)
T = 10000
lam_list = [3,6,9]
z_list = [2,4,8]
trials_list = list(range(100))

# for z in z_list:
#     for lam in lam_list:
#         print(z,lam)
#         hx_all_q = np.zeros(len(q_list))
#         for i,q in enumerate(q_list):
#             hx_this_q = []
#             for trial in trials_list:
#                 efile = "../data_QMpaper-NEW/z%i_q%0.3f_T%i_lam%i_sim%i.txt" % (z,q,T,lam,trial)
#                 if os.path.isfile(efile):
#                     edata = pd.read_csv(efile, sep = " ")
#                     hx_this_q.extend(edata["hx"].values)
#             hx_all_q[i] = np.mean(hx_this_q)
       
#         df = pd.DataFrame({"q":q_list,"hx_avg":hx_all_q})
#         df.to_csv("QMpaper-NEW/z%i_lam%i_T%i.csv" % (z,lam,T), index=False)


z_style = ['x','s','o']
lam_color = ['C0','C1','C2']
linewidth = 2.5
ms = 4

fig,ax = plt.subplots(1,2,figsize=(8,4))
for t,TT in enumerate([1000,10000]):
    plt.sca(ax[t])

    for i,z in enumerate(z_list):
        for j,lam in enumerate(lam_list):
            data = pd.read_csv("QMpaper-NEW/z%i_lam%i_T%i.csv" % (z,lam,TT))
            plt.plot(data["q"].values,data["hx_avg"].values,z_style[i], c=lam_color[j], fillstyle="none", label=r"$z=%i,\lambda=%i$" % (z,lam))    

            T = TT*lam
            theory_L = [T/math.log(z) *  ( (1-q)*(math.log(T*z) - 1) +
                     q/2*(math.log(T*z**(lam+2))+(z**lam/T + 1)*math.log(T/z**lam + 1) - 2)) for q in q_list]
            theory_hx = [T*math.log(T,2)/L for L in theory_L]

            # only change Lambda_R
            theory_L2 = [T/math.log(z) *  ( (1-q)*(math.log(T*z) - 1 + np.euler_gamma - math.log(z)/2) +
                     q/2*(math.log(T*z**(lam+2))+(z**lam/T + 1)*math.log(T/z**lam + 1) - 2)) for q in q_list]
            theory_hx2 = [T*math.log(T,2)/L for L in theory_L2]



            # change Lambda_R and Lambda_Q
            # theory_L2 = [T/math.log(z) *  ( (1-q)*(math.log(T*z) - 1) +
            #          q/2*(math.log(T*z**(lam+2))+(z**lam/T + 1)*math.log(T/z**lam + 1) - 2)) + T*(np.euler_gamma/math.log(z) - 1/2) for q in q_list]
            # theory_hx2 = [T*math.log(T,2)/L for L in theory_L2]
        
            plt.plot(q_list, theory_hx, ':', c=lam_color[j], ms=ms)
            plt.plot(q_list, theory_hx2, '-', c=lam_color[j], linewidth=linewidth)

    # axcurr = plt.gca()
    # x0, x1 = axcurr.get_xlim()
    # y0, y1 = axcurr.get_ylim()
    # dx = x1 - x0
    # dy = y1 - y0
    # xlen = 0.25
    # xpad = 0.02
    # ypad = 0.02
    # axcurr.add_artist(Rectangle((x0+xpad*dx, y0+ypad*dy), xlen*dx, dy*(1-2*ypad), facecolor="none", ec="gray", lw=3.0))
    plt.xlabel(r"Quote probability, $q$",fontsize=14.5)    

plt.sca(ax[0])
# leg1 = plt.legend(loc="lower center", ncol=3, prop={'size': 9})
leg1 = plt.legend(loc="lower left", bbox_to_anchor=(0,0.08), ncol=3, prop={'size': 14.5})
# leg = plt.legend(title=r"$T=%i$" % TT, loc="lower left", bbox_to_anchor=(0,0.08), ncol=3, prop={'size': 8}))
leg1._legend_box.align = "left"
ax[0].add_artist(leg1)

theory1_line = mlines.Line2D([], [], color='k', ls=':',lw=linewidth)
theory2_line = mlines.Line2D([], [], color='k', ls='-',lw=linewidth)
plt.legend([theory1_line,theory2_line],["theory 1", "theory 2"],loc="upper right",prop={'size': 14.5})

# plt.ylabel(r"Cross-entropy, $h_\times$ [bits]",fontsize=14.5)
plt.ylabel(r"$h_\times$",fontsize=14.5)
# plt.savefig("C:/Users/tysonp/Desktop/Figure_1.pdf")

blt.letter_subplots(axes=ax, xoffset=0, yoffset=1.05)

plt.tight_layout(h_pad=0)
plt.show()



