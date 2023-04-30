from match.RothPeranson import MatchController

def run_match():
    program_rol = 'easy_match/program_rank_order_lists.csv'
    candidate_rol = 'easy_match/candidate_rank_order_lists.csv'
    #couple_rol=''
    program_places = 'easy_match/program_places.csv'

    match = MatchController(program_rol, candidate_rol, program_places, #couple_rol)
   # for k,v in match.candidates.items():
        #name_list=[]
       # for program in v.choices:
        #    name_list.append(program.name)
      #  print(name_list)
    match.start_match()
    results = match.results_dict()

    print(results)
    match.get_output_csv()

if __name__ == '__main__':
    run_match()
