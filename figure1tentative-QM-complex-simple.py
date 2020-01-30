import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dir1 = "ER_BA_N1000/processing"
dir2 = "Lewis_sims"
ER = pd.read_csv(f"{dir1}/hx_ER.csv")
BA = pd.read_csv(f"{dir1}/hx_BA.csv")
N = 1000
BAdeg = np.array([2*m - 2*m**2/N for m in BA["m"].values]) # theoretical degree for BA

fig,ax = plt.subplots(2,3,figsize=(8,5))

# average cross-entropy vs average degree
plt.sca(ax[0,0])
Ier_ = ER["k"].values <= 40
#plt.plot(ER["k"].values[I_], ER["hx_avg"].values - ER["h_avg"].values,'ko', label="ER") 
plt.plot(ER["k"].values[Ier_], ER["hx_avg"].values[Ier_],'ko-', label="ER") 
Iba_ = BAdeg <= 40
#plt.plot(BAdeg[I_], BA["hx_avg"].values - BA["h_avg"].values, 'ro', label="BA")
plt.plot(BAdeg[Iba_], BA["hx_avg"].values[Iba_], 'ro-', label="BA")
plt.xlabel(r"Average degree, $\langle k \rangle$")
#plt.ylabel(r"KL-divergence, $\langle h_\times - h \rangle$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.legend()
plt.title("Quoter Model")

# variance of cross-entropy vs average degree
plt.sca(ax[1,0])
plt.plot(ER["k"].values[Ier_], np.power(ER["hx_std"].values[Ier_], 2), 'ko-', label="ER")
plt.plot(BAdeg[Iba_], np.power(BA["hx_std"].values[Iba_], 2), 'ro-', label="BA")
plt.xlabel(r"Average degree, $\langle k \rangle$")
plt.ylabel(r"Variance of $h_\times$")

ER_simple_peak_size_m = pd.read_csv(f'{dir2}/ER_simple_peak_size_m.csv')
ER_simple_peak_size_var = pd.read_csv(f'{dir2}/ER_simple_peak_size_var.csv')
BA_simple_peak_size_m = pd.read_csv(f'{dir2}/BA_simple_peak_size_m.csv')
BA_simple_peak_size_var = pd.read_csv(f'{dir2}/BA_simple_peak_size_var.csv')
ER_complex_peak_size_m = pd.read_csv(f'{dir2}/ER_complex_peak_size_m.csv')
ER_complex_peak_size_var = pd.read_csv(f'{dir2}/ER_complex_peak_size_var.csv')
BA_complex_peak_size_m = pd.read_csv(f'{dir2}/BA_complex_peak_size_m.csv')
BA_complex_peak_size_var = pd.read_csv(f'{dir2}/BA_complex_peak_size_var.csv')


# LEWIS
plt.sca(ax[0,1])
plt.plot(ER_simple_peak_size_m['k'],ER_simple_peak_size_m['peak_size'],'k-o')
plt.plot(BA_simple_peak_size_m['m'],BA_simple_peak_size_m['peak_size'],'r-o')
plt.ylabel('Average peak size')
plt.title("Simple Contagion")

plt.sca(ax[1,1])
plt.plot(ER_simple_peak_size_var['k'],ER_simple_peak_size_var['peak_size'],'k-o',label='Erdos-Renyi')
plt.plot(BA_simple_peak_size_var['m'],BA_simple_peak_size_var['peak_size'],'r-o',label='Barabasi-Albert')
plt.ylabel('Variance of peak size')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.sca(ax[0,2])
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

plt.sca(ax[1,2])
plt.plot(ER_complex_peak_size_var['k'],ER_complex_peak_size_var['peak_size'],'k-o')
plt.plot(BA_complex_peak_size_var['m'],BA_complex_peak_size_var['peak_size'],'r-o')
plt.axvline(14,linestyle="--",color="C0")
plt.ylabel('Variance of peak size')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel(r'$\langle k \rangle$')

plt.tight_layout()
plt.savefig('simple_complex_sims.pdf')
plt.show()




    
