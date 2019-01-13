from mip.model import *
from sys import stdout, argv
from time import process_time
import time

Solvers=['cbc', 'gurobi']
N = range(100,1001,100)

f = open('queens-pypy.csv', 'w')

def gen_model(n, solver):
	st = time.time()
	queens = Model('queens', MINIMIZE, solver_name=solver)

	x = [[queens.add_var('x({},{})'.format(i, j), type='B', obj=-1.0)
		  for j in range(n)] for i in range(n)]

	# one per row
	for i in range(n):
		queens += xsum(x[i][j] for j in range(n)) == 1, 'row({})'.format(i)

	# one per column
	for j in range(n):
		queens += xsum(x[i][j] for i in range(n)) == 1, 'col({})'.format(j)

	# diagonal \
	for p, k in enumerate(range(2 - n, n - 2 + 1)):
		queens += xsum(x[i][j] for i in range(n) for j in range(n) if i - j == k) <= 1, 'diag1({})'.format(p)

	# diagonal /
	for p, k in enumerate(range(3, n + n)):
		queens += xsum(x[i][j] for i in range(n) for j in range(n) if i + j == k) <= 1, 'diag2({})'.format(p)

	ed = time.time()

	f.write('{},{},{},pypy-mip-{},{:.4f}\n'.format(n, queens.num_cols, queens.num_rows, solver, ed-st))
	f.flush()


for n in N:
	for solver in Solvers:
		gen_model(n, solver)
f.close()
