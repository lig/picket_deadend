from mongoengine import *


class Project(Document):
    
    name = StringField()
    manager = ReferenceField('Employee')


class Release(Document):
    
    name = StringField()
    deadline = DateTimeField()
    current_stage = ReferenceField('Stage')
    milestones = SortedListField(EmbeddedDocumentField('Milestone'),
        ordering='deadline')


class Milestone(EmbeddedDocument):
    
    stage = ReferenceField('Stage')
    deadline = DateTimeField()


class Department(Document):
    
    name = StringField()
    head = ReferenceField('Employee')


class Stage(Document):
    
    name = StringField()
    department = ReferenceField('Department')
    order = IntField()
    first = ListField(GenericReferenceField()) # Status, Stage


class Status(Document):
    
    name = StringField()
    department = ReferenceField('Department')
    handler = GenericReferenceField() # Employee, Group, Department
    next = ListField(GenericReferenceField()) # Status, Stage


class Group(Document):
    
    department = ReferenceField('Department')
    project = ReferenceField('Project')
    employees = ListField(ReferenceField('Employee'))    


class Employee(Document):
    
    user = ReferenceField('User')
