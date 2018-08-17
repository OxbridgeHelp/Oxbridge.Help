import pandas as pd
import csv

identity = lambda x:x

def readCSV(fileName):
	with open(fileName, "r", encoding="latin-1") as file:
		reader = csv.reader(file)
		temp_list = [[thing2 for thing2 in thing] for thing in reader]
	return temp_list

applicantConversions = [int, identity, identity, identity, int, lambda x: x == "Y", identity]
def readApplicantCSV(fileName):
	temp_list = readCSV(fileName)
	keys = temp_list.pop(0)
	temp_list = [{keys[i].lower():applicantConversions[i](thing[i]) for i in range(len(keys))} for thing in temp_list]
	temp_dict = {}
	for thing in temp_list:
		id = thing["applicantid"]
		del thing["applicantid"]
		temp_dict[id] = thing
	return temp_dict

dataTypes = ["InterviewPrep", "PersonalStatement", "TestPrep", "GeneralResources", "Interview", "GeneralAdvice", "CourseResources"]
dataConversions = [int, lambda x:dataTypes.index(x), identity, lambda x:int(x) if x else -1, lambda x:int(x) if x else -1]
def readDataCSV(fileName):
	temp_list = readCSV(fileName)
	keys = temp_list.pop(0)
	temp_list = [{keys[i].lower():dataConversions[i](thing[i]) for i in range(len(keys))} for thing in temp_list]
	return temp_list


if __name__ == "__main__":
	import sys
	if not "-" in sys.argv:
		print("Need an option: try using -p or -p after the arguments")
		sys.exit(0)
	if "-p" in sys.argv:
		if "app" in sys.argv[1].lower():
			print(readApplicantCSV(sys.argv[2]))
		else:
			print(readDataCSV(sys.argv[2]))
	if "-l" in sys.argv:
		import database
		applicants = readApplicantCSV(sys.argv[2])
		data = readDataCSV(sys.argv[3])
		idDict = {}
		for napplicant in applicants:
			num = database.add_applicant(**applicants[napplicant])
			idDict[napplicant] = num
		for datum in data:
			datum["applicant"] = idDict[datum["applicantid"]]
			del datum["applicantid"]
			database.add_data(**datum)

