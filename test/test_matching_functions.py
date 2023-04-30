from src.match.matching_functions import *

def test_get_matched_program():
    student_id= 'S1'
    matches= {'H1':['S4', 'S5', 'S7'],
              'H2':['S1', 'S8', 'S3'],
              'H3':['S10', 'S11','S12']}
    
    result = get_matched_program(student_id, matches)
    assert result=='H2'
    student_id= 'S14'
    result = get_matched_program(student_id, matches)
    assert result== None
    student_id='S11'
    result = get_matched_program(student_id, matches)
    assert result=='H3'