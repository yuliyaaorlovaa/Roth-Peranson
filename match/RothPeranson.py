import pandas as pd

""" class CoupleStudent():
    def __init__(self, name, choices, partner):
        self.name = name
        self.choices = choices[::-1]
        self.current_rank = None
        self.current_place = None
        self.partner = partner
    
    def find_next_preference(self):
        # print(self.name, self.current_rank)
        return self.choices.pop()
    
    # both couples go for their next ranked.
    def apply_next(self):
        self.apply_next_me();
        self.partner.apply_next_me();

    def apply_next_me(self):
        try:
            program = self.find_next_preference()
        except IndexError:
            self.current_place = None
            # print("{} did not match.".format(self.name))
            return False

        # print(self.name, program.name)

        if program.receive_application(self):
            # print("{} temp matched to {}".format(self.name, program.name))
            self.current_place = program
            return True

        self.apply_next() """

class Couple():
    def __init__(self, names, choice_sets):
        self.names = names
        self.choice_sets = choice_sets[::-1]
        self.current_ranks = None
        self.current_places = None
    
    def find_next_preferences(self):
        # print(self.name, self.current_rank)
        if self.choices:
            return self.choices.pop()
        else:
            return None
    
    # both couples go for their next ranked.
    def apply_next(self):
        both_accepted = False
        while not both_accepted:
            programs = self.find_next_preferences()
            if not programs:
                self.current_place = None
                # print("{} did not match.".format(self.names))
                return False
            else:
                # print(self.name, program.name)
                accepted1 = programs[0].receive_application(self.names[0])
                if accepted1:
                    # print("{} temp matched to {}".format(self.names[0], program.name))
                    self.current_places[0] = programs[0]
                    accepted2 = programs[1].receive_application(self.names[1])
                    if accepted2:
                        # print("{} temp matched to {}".format(self.names[1], program.name))
                        self.current_places[1] = programs[1]
                        both_accepted = True
        return True

class Student():

    def __init__(self, name, choices):
        self.name = name
        self.choices = choices[::-1]
        self.current_rank = None
        self.current_place = None

    def find_next_preference(self):
        # print(self.name, self.current_rank)
        return self.choices.pop()

    def apply_next(self):
        try:
            program = self.find_next_preference()
        except IndexError:
            self.current_place = None
            # print("{} did not match.".format(self.name))
            return False

        # print(self.name, program.name)

        if program.receive_application(self.name):
            # print("{} temp matched to {}".format(self.name, program.name))
            self.current_place = program
            return True

        self.apply_next()

class Program():
# Class representing programs accepting total_places students

    def __init__(self, name, total_places=1):
        self.name = name
        self.choices = []
        self.current_picks = []
        self.total_places = total_places

    def get_insert_point(self, candidate):
        candidate_rank = self.choices.index(candidate)
        current_ranks = [self.choices.index(c) for c in self.current_picks]

        for i, r in enumerate(current_ranks):
            if candidate_rank < r:
                return i

    def receive_application(self, candidate):
        if candidate in self.choices:
            if len(self.current_picks) < self.total_places:
                self.current_picks.append(candidate)
                self.current_picks = sorted(self.current_picks, key=lambda r: self.choices.index(r))
                return True

            if self.get_pick_rank(candidate) < self.get_pick_rank(self.current_picks[-1]):
                insert_point = self.get_insert_point(candidate)
                self.current_picks.insert(insert_point, candidate)
                replaced = self.current_picks.pop()
                replaced.apply_next()
                return True

        return False

    def get_pick_rank(self, candidate):
        return self.choices.index(candidate)


class MatchController():
# Processing rank order lists for Students and Programs
# Controlling the match process and returning the final results.

    def __init__(self, program_data, candidate_data, places_data=None, #couplesdata):

        self.program_data = pd.read_csv(program_data)
        self.candidate_data = pd.read_csv(candidate_data)
        if places_data:
            self.places_data = pd.read_csv(places_data, index_col=0)

        self.programs = {}
        self.candidates = {}
        #self.couples????

        for c in self.program_data.columns:
            if places_data:
                self.programs[c] = Program(c, self.places_data.loc[c].places)
            else:
                self.programs[c] = Program(c)

        for c in self.candidate_data.columns:
            choices = self.candidate_data[c].dropna().tolist()
            choice_objects = [self.programs[p] for p in choices]
            self.candidates[c] = Student(c, choice_objects)

        # for c in self.couples_data.columns:
        #     choices = self.couples_data[c].dropna().tolist()
        #     choice_objects = [self.programs[p] for p in choices]
        #     self.candidates[c] = Couple(c, choice_objects)

        for c in self.program_data.columns:
            choices = self.program_data[c].dropna().tolist()
            choice_objects = [self.candidates[c].name for c in choices]
            self.programs[c].choices = choice_objects

    def start_match(self):
        for k, v in self.candidates.items():
            v.apply_next()

    def print_results(self):
        for c in sorted(self.candidates.keys()):
            print(c)
            try:
                print('    ', self.candidates[c].current_place.name)
            except AttributeError:
                print('Did not match')

    def results_dict(self):
        results_dict = {}

        for k, v in self.candidates.items():
            try:
                results_dict[k] = v.current_place.name
            except AttributeError:
                results_dict[k] = 'Did not match'

        return results_dict

    def get_output_csv(self):
        results = self.results_dict()

        results_df = pd.DataFrame.from_dict(
            results,
            orient='index')

        results_df = results_df.reset_index()
        results_df.columns = ['Candidate', 'Matched Program']

        results_df.to_csv('easy_match/results.csv', index=False)

