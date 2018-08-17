from peewee import *
from playhouse.db_url import connect

password = input("Input the database password:\n")
database = connect("mysql://dev:{}@localhost/dev".format(password))
database.connect()

class BaseModel(Model):
	class Meta:
		database = database

class Applicant(BaseModel):
	university = TextField()
	college = TextField()
	course = TextField()
	cycle = IntegerField()
	offer = IntegerField()
	email = TextField()

class Data(BaseModel):
	applicant = ForeignKeyField(Applicant)
	datatype = IntegerField()
	data = TextField()
	rankgroup = IntegerField()
	firstthree = BooleanField()
	class Meta:
		primary_key = CompositeKey("applicant", "datatype")

database.create_tables([Applicant, Data])

def add_applicant(university, college, course, cycle, offer, email):
	return Applicant.insert(university=university, college=college, course=course, cycle=cycle, offer=offer, email=email).execute()

def add_data(applicant, datatype, data, rankgroup, firstthree):
	return Data.insert(applicant=applicant, datatype=datatype, data=data, rankgroup=rankgroup, firstthree=firstthree).execute()

def add_compliment(university, college, course, cycle, offer, email, data):
	num = add_applicant(university, college, course, cycle, offer, email)
	for datum in data:
		datum = dict(datum)
		datum.update({"applicant": num})
		add_data(**datum)

test = lambda : add_compliment(university="a", college="b", course="c", cycle=0, offer=True, email="hi", data=[{"dataType":1, "data":"Hi", "firstthree":False, "rankGroup":2}, {"dataType":2, "data": "what?", "firstthree":True, "rankGroup":1}])
