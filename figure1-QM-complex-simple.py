import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bltools as blt
from scipy import stats, linalg
from scipy.optimize import fsolve
import math
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def get_predictability(S,N): # explodes for small values of N or large values of S
    try:
        PiMax = fsolve(lambda Pi : S + Pi*math.log(Pi,2) + (1 - Pi)*math.log(1 - Pi,2) - (1 - Pi)*math.log(N-1,2), 0.5)
    except:
        PiMax = 1
    return float(PiMax)

dir1 = "ER_BA_N1000/processing"
dir2 = "Lewis_sims"

fig,ax = plt.subplots(1,3,figsize=(8,3),constrained_layout=True)

# LEWIS et al: simple & complex contagion 
ER_simple_peak_size_m = pd.read_csv(f'{dir2}/ER_simple_peak_size_m.csv')
ER_simple_peak_size_var = pd.read_csv(f'{dir2}/ER_simple_peak_size_var.csv')
BA_simple_peak_size_m = pd.read_csv(f'{dir2}/BA_simple_peak_size_m.csv')
BA_simple_peak_size_var = pd.read_csv(f'{dir2}/BA_simple_peak_size_var.csv')
ER_complex_peak_size_m = pd.read_csv(f'{dir2}/ER_complex_peak_size_m.csv')
ER_complex_peak_size_var = pd.read_csv(f'{dir2}/ER_complex_peak_size_var.csv')
BA_complex_peak_size_m = pd.read_csv(f'{dir2}/BA_complex_peak_size_m.csv')
BA_complex_peak_size_var = pd.read_csv(f'{dir2}/BA_complex_peak_size_var.csv')

plt.sca(ax[0])
plt.plot(ER_simple_peak_size_m['k'],ER_simple_peak_size_m['peak_size'],'k-o',label="ER")
plt.plot(BA_simple_peak_size_m['m'],BA_simple_peak_size_m['peak_size'],'r-o',label="BA")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel('Average peak size')
plt.title("Simple Contagion")
plt.legend()

plt.sca(ax[1])
peak_index_ER = np.argmax(ER_complex_peak_size_m['peak_size'].values)
peak_k_ER = ER_complex_peak_size_m["k"].values[peak_index_ER]
peak_index_BA = np.argmax(BA_complex_peak_size_m['peak_size'].values)
peak_k_BA = BA_complex_peak_size_m["m"].values[peak_index_BA]

plt.plot(ER_complex_peak_size_m['k'],ER_complex_peak_size_m['peak_size'],'k-o')
plt.plot(BA_complex_peak_size_m['m'],BA_complex_peak_size_m['peak_size'],'r-o')
##plt.axvline(peak_k_ER,linestyle="--",color="k")
##plt.axvline(peak_k_BA,linestyle="--",color="r")
plt.axvline(14,linestyle="--",color="C0")
plt.ylabel('Average peak size')
plt.xlabel(r'$\langle k \rangle$')
plt.title("Complex Contagion")


# QUOTER MODEL
ER = pd.read_csv(f"{dir1}/hx_ER.csv")
BA = pd.read_csv(f"{dir1}/hx_BA.csv")
N = 1000
BAdeg = np.array([2*m - 2*m**2/N for m in BA["m"].values]) # theoretical degree for BA

# average predictability vs average degree
plt.sca(ax[2])
Ier_ = ER["k"].values <= 40
ERpred = [get_predictability(s,1000) for s in ER["hx_avg"].values[Ier_]]
plt.plot(ER["k"].values[Ier_], ERpred,'ko-', label="ER") 
Iba_ = BAdeg <= 40
BApred = [get_predictability(s,1000) for s in BA["hx_avg"].values[Iba_]]
plt.plot(BAdeg[Iba_], BApred, 'ro-', label="BA")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"Average predictability, $\Pi$")
plt.title("Quoter Model")

# inset. average hx vs average degree
axcurr = plt.gca()
dd = 0.02
dx,dy = -0.195+dd, 0.26+dd
a = 1.3
wi,hi = a*0.4-dd,a*0.4*0.8-dd
axins = inset_axes(axcurr, width="100%", height="100%",
                   bbox_to_anchor=(.65+dx, .3+dy, wi,hi),
                   bbox_transform=axcurr.transAxes, loc="center")
plt.plot(ER["k"].values[Ier_], ER["hx_avg"].values[Ier_], "ko-")
plt.plot(BAdeg[Iba_], BA["hx_avg"].values[Iba_], "ro-")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"$\langle h_\times \rangle$")

blt.letter_subplots(axes=ax.flatten(), xoffset=-.1, yoffset=1.05)
##plt.tight_layout()
plt.savefig('figure1-QM-complex-simple.pdf')
plt.show()




    
