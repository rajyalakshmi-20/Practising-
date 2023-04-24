class Student():
    def __init__(self,name,rollno):
        self.name=name
        self.rollno=rollno
newStudent=Student(name="pavan",rollno=666) 
class Display(Student):
    def __init__(self,father,height,group):
        self.father=father
        self.height=height
        self.gropu=group
newDisplay=Display(father="venu",height="5.5ft",group="python")
class Setage(Student):
    def __init__(self,age):
        self.age=age
newSetage=Setage(age=22)
class Setmarks(Student):
    def __init__(self,marks):
        self.marks=marks
newSetmarks=Setmarks(marks=555)
 
print("name of the:",newStudent.name)
print("roll no.of student:",newStudent.rollno)
print("father nameof the student:",newDisplay.father)
print("age of the student:",newSetage.age)
print("marks of the students:",newSetmarks.marks) 