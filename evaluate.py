from nfa import NFA
class Evaluator:
	def __init__(self, reg_expr):
		self.expr = reg_expr
	def expr2nfa(self):
		# Push everything into stack
		stack = [NFA(2, 1, {(0, x) : set([1])}, x) if len(x) == 1 else x for x in self.expr.split(" ")]
		# 2nd stack for saving the op result
		res_stack = []
		# While stack is not empty pop it
		# and compute the operations
		while stack:
			node = stack.pop()
			if (type(node) != str):
				res_stack.append(node)
			if node == "STAR":
				v1 = res_stack.pop()
				res_stack.append(v1.kleen_start(v1))
			if node == "PLUS":
				v1 = res_stack.pop()
				res_stack.append(v1.concat(v1, v1.kleen_start(v1)))
				pass
			if node == "UNION":
				v1 = res_stack.pop()
				v2 = res_stack.pop()
				res_stack.append(v1.union(v1, v2))
			if node == "CONCAT":
				v1 = res_stack.pop()
				v2 = res_stack.pop()
				res_stack.append(v1.concat(v1, v2))
		return res_stack.pop()