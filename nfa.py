EPS = ""

def shift(offset, this_dict):
    return {(k[0] + offset, k[1]) : set([i + offset for i in v]) for k,v in this_dict.items()}
def get_value_by_idx(this_dict, idx):
    return [v for k,v in this_dict.items()][idx]
def get_key_by_idx(this_dict, idx):
    return [k[0] for k,v in this_dict.items()][idx]
class NFA:
    def __init__(self, nr_states, final_state, transitions, abc):
        self.nr_states = nr_states
        self.init_state = 0
        self.final_state = final_state
        self.transitions = transitions
        self.abc = abc
    def print_NFA(self):
        print("Init state:", self.init_state)
        print("Total states:", self.nr_states)
        print("Final state:", self.final_state)
        print("Delta:", self.transitions)
        print("Alpha:", "".join(list(set(self.abc))))

    def concat(self, fst_nfa, snd_nfa):
        # add one additional states at the end of fst automata
        # shift all states of 2nd automata with + final state of fst automata
        # add redundant epsilon transition between 2 NFAs
        #fst_nfa.transitions.update({(fst_nfa.final_state, EPS) : set([fst_nfa.final_state + 1])})
        shifted_nfa = shift(max(get_value_by_idx(fst_nfa.transitions, -1)), snd_nfa.transitions)
        fst_nfa.transitions.update(shifted_nfa)
        # return the new DFA concatenated by two previous
        return NFA(fst_nfa.nr_states + snd_nfa.nr_states,
                    max(get_value_by_idx(shifted_nfa, -1)),
                    fst_nfa.transitions,
                    fst_nfa.abc+snd_nfa.abc)
    def kleen_start(self, nfa):
        # shift with +1 all states of current NFA
        shifted_trans = shift(1, nfa.transitions)
        # construct 2 additional eps transitions starting from init state 
        start = {(0, EPS) : set([1, max(get_value_by_idx(shifted_trans, -1)) + 1])}
        # insert states into nfa
        start.update(shifted_trans)
        # insert 2 additional eps transitions starting from final state
        end = {(max(get_value_by_idx(shifted_trans, -1)), EPS) : 
                        set([get_key_by_idx(shifted_trans, 0),
                        max(get_value_by_idx(shifted_trans, -1)) + 1])}
        start.update(end)
        # construct new NFA with all transitions, initial and final states
        return NFA(max(get_value_by_idx(start, -1)) + 1,
                    max(get_value_by_idx(start, -1)),
                    start,
                    nfa.abc)
    def union(self, fst, snd):
        shifted_fst = shift(1, fst.transitions)
        shifted_snd = shift(max(get_value_by_idx(shifted_fst, -1)) + 1, snd.transitions)
        start = {(0, EPS) : set([get_key_by_idx(shifted_fst, 0), get_key_by_idx(shifted_snd, 0)])}


        start.update(shifted_fst)
        start.update({(max(get_value_by_idx(shifted_fst, -1)), EPS) : set([max(get_value_by_idx(shifted_snd, -1)) + 1])})
        start.update(shifted_snd)
        start.update({(max(get_value_by_idx(shifted_snd, -1)), EPS) : set([max(get_value_by_idx(shifted_snd, -1)) + 1])})

        return NFA(max(get_value_by_idx(start, -1)) + 1,
                    max(get_value_by_idx(start, -1)),
                    start,
                    fst.abc+snd.abc)