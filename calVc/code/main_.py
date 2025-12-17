from vcal import get_atom_config_from, get_muk_from, O_ijk_cal, get_Vc
import matplotlib.pyplot as plt
import numpy as np

config1 = "ov2.config"
qp1 = "ov2qpoints.yaml.dat"
e1 = "ov2.EP_COEFF"

config2 = "far.config"
qp2 = "farqpoints.yaml.dat"
e2 = "far.EP_COEFF"

config3 = "close.config"
qp3 = "closeqpoints.yaml.dat"
e3 = "close.EP_COEFF"

config4 = "ov.config"
qp4 = "ovqpoints.yaml.dat"
e4 = "ov.EP_COEFF"

_, _, _, _,arrayMass = get_atom_config_from(config1)
oijk, o = O_ijk_cal(qp1, e1, arrayMass)
ts = np.linspace(0,1000,1000)
vcs = []
for T in ts:
    vcs.append(get_Vc(oijk, o, T))

plt.plot(ts, vcs,label = 'Ovfar')

_, _, _, _,arrayMass = get_atom_config_from(config4)
oijk, o = O_ijk_cal(qp4, e4, arrayMass)
ts = np.linspace(0,1000,1000)
vcs = []
for T in ts:
    vcs.append(get_Vc(oijk, o, T))

plt.plot(ts, vcs, label = 'Ovclose')

_, _, _, _,arrayMass = get_atom_config_from(config2)
oijk, o = O_ijk_cal(qp2, e2, arrayMass)
ts = np.linspace(0,1000,1000)
vcs = []
for T in ts:
    vcs.append(get_Vc(oijk, o, T))

plt.plot(ts, vcs,label = 'DBfar')

_, _, _, _,arrayMass = get_atom_config_from(config3)
oijk, o = O_ijk_cal(qp3, e3, arrayMass)
ts = np.linspace(0,1000,1000)
vcs = []
for T in ts:
    vcs.append(get_Vc(oijk, o, T))

plt.plot(ts, vcs, label = 'DBclose')


plt.xlabel('T(K)')
plt.ylabel('Vc(eV)')
#plt.yscale('log')
plt.legend()
plt.show()
