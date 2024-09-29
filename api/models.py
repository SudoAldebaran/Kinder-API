from django.db import models

#doc PARENTS
class Parent(models.Model):
    name = models.CharField(max_length=100) #doc PARENT NAME
    email = models.EmailField(unique=True) #doc PARENT EMAIL : MUST BE UNIQUE

#doc CHILD
class Child(models.Model):
    name = models.CharField(max_length=100) #doc CHILD NAME
    age = models.IntegerField() #doc CHILD AGE
    parent = models.ForeignKey(Parent, related_name='children', on_delete=models.CASCADE) #doc FOREIGN KEY : PARENT

#doc HOUSEHOLD
class Household(models.Model):
    parent1 = models.ForeignKey(Parent, related_name='household_parent1', on_delete=models.CASCADE) #doc HOUSEHOLD PARENT 1
    parent2 = models.ForeignKey(Parent, related_name='household_parent2', on_delete=models.CASCADE) #doc HOUSEHOLD PARENT 2

#doc INVITATION
class Invitation(models.Model):
    sender = models.ForeignKey(Parent, related_name='invitation_sent') #doc PARENT SENDER
    recipient = models.ForeignKey(Parent, related_name='invitations_received') #doc PARENT RECIPIENT
    household = models.ForeignKey(Household) # doc HOUSE HOLD RELATED TO THE INVITATION
    created_at = models.DateField(auto_now_add=True) #doc CREATION DATE
    accepted = models.BooleanField(default=False) #doc ACCEPTED : TRUE OR FALSE




