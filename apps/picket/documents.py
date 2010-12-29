from django.db.models import permalink
from mongoengine import *
from mongoengine.django.auth import User

from sequences import get_next_pk


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
    
    number = IntField(primary_key=True)
    subject = StringField(max_length=1024)
    submitted = DateTimeField()
    author = ReferenceField(User)
    text = StringField()
    project = ReferenceField(Project)
    status = ReferenceField(Status)
    handler = GenericReferenceField() # Employee, Group, Department
    comments = SortedListField(EmbeddedDocumentField(Comment),
        ordering='submitted')
    
    def __unicode__(self):
        return '[%s] %s' % (self.number, self.subject)

    @permalink
    def get_absolute_url(self):
        return 'picket-issue', (self.number,)
    
    def save(self):
        #@todo: status and other logic handling
        
        if not self.number:
            self.number = get_next_pk('issue')
        
        super(Issue, self).save()
