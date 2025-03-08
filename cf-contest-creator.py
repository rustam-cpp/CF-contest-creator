import codeforces_api
import random
import os
import time
import sys

before_contest = 10
contest_duration = str()
while True:
  dur = input("Enter contest duration (in minutes or -1 for unlimited duration): ")
  try:
    contest_duration = int(dur)
    break
  except:
    print("Please, enter a number")

print("\nGetting problems from problemset...\n")

cf = codeforces_api.CodeforcesApi()
pr = cf.problemset_problems()
problems = pr['problems']
size = len(problems)

nickname = input("Enter your nickname on codeforces.com: ")
print()
count = str()
while True:
  cnt = input("Enter count of problems: ")
  try:
    count = int(cnt)
    break
  except:
    print("Please, enter a number")
ratings = list()
for i in range(count):
  while True:
    try:
      l, r = map(int, input("Enter problem " + str(i + 1) + " rating range (separated by a space, example: 1500 1700): ").split())
      if l > r:
        print("Please, enter 2 numbers, the first of which is less or equal than the second")
      elif l % 100 == 0 and r % 100 == 0 and l >= 800 and r >= 800 and l <= 3500 and r <= 3500:
        ratings.append(random.randint(l // 100, r // 100) * 100)
        break
      else:
        print("Please, enter 2 numbers that can be the rating of the task on CF")
    except:
      print("Please, enter 2 numbers")

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

new_problems = str()
flag = bool()

while True:
  new_problems = input("Do you want to use problems from newer contests? (Y/N): ")
  if new_problems == 'Y':
    flag = False
    break
  elif new_problems == 'N':
    flag = True
    break
  else:
    print("Please, enter Y or N")

for r in ratings:
  while True:
    idx = random.randint(0, size-1)
    problem = problems[idx]
    if problem.rating == r and problem.contest_id and tried.count(str(problem.contest_id) + problem.index) == 0 and (flag or problem.contest_id >= 1500) and problem.tags.count("*special") == 0:
      out.append(": codeforces.com/contest/" + \
            str(problem.contest_id) + "/problem/" + problem.index)
      # f.write("\t<a href=\"" + "https://codeforces.com/contest/" + str(problem.contest_id) + "/problem/" + \
      #         problem.index + "\" target=\"_blank\">Problem " + str(ix) + "<br></a>\n")
      break

# f.write("</body>\n</html>")
# f.close()

print("Contest created!\n")

while True:
  shuffle = input("Shuffle problems? (Y/N): ")
  if shuffle == 'Y':
    for i in range(2, count):
      if random.randint(0, 1) == 1:
        j = random.randint(0, i - 1)
        p1 = out[i]
        p2 = out[j]
        out[j] = p1
        out[i] = p2
    break
  elif shuffle == 'N':
    break
  else:
    print("Please, enter Y or N")

print("\nGood luck and happy coding!\n")

if contest_duration != -1:
  print("Contest starts in   ", end='')
  for t in range(before_contest, 0, -1):
    timer = str(t)
    if len(timer) == 1:
      timer = '0' + timer
    print("\b\b\b", timer, end='')
    sys.stdout.flush()
    time.sleep(1)

  print("\b" * 100, end='')
  print("Contest starts!     \n")

ix = 1

for p in out:
  print("Problem " + str(ix) + p)
  ix += 1

print()

# os.system("firefox index.html")

if contest_duration != -1:
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

input("Press Enter to exit")