from mongoengine import *


class Employee(Document):
    
    user = ReferenceField('User')


class Project(Document):
    
    name = StringField()
    manager = ReferenceField(Employee)


class Department(Document):
    
    name = StringField()
    head = ReferenceField(Employee)


class Group(Document):
    
    department = ReferenceField(Department)
    project = ReferenceField(Project)
    employees = ListField(ReferenceField(Employee))    


class Stage(Document):
    
    name = StringField()
    department = ReferenceField(Department)
    order = IntField()
    first = GenericReferenceField() # Status, Stage


class Milestone(EmbeddedDocument):
    
    stage = ReferenceField(Stage)
    deadline = DateTimeField()


class Release(Document):
    
    name = StringField()
    project = ReferenceField(Project)
    deadline = DateTimeField()
    current_stage = ReferenceField(Stage)
    milestones = SortedListField(EmbeddedDocumentField(Milestone),
        ordering='deadline')


class Status(Document):
    
    name = StringField()
    department = ReferenceField(Department)
    handler = GenericReferenceField() # Employee, Group, Department
    next = ListField(GenericReferenceField()) # Status, Stage


class Comment(EmbeddedDocument):
    
    submitted = DateTimeField()
    author = ReferenceField(Employee)
    text = StringField()

    
class Issue(Document):
    
    subject = StringField()
    submitted = DateTimeField()
    author = ReferenceField(Employee)
    text = StringField()
    project = ReferenceField(Project)
    status = ReferenceField(Status)
    handler = GenericReferenceField() # Employee, Group, Department
    comments = SortedListField(EmbeddedDocumentField(Comment),
        ordering='submitted')
