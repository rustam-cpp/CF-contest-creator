import codeforces_api
import random
import os
import time
import sys

before_contest = 10
contest_duration = int(input("Enter contest duration (in minutes): "))


print("\nGetting problems from problemset...\n")

cf = codeforces_api.CodeforcesApi()
pr = cf.problemset_problems()
problems = pr['problems']
size = len(problems)

nickname = input("Enter your nickname on codeforces.com: ")
print()
count = int(input("Enter count of problems: "))
ratings = list()
for i in range(count):
	print("Enter problem", i + 1, "rating range (separated by a space, example: 1500 1700):", end=' ')
	l, r = map(int, input().split())
	ratings.append(random.randint(l // 100, r // 100) * 100)

print("\nNeed to get your already tried problems...")

problems_tried_by_user = cf.user_status(handle=nickname)
tried = list()

print("\nGenerating...")

for s in problems_tried_by_user:
	p = s.problem
	tried.append(str(p.contest_id) + p.index)

# f = open("index.html", "w")
# f.write("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n\t<meta charset=\"UTF-8\">\n\t<title>Contest</title>\n</head>\n<body>\n")

# f.write("\t<h1>Contest of " + str(count) + " problems</h1>\n")

out = list()

new_problems = input("Do you want to use problems from newer contests? (Y/N): ")
flag = True
if new_problems == 'Y':
	flag = False

for r in ratings:
	while True:
		idx = random.randint(0, size-1)
		problem = problems[idx]
		if problem.rating == r and problem.contest_id and tried.count(str(problem.contest_id) + problem.index) == 0 and (flag or problem.contest_id >= 1500) and problem.tags.count("*special") == 0:
			out.append(": codeforces.com/contest/" + \
						str(problem.contest_id) + "/problem/" + problem.index)
			# f.write("\t<a href=\"" + "https://codeforces.com/contest/" + str(problem.contest_id) + "/problem/" + \
			#		 problem.index + "\" target=\"_blank\">Problem " + str(ix) + "<br></a>\n")
			break

# f.write("</body>\n</html>")
# f.close()

print("Contest created!\n")

shuffle = input("Shuffle problems? (Y/N): ")
if shuffle == 'Y':
	for i in range(2, count):
		if random.randint(0, 1) == 1:
			j = random.randint(0, i - 1)
			p1 = out[i]
			p2 = out[j]
			out[j] = p1
			out[i] = p2
print("\nGood luck and happy coding!\n")
print("Contest starts in   ", end='')
for t in range(before_contest, 0, -1):
	timer = str(t)
	if len(timer) == 1:
		timer = '0' + timer
	print("\b\b\b", timer, end='')
	sys.stdout.flush()
	time.sleep(1)

print("\b" * 100, end='')
print("Contest starts!	 \n")

ix = 1

for p in out:
	print("Problem " + str(ix) + p)
	ix += 1

print()

# os.system("firefox index.html")

h = contest_duration // 60
m = contest_duration % 60
s = 0
for i in range(contest_duration * 60):
	hh = str(h)
	if len(hh) == 1:
		hh = '0' + hh
	mm = str(m)
	if len(mm) == 1:
		mm = '0' + mm
	ss = str(s)
	if len(ss) == 1:
		ss = '0' + ss
	print(hh, mm, ss, sep=':', end='')
	sys.stdout.flush()
	time.sleep(1)
	print("\b" * 100, end='')
	sys.stdout.flush()
	s -= 1
	if s == -1:
		s = 59
		m -= 1
		if m == -1:
			m = 59
			h -= 1

print("The contest is over!")
