import numpy as np


"""常数，国际单位制"""
dict_MASS  = {1:1.008, # H
              8:15.999, # O
              14:28.085, # Si
              31:69.723, # Ga
              7:14.007, # N
              6:12.011} # C

AUG  = 1.0E-10
AMU  = 1.66054E-27
THz  = 1.0E+12
KB   = 1.38064E-23
HBAR = 1.05457E-34
QE   = 1.60218E-19


def get_atom_config_from(file_atom_config):
    lattice_vectors = np.loadtxt(file_atom_config, skiprows=2, max_rows=3)
    lattice_vectors = lattice_vectors * AUG
    # print(file + ' lattice_vectors: \n', lattice_vectors)
    Vsc = np.linalg.det(lattice_vectors)

    with open(file_atom_config, 'r') as f:
        lines = f.readlines()
        Natoms = int(lines[0].split()[0])
        for i, line in enumerate(lines):
            if 'Position, move_x, move_y, move_z' in line:
                start_line = i + 1
                # print(start_line)
                break

    atom_data = []
    for i, line in enumerate(lines[start_line:]):
        if i < Natoms:
            parts = line.split()
            if len(parts) >= 4: 
                atom_type = int(parts[0])
                frac_coords = list(map(float, parts[1:4]))
                atom_data.append([atom_type] + frac_coords)
        else:
            break
    atom_data = np.array(atom_data)
    # print(atom_data[0])

    atom_types = atom_data[:, 0].astype(int)
    frac_coords = atom_data[:, 1:4]

    #处理边界数值问题
    for a in frac_coords:
        for i in range(3):
            if a[i] > 0.99:
                a[i] = a[i] - 1.00

    real_coords = np.zeros_like(frac_coords)

    for i, fr in enumerate(frac_coords):
        real_coords[i][0] = fr[0] * lattice_vectors[0][0] + fr[1] * lattice_vectors[1][0] + fr[2] * lattice_vectors[2][0]
        real_coords[i][1] = fr[0] * lattice_vectors[0][1] + fr[1] * lattice_vectors[1][1] + fr[2] * lattice_vectors[2][1]
        real_coords[i][2] = fr[0] * lattice_vectors[0][2] + fr[1] * lattice_vectors[1][2] + fr[2] * lattice_vectors[2][2]

    list_mass = []
    for i in atom_types:
        list_mass.append(dict_MASS[i] * AMU)
    array_mass = np.array(list_mass)

    print("File:", file_atom_config)
    print("Natoms:", Natoms)
    print("Vsc:", Vsc)

    return real_coords, atom_types, Natoms, Vsc, array_mass

def get_muk_from(file_qpoints_yaml_dat, array_mass):
    Natoms = len(array_mass)
    omega_k = []
    frequency_local = []
    mu_k = []
    with open(file_qpoints_yaml_dat) as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if 'frequency' in lines[i]:
                frequency_local.append(i)
                omega_k.append(float((lines[i].split())[1]))
            i += 1
        omega_k = np.array(omega_k)
        omega_k = omega_k * THz * 2 * np.pi
        #获取原子数
        # Natoms = int(lines[len(lines) - 3].split('-')[1]) + 1
        # print('Natom:{}'.format(Natoms))

        for k in frequency_local:
            q = []
            for j in range(1,Natoms+1):
                temp = (lines[k + j].split())[1::2]
                for it,t in enumerate(temp):
                    temp[it] = float(t)
                q.append(temp)
            mu_k.append(q)
        mu_k = np.array(mu_k)

    mu_k = mu_k / np.sqrt(array_mass.reshape(1, Natoms, 1))

    return omega_k, mu_k

def O_ijk_cal(file_qpoints_yaml_dat, file_out_ep_cpeff, array_mass):

    omega_k, mu_k = get_muk_from(file_qpoints_yaml_dat, array_mass)

    rawdata_ep = np.loadtxt(file_out_ep_cpeff, skiprows=1, delimiter=None)
    eps = rawdata_ep[:,1:]
    # print(INT_eps[1][1],'!!eps') # 1.5417850284890895E-003
    eps = eps * (QE/AUG)

    Oijk = np.sum(mu_k * eps, axis=(1, 2))

    return Oijk, omega_k

def get_Vc(Oijk, omega_k, T):

    omega_k[omega_k < 1e9] = 1e30 # 数值计算是这样的

    return np.sqrt(KB * np.sum(Oijk ** 2 / omega_k ** 2)) * np.sqrt(T) / QE
