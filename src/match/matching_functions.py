import random
import numpy as np
import scipy.stats as stats

    
def match(single_names, names_c, applicant_stack):
    for s in single_names:
        applicant_stack.append(s)
        make_stable()
    for c in names_c:
        applicant_stack.append(c)
        make_stable()
    return True


def make_stable(single_names, matches, program_stack, applicant_stack):
    while applicant_stack:
#        print(f'applicant_stack={applicant_stack}, matches={matches}')
        s = applicant_stack.pop(0)
        if s in single_names:
            add_single(s)
        else:
            add_couple(s)
    if program_stack:
#       print(f'program_stack={program_stack}, matches={matches}')
        program = program_stack.pop(0)
        while matches['no match']:
            s = matches['no match'].pop()
            reset(s)
        deal_with(program, matches, member_of)
        random.shuffle(applicant_stack)
        make_stable()

    return program_stack, applicant_stack


def deal_with(p:str, matches:dict, member_of:dict):
    """modifies the matches dictionary according to mutual preferences

    Args:
        p (str): program id to match 
        matches (dict): dictionaries that uses program as keys and list of students as return value 
        member_of (dict): dictionary that uses couple id as keys and list of members of couple as return value
    """
    

    for program, students in matches.items():
        if program == p:
            next
        for s in students:
            if s in member_of:
                c = member_of[s]
                deal_with_couple(c, p)
            elif mutually_prefer(p, s, program):
                reset(s)


def reset(s, applicant_stack, current_choices):
    print(f'resetting {s}')
    withdraw(s)
    applicant_stack.append(s)
    current_choices[s] = 0


def deal_with_couple(c, p, couple_rol):
    """_summary_

    Args:
        c (_type_): _description_
        p (_type_): _description_
        couple_rol (_type_): _description_
    """
    c_ind = choice_index(c)
    for i in range(c_ind):
        prefs = couple_rol[c][i]
        if p in prefs and is_couple_preferred(c, prefs):
            reset(c)
            return
        

def mutually_prefer(p, student, current_program):
    prefs = get_preferences(student)
    if current_program == 'no match':
        student_prefers = True
    else:
        student_prefers =  prefs.index(p) < prefs.index(current_program)
    return is_preferred(student, p) and student_prefers


def get_preferences(s, single_names, student_rol, names_c, couple_rol, member_of, couples):
    if s in single_names:
        return student_rol[s]
    elif s in names_c:
        return couple_rol[s]
    else:
        couple = member_of[s]
        ind = couples[couple].index(s)
        return [pref[ind] for pref in couple_rol[couple]]
    

def get_matched_program(student_id:str, matches:dict)->str:
    """_summary_

    Args:
        s (str): string key that looks up unique student id
        matches (dict): dictionaries that uses program as keys and list of students as return value 

    Returns:
        _type_: _description_
    """
    for program, students in matches.items():
        if student_id in students:
            return program
    return None


def add_single(s, matches, student_rol):
    if not has_options(s):
        matches['no match'].append(s)
        return False
    program = student_rol[s][choice_index(s)]
    if is_preferred(s, program):
#        print(f'{program} prefers {s}')
        accept(s, program)
    else:
#        print(f'{s} is moving on')
        move_on(s)


def add_couple(c, matches):
    if not has_options(c):
        matches['no match'].append(c)
        return False
    return couple_propose(c)


def couple_propose(c, couple_rol, couples):
    prefs = couple_rol[c][choice_index(c)]
    pref1, pref2 = prefs
    c1, c2 = couples[c]
    if is_couple_preferred(c, prefs):
        print(f'{pref1} and {pref2} prefer {c1} and {c2}')
        accept(c1, pref1)
        accept(c2, pref2)
    else:
        print(f'{c1}, {c2} are moving on')
        move_on(c)


def move_on(s, single_names, names_c, member_of, partners, current_choices, applicant_stack):
    if s in single_names:
        current_choices[s] += 1
        applicant_stack.append(s)
    elif s in names_c:
        current_choices[s] += 1
        applicant_stack.append(s)
    else:
        couple = member_of[s]
        partner = partners[s]
        withdraw(partner)
        move_on(couple)


def withdraw(s, matches, member_of, partners, program_stack):
    program = get_matched_program(s)
    if program:
        matches[program].remove(s)
        if program != 'no match':
            program_stack.append(program)
    if s in member_of:
        partner = partners[s]
        program = get_matched_program(partner)
        if program:
            matches[program].remove(partner)
            if program != 'no match':
                program_stack.append(program)


def is_couple_preferred(c, programs, couples, num_slots, hospital_rol, matches):
    pref1, pref2 = programs
    c1, c2 = couples[c]
    if pref1 == pref2:
        if num_slots < 2:
            return False
        prog_prefs = hospital_rol[pref1]
        if prog_prefs.index(c1) < prog_prefs.index(c2):
            oc1, oc2 = c1, c2
        else:
            oc1, oc2 = c2, c1
        current_matches = matches[pref1]
        if len(current_matches) <= num_slots - 2:
            return True
        elif len(current_matches) == num_slots - 1:
            return prog_prefs.index(oc2) < prog_prefs.index(current_matches[-1])
        else:
            return prog_prefs.index(oc2) < prog_prefs.index(current_matches[-2])
    else:
        return is_preferred(c1, pref1) and is_preferred(c2, pref2)
    

def is_preferred(s, program, num_slots, matches, hospital_rol):
    if len(matches[program]) < num_slots:
        return True
    else:
        current_match = matches[program][-1]
        prefs = hospital_rol[program]
        return prefs.index(s) < prefs.index(current_match)
    

def accept(s, program, matches, num_slots):
    if len(matches[program])==num_slots:
        current_match = matches[program][-1]
        matches[program].remove(current_match)
        move_on(current_match)
    matches[program].append(s)
    sort_matches(program)


def sort_matches(program, hospital_rol, matches):
    prefs = hospital_rol[program]
    matches[program].sort(key=lambda s: prefs.index(s))


def has_options(s, single_names, student_rol, couple_rol):
    if s in single_names:
        choice=choice_index(s)
        student_list=len(student_rol[s])
        return choice_index(s) < len(student_rol[s])
    else:
        return choice_index(s) < len(couple_rol[s])


def choice_index(s, current_choices):
    if s not in current_choices:
        current_choices[s] = 0
    return current_choices[s]



    

    
