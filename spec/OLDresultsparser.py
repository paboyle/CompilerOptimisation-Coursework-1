#!/usr/bin/python
from os import system
import shlex

file = open("CompileRuntimes")
results={}
for line in file:
	tokens = shlex.split(line)
	if not (tokens[3] in results):
		results[tokens[3]] = {}
	if not (tokens[6] in results[tokens[3]]):
		results[tokens[3]][tokens[6]] = {}
	if not ("compile" in results[tokens[3]][tokens[6]]):
		results[tokens[3]][tokens[6]]["compile"] = {}
	#if !(tokens[1] in results[tokens[3]][tokens[6]]["compile"]):
	#	results[tokens[3]][tokens[6]]["compile"][tokens[1]] = {}
	results[tokens[3]][tokens[6]]["compile"][tokens[1]] = tokens[8]

file2 = open("BenchRunTimes")
for line2 in file2:
	tokens = shlex.split(line2)
	if not ("run" in results[tokens[3]][tokens[6]]):
		results[tokens[3]][tokens[6]]["run"] = {}
	results[tokens[3]][tokens[6]]["run"][tokens[1]] = tokens[8]


for program in results:
	for opt in results[program]:
		times= []
		for run in results[program][opt]["compile"]:
			#print results[program][opt]["compile"][run]
			times.append(int(float(results[program][opt]["compile"][run])))
		#print "COMPILE\t {0} {1} : {2}".format(program, opt, sum(times)/len(times))
		results[program][opt]["compile"]["avg"] = sum(times)/len(times)
		runtimes = []
		for run in results[program][opt]["run"]:
			runtimes.append(int(float(results[program][opt]["run"][run])))
		#print "RUN\t {0} {1} : {2}".format(program, opt, sum(runtimes)/len(runtimes))
		results[program][opt]["run"]["avg"] = sum(runtimes)/len(runtimes)


baseline = ['-O3', '-O0', '-O1', '-O2', '-O3']

overall = {}
for program in results:
	for opt in results[program]:
		
			if not opt in baseline:
				if opt in overall:
					overall[opt] += int(float(results[program][opt]["run"]["avg"]))
				else:
					overall[opt] = int(float(results[program][opt]["run"]["avg"]))

bestoverall = min(overall, key=overall.get)

outfile = open("raw_runtimes", 'w')
failures = {}
best = {}

for program in results:
	outfile.write(program + "\n")
	plot = open("plots/{0}.plot".format(program), 'w')
	failures[program] = {}
	best[program] = ("DEFAULT", 10000000000, 0)
	failures[program]["RAW"] = []
	for opt in results[program]:
		
		if results[program][opt]["run"]["avg"] < best[program][1]:
			if not opt in baseline:
				best[program] = (opt, results[program][opt]["run"]["avg"], results[program][opt]["compile"]["avg"])
		if len(opt) < 5:
			plot.write("{0}\t{1}\t{2}\n".format( results[program][opt]["run"]["avg"], results[program][opt]["compile"]["avg"], '\"' + opt + '\"'))
		outfile.write("\"" + opt + "\"")
		for run in results[program][opt]["run"]:
			if int(float(results[program][opt]["run"][run])) < 50:
				failopts = opt.split(" ")
				failures[program]["RAW"].append(opt)
				for fo in failopts:
					if fo in failures[program]:
						failures[program][fo] += 1
					else:
						failures[program][fo] = 0
			#rt.append(int(results[program][opt]["run"][run]))

			outfile.write(" " + str(int(float(results[program][opt]["run"][run]))))
		outfile.write("\n")
	plot.write("{0}\t{1}\t{2}\n".format(best[program][1], best[program][2], "\"Best for Program\""))#'\"' + best[program][0] + '\"'))
	if len(results[program].keys()) == 204:
		plot.write("{0}\t{1}\t{2}\n".format(results[program][bestoverall]["run"]["avg"], results[program][bestoverall]["compile"]["avg"], " \"Best across all\""))
	plot.close()
	system("./plots/bars.sh {0} {1}".format("plots/{0}.plot".format(program), "plots/{0}.png".format(program)))
outfile.close()



