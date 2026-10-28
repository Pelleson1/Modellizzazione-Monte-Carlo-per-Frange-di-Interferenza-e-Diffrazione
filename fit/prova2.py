import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2 

def E(x, alpha):
    return  np.sinc(alpha*x/np.pi)**2

def C(x, delta):
    return np.cos(delta*x)**2

def mu(x, B, I, alpha, delta):
    return B + I*E(x, alpha)*C(x, delta)

data = np.genfromtxt(
"data.csv",
delimiter=",",
names=True
)

x = data["x"]
y = data["y"]
sigma_y = data["sigma_y"]

def size_comparison (data):
    return (len(data["x"])==len(data["y"]) and len(data["y"])==len(data["sigma_y"]))


print("\n==============================================================")
print("Compatibilità lunghezza dei dati: ",size_comparison(data))
print("Numero di conteggi: ", np.floor(np.sum(y)))
print("Intervallo di x : ", abs(x[0]-x[-1]), '\n')

B0 = (y[0] + y[-1])/2
I0 = np.max(y) - B0
delta0 = np.pi/0.6
alpha0 = np.pi/3.5

lower = [0.0, 0.0, 0.10, 1]
upper = [np.inf, np.inf, 3.0, 12.0]
p0 = [B0, I0, alpha0, delta0]

print(f"Parametri iniziali: B0={float(p0[0]):.4f}, I0={float(p0[1]):.4f}, alpha0={float(p0[2]):.4f}, delta0={float(p0[3]):.4f}")
print(f"Lower bounds: B0_inf={float(lower[0]):.4f}, I0_inf={float(lower[1]):.4f}, alpha0_inf={float(lower[2]):.4f}, delta0_inf={float(lower[3]):.4f}")
print(f"Upper bounds: B0_sup={float(upper[0]):.4f}, I0_sup={float(upper[1]):.4f}, alpha0_sup={float(upper[2]):.4f}, delta0_sup={float(upper[3]):.4f}\n")

popt, pcov = curve_fit(
mu, x, y,
p0=p0,
sigma=sigma_y,
absolute_sigma=True,
bounds=(lower, upper),
maxfev=10000000
)

B_hat = popt[0]
I_hat = popt[1]
alpha_hat = popt[2]
delta_hat = popt[3]

sigma_y_hat = np.sqrt(np.diagonal(pcov))

den = np.sqrt(np.outer(np.diagonal(pcov),np.diagonal(pcov)))
corr = pcov / den
print("Parametro B stimato: ",f"{B_hat:.4f}", " +/- ",f"{sigma_y_hat[0]:.4f}")
print("Parametro I stimato: ",f"{I_hat:.4f}", " +/- ",f"{sigma_y_hat[1]:.4f}")
print("Parametro alpha stimato: ",f"{alpha_hat:.4f}", " +/- ",f"{sigma_y_hat[2]:.4f}")
print("Parametro delta stimato: ",f"{delta_hat:.4f}", " +/- ",f"{sigma_y_hat[3]:.4f}\n")

layout = """
AC
BC
"""

fig, axes = plt.subplot_mosaic(layout, figsize=(10.5, 7.8))
axes['A'].scatter(x, y, color="tab:red", label="data")
axes['A'].errorbar(x, y, sigma_y, fmt='o', color="tab:red")
axes['A'].grid(True)
axes['A'].legend()
axes['A'].plot(x, mu(x, B_hat, I_hat, alpha_hat, delta_hat), color="tab:green", label="fit")

im = axes['C'].imshow(corr, vmin=-1, vmax=1, cmap="plasma")
fig.colorbar(im, ax=axes['C'], fraction=0.046, shrink=1.0, label="correlazione")
axes['C'].set_xticks([0, 1, 2, 3], ["B", "I", "alpha", "delta"])
axes['C'].set_yticks([0, 1, 2, 3], ["B", "I", "alpha", "delta"])
axes['C'].set_title("Matrice di correlazione dei parametri")

res = data["y"] - mu(x, B_hat, I_hat, alpha_hat, delta_hat)
pull = res / sigma_y
chi2_obs = np.sum(pull**2)
dof = len(data) - len(p0)
chi2_red_obs = chi2_obs / dof

p_value = chi2.sf(chi2_obs, dof)

axes['B'].axhline(0, color="red", linestyle="--", linewidth=2, label="Media simulata")
#axes[1, 0].set_ylim(-2, 2)
axes['B'].grid(True)
axes['B'].scatter(x, pull, label="pull")
axes['B'].legend()

print(f"Chi2_red_obs = {float(chi2_red_obs):.4f}")
print(f"p value = {float(p_value):.4f}")
print("==============================================================\n")

plt.tight_layout()
plt.show()