import sys
from nfa import NFA
from evaluate import Evaluator

class DFA:
	def __init__(self):
		self.EPS = ''
		self.delta = dict()
		self.queue = []
		self.mapping = dict()
		self.states = {0}
		self.nr_states = 0
	# Main function for converting NFA to DFA
	def make_dfa(self, delta, abc):
		self.eps_closure(delta, 0, self.states)
		self.queue.append(self.states)
		self.mapping[0] = self.states
		crt_state = 1
		while self.queue:
			curent_state = self.queue.pop(0)
			for symbol in abc:
				trans = set(self.next_state(delta, list(curent_state), symbol))
				for var in list(trans):
					self.eps_closure(delta, var, trans)
				if trans not in self.mapping.values():
					self.mapping.update({crt_state : trans})
					crt_state += 1
					self.queue.append(trans)
				self.delta.update({(self.nr_states, symbol) : trans})
			self.nr_states += 1
	# Compute all epsilone closure from the current state
	def eps_closure(self, transitions, state, next_states):
		# if there is no transition with EPS return nothing
		if (state, self.EPS) not  in transitions:
			return None
			# a DFS throught all EPS states
		for x in list(transitions[state, self.EPS]):
			if (x, self.EPS) not in transitions:
				next_states.add(x)
			else:
				if x not in list(next_states):
					next_states.add(x)
					self.eps_closure(transitions, x, next_states)

	# Returns the list of next states with a specifit symbol
	# from the delta transitions of the NFA
	def next_state(self, delta, states, symbol):
		return sum([list(delta[x, symbol]) for x in states if (x, symbol) in delta ], [])

	# joins all finals states from the automata
	# traverse all final_states from NFA and check if
	# this specific states is mapped with at least one
	# state from DFAs states 
	def final_states(self, mapping, final_states):
		states = []
		for x in final_states:
			states.append([k for k,v in mapping.items() if x in set(v)])
		final = sum(states, [])
		return(" ".join([str(y) for y in set(final)]) + "\n")

	# Convers all transitions in human readable string
	def toString(self, dfa, mapping):
		trans = ""
		for x, y in dfa.items():
			trans += " ".join([str(x[0]) + ( ",'" + str(x[1]) + "',") \
						+ str(a) + "\n" for a in mapping if y == mapping[a]])
		return trans

def main(argv):
	
	file_reader = open(argv[0], "r")
	file_writer = open(argv[1], "w") 

	# Read the RegExpr from the file
	f = file_reader.readline().rstrip()
	# Make an instance of evauator to eval the regexpr
	e = Evaluator(f)

	
	# Evaluate the RegExpr using stack
	automata = e.expr2nfa()
	
	# Make an instance of dfa automata
	dfa_instance = DFA()
	
	# Convert nfa into dfa passing the delta transitions and the alphabet
	dfa_instance.make_dfa(automata.transitions, automata.abc)
	
	# Save the result as an entire string
	result  = "".join(set(automata.abc)) + "\n" + str(dfa_instance.nr_states)  + "\n" \
				+ str(automata.init_state) + "\n" \
				+ dfa_instance.final_states(dfa_instance.mapping, set([automata.final_state])) \
				+ dfa_instance.toString(dfa_instance.delta, dfa_instance.mapping)

	# Write the string into out file
	file_writer.write(result[:-1])

	return True

if __name__ == '__main__':
	main(sys.argv[1:])