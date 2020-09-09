from django.db import models

# Create your models here.

class Player(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    employer = models.IntegerField()
    full_name = models.CharField(max_length=60)

    def __str__(self):
        return self.email

class Employer(models.Model):
    company_name = models.CharField(max_length=60)

class Modules(models.Model):
    code = models.CharField(max_length=10)
    case = models.IntegerField()
    creation_date = models.DateField()

class PlaySession(models.Model):
    employee_email = models.CharField(max_length=30)
    module_id = models.IntegerField()
    date_taken = models.DateField(auto_now=True)
    score = models.IntegerField()
    success = models.BooleanField()
    time_taken = models.IntegerField()
    
class Employee(models.Model):
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
