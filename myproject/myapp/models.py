from django.db import models

class Issue(models.Model):
    STATUS_CHOICES = (
        ('INQUEUE', 'In Queue'),
        ('ASSIGNED', 'Assigned'),
        ('DISPATCHED', 'Dispatched'),
        ("CLEARED","Cleared")
    )

    issueID = models.AutoField(primary_key=True)
    userID = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    problem = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INQUEUE')
    assigned_mech=models.IntegerField(default=0)
    assigned_agent=models.IntegerField(default=0)

class Agent(models.Model):
    agentID = models.AutoField(primary_key=True)
    queue = models.IntegerField(default=0)
    issue_list=models.CharField(max_length=1000,default='[]')

class Mechanic(models.Model):
    mechanicID = models.AutoField(primary_key=True)
    availability = models.BooleanField(default=True)
