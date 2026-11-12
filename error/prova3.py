import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def Cov_matrix(corrs, vars):
    A = np.zeros((4, 4))
    j=0
    idx = 0
    for n in range (0,2, 1):
        for i in range (j+1, 4, 1):
            A[n, i] = corrs[idx] * np.sqrt(vars[n] * vars[i]) 
            idx += 1
        j+=1
    A = A + A.T + np.diag(vars)
    return A 
def g(z):
    a = z[0]/(z[2]*z[3])
    d = z[1]/(z[2]*z[3])
    q = d/a
    return [a, d, q]
def J(z):
    J = np.array([
        [1 / (z[2] * z[3]),      0.0,           -z[0] / (z[2]**2 * z[3]), -z[0] / (z[2] * z[3]**2)],
        [0.0,               1 / (z[2] * z[3]),  -z[1] / (z[2]**2 * z[3]), -z[1] / (z[2] * z[3]**2)],
        [-z[1] / z[0]**2, 1 / z[0],      0.0,                  0.0]
    ], dtype=float)
    return J

alpha = 0.9001
sigma_alfa = 0.0002
delta = 5.1998
sigma_delta = 0.0001

k = 1
sx = 1
sigma_k = 0.01
sigma_sx = 0.01

corr_alpha_delta = 4.56453526e-04
corr_alpha_k = 0
corr_alpha_sx = 0
corr_delta_k = 0
corr_delta_sx = 0
corr_k_sx = 0

corrs = [corr_alpha_delta, corr_alpha_k, corr_alpha_sx, corr_delta_k, corr_delta_sx, corr_k_sx]
vars = [sigma_alfa ** 2, sigma_delta ** 2, sigma_k ** 2, sigma_sx ** 2]

z = [alpha, delta, k, sx]

C_z = Cov_matrix(corrs, vars)
J = J(z)
eigvals = np.linalg.eigvalsh(C_z)

den = np.sqrt(np.outer(np.diagonal(C_z),np.diagonal(C_z)))
corr = C_z / den

C_g = J @ C_z @ J.T
var = np.sqrt(np.diag(C_g))
print("a = ", g(z)[0], " +/- ", var[0])
print("d = ", g(z)[1], " +/- ", var[1])
print("q = ", g(z)[2], " +/- ", var[2])

print (corr)
print ("autovalori = ", eigvals)





media_input = np.array([alpha, delta, k, sx])

rng = np.random.default_rng(20261003)
campioni = rng.multivariate_normal(
mean=media_input,
cov=C_z,
size=100_000
)

alpha_mc = campioni[:, 0]
delta_mc = campioni[:, 1]
k_mc = campioni[:, 2]
sx_mc = campioni[:, 3]

a_mc = alpha_mc/(k_mc * sx_mc)
d_mc = delta_mc/(k_mc * sx_mc)



alpha_hat = np.mean(alpha_mc)
delta_hat = np.mean(delta_mc)
k_hat = np.mean(k_mc)
sx_hat = np.mean(sx_mc)

sigma_alpha_hat = np.std(alpha_mc, ddof=1)
sigma_delta_hat = np.std(delta_mc, ddof=1)
sigma_k_hat = np.std(k_mc, ddof=1)
sigma_sx_hat = np.std(sx_mc, ddof=1)

alpha_median = np.median(alpha_mc)
delta_median = np.median(delta_mc)
k_median = np.median(k_mc)
sx_median = np.median(sx_mc)

p16_alpha, p84_alpha = np.percentile(alpha_mc, [16, 84])
p16_delta, p84_delta = np.percentile(delta_mc, [16, 84])
p16_k, p84_k = np.percentile(k_mc, [16, 84])
p16_sx, p84_sx = np.percentile(sx_mc, [16, 84])

layout = """
AC
BC
"""

counts, xedges, yedges, image = plt.hist2d(a_mc, d_mc, bins=100000, cmap='viridis')

fig, axes = plt.subplot_mosaic(layout, figsize=(10.5, 7.8))
im = axes['C'].imshow(corr, vmin=-1, vmax=1, cmap="plasma")
fig.colorbar(im, ax=axes['C'], fraction=0.046, shrink=1.0, label="correlazione")
axes['C'].set_xticks([0, 1, 2, 3], ["alpha", "delta", "k", "Sx"])
axes['C'].set_yticks([0, 1, 2, 3], ["alpha", "delta", "k", "Sx"])
axes['C'].set_title("Matrice di correlazione dei parametri")
plt.tight_layout()
plt.show()
