# regexpr2dfa
Convert a Regular Expression into DFA

# How to run
Linux/WSL: python3 main.py <input_file> <out_file>

# Input
An input file contains a regular expression in a prenex form.


# Output
Program writes at the outfile an DFA with its:
<dfa_alphabet>
<number_of_states>
<initial_state>
<final_states>
<transitions>
  
# Prenex examples
A prenex form of ** ab|c* ** regexpr has a tree representation of **UNION(CONCAT(a,b),STAR(c))**.
Prenex form has its operations first after operands are followed.

# Algorithm
  1. Convert the expression into NFA automata with epsilone transitions
  2. Evaluate the expression and construct a final NFA using Thompson's construction
  3. Convert final NFA into DFA using epsilone closure
  
UNION a b = a|b
  
UNION CONCAT a b STAR c = ab | c*
  
CONCAT UNION a b UNION c d = (a | b)(c | d)
  
  

# Refs
https://en.wikipedia.org/wiki/Thompson%27s_construction
https://www.geeksforgeeks.org/regular-expression-to-nfa/



