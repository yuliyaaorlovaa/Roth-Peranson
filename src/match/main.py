import random
import numpy as np
import scipy.stats as stats
from matching_functions import *
from setup import *
from itertools import product

num_students = [50, 100, 200]
num_hospitals = [10, 20, 30]
num_locations = [2, 4, 5]
num_couples= [4, 5, 6]
sig_s = [0.2, 0.3, 0.5]
sig_h = [0.2, 0.3, 0.5]
num_slots_list=[4, 5, 6]
combinations = product(num_students, num_hospitals, num_locations, num_couples, sig_s, sig_h, num_slots_list)


def main_routine(outputs):

    rating_s, rating_h, location, epsilon_sh, epsilon_hs, epsilon_l, delta, student_utility, hospital_utility, ind_couple_utility, student_utility, student_rol, hospital_rol, names_h, names_s, couples, partners, names_c, student_rol, hospital_rol, couple_rol, single_names, program_names, member_of, matches = outputs
    n_s = num_students 
    n_h = num_hospitals
    n_l = num_locations
    n_c = num_couples
    sigma_s = sig_s
    sigma_h = sig_h


    program_stack, applicant_stack= make_stable(single_names, matches)
    deal_with(p, matches, member_of)
    reset(s)
    deal_with_couple(c, p, couple_rol)
    mutually_prefer(p, student, current_program)
    get_preferences(s, single_names, student_rol, names_c, couple_rol, member_of, couples)
    get_matched_program(s, matches)
    add_single(s, matches, student_rol)
    add_couple(c, matches)
    couple_propose(c, couple_rol, couples)
    move_on(s, single_names, names_c, member_of, partners)
    withdraw(s, matches, member_of, partners)
    is_couple_preferred(c, programs, couples, num_slots, hospital_rol, matches)
    is_preferred(s, program, num_slots, matches, hospital_rol)
    accept(s, program, matches, num_slots)
    sort_matches(program, hospital_rol, matches)
    has_options(s, single_names, student_rol, couple_rol)
    choice_index(s) 


    print(f'matches={matches}')
    #return match()


for n_s, n_h, n_l, n_c, sigma_s, sigma_h, num_slots in combinations:
    n_ss=n_s-2*n_c
    outputs = setup(n_s, n_h, n_l, n_c, sigma_s, sigma_h, num_slots)

    main_routine(outputs)

# individuals vs couple and log results

# main_routine(outputs)

    