import numpy as np
import scipy.stats as stats

def make_members(couples):
    member_of = {}
    for couple_name, members in couples.items():
        for s in members:
            member_of[s] = couple_name
    return member_of

def setup(n_s, n_h, n_l, n_c, sigma_s, sigma_h, n_ss):

    rating_s = stats.norm(0,1).rvs(size = n_s)
    rating_h = stats.norm(0,1).rvs(size = n_h)
    location = stats.randint(0, n_l).rvs(size = n_h)

    epsilon_sh = stats.norm(0,1).rvs((n_s, n_h))
    epsilon_hs = stats.norm(0,1).rvs((n_h, n_s))
    epsilon_l = stats.norm(0,1).rvs((n_s, n_l))

    delta = stats.expon(scale=1).rvs(n_s)

    student_utility = rating_h + sigma_s * epsilon_sh + delta[:, None] * epsilon_l[:, location]
    hospital_utility = rating_s + sigma_h * epsilon_hs 

    ind_couple_utility = student_utility[:2*n_c]
    student_utility = student_utility[2*n_c:]

    student_rol= np.flip(np.argsort(student_utility, axis=1), axis=1)
    hospital_rol= np.flip(np.argsort(hospital_utility, axis=1), axis=1)

    names_h = np.array([f'H{i+1}' for i in range(n_h)])
    names_s = []
    for i in range(n_s):
        if i < 2*n_c:
            names_s.append(f'C{i+1}')
        else:
            names_s.append(f'S{i-2*n_c+1}')
    names_s = np.array(names_s)

    couples = {}
    partners = {}
    names_c = []
    for i in range(n_c):
        c1_name = names_s[2*i]
        c2_name = names_s[2*i+1]
        couple_name = f'C{2*i+1}{2*i+2}'
        names_c.append(couple_name)
        couples[couple_name] = [c1_name, c2_name]
        partners[c1_name] = c2_name
        partners[c2_name] = c1_name
    
    student_rol= {names_s[i+2*n_c]:list(names_h[student_rol[i]]) for i in range(n_ss)}
    hospital_rol= {names_h[i]:list(names_s[hospital_rol[i]]) for i in range(n_h)}

    couple_rol = {}
    for i in range(n_c):
        c1_utils = ind_couple_utility[2*i]
        c2_utils = ind_couple_utility[2*i+1]
        joint_util = np.add.outer(c1_utils, c2_utils)
        bonus=1
        recieves_bonus=np.equal.outer(location,location)
        couple_utility=joint_util+bonus*recieves_bonus
        joint_rol = np.transpose(np.flip(np.unravel_index(np.argsort(joint_util, axis=None), joint_util.shape), axis=1))
        joint_rol = names_h[joint_rol].tolist()
        couple_rol[names_c[i]] = joint_rol
        
    single_names = student_rol.keys()
    program_names = hospital_rol.keys()

    member_of = make_members(couples)

    matches = {p: [] for p in (list(program_names) + ['no match'])}

    outputs= rating_s, rating_h, location, epsilon_sh, epsilon_hs, epsilon_l, delta, student_utility, hospital_utility, ind_couple_utility, student_utility, student_rol, hospital_rol, names_h, names_s, couples, partners, names_c, student_rol, hospital_rol, couple_rol, single_names, program_names, member_of, matches
    return outputs
