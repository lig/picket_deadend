from django.db.models import permalink
from mongoengine import *
from mongoengine.django.auth import User


class Project(Document):
    
    name = StringField(max_length=255)
    manager = ReferenceField(User)
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return 'picket-admin-project', (self.id,)


class Department(Document):
    
    name = StringField(max_length=255)
    head = ReferenceField(User)
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return 'picket-admin-department', (self.id,)


class Group(Document):
    
    department = ReferenceField(Department)
    project = ReferenceField(Project)
    employees = ListField(ReferenceField(User))    


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
    author = ReferenceField(User)
    text = StringField()

    
class Issue(Document):
    
    subject = StringField()
    submitted = DateTimeField()
    author = ReferenceField(User)
    text = StringField()
    project = ReferenceField(Project)
    status = ReferenceField(Status)
    handler = GenericReferenceField() # Employee, Group, Department
    comments = SortedListField(EmbeddedDocumentField(Comment),
        ordering='submitted')
