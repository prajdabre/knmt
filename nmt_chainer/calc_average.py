import sys, os

a = open(sys.argv[1])
b = open(sys.argv[2])

total = 0.0
tot_lines = 0

for i, j in zip(a, b):
	total += float(i)*float(j)
	tot_lines += float(j)

print total/tot_lines
	