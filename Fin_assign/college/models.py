from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Student(models.Model):
    studentID = models.CharField(max_length=20, primary_key=True)
    studentName = models.CharField(max_length=100)
    studentAge = models.IntegerField()
    studentEmail = models.CharField(max_length=50, null=True)
    studentPS = models.CharField(max_length=50, null=True)

    def set_password(self, password):
        self.studentPS = make_password(password)

    def check_password(self, password):
        return check_password(password, self.studentPS)

class Staff_Lecturer(models.Model):
    slID = models.CharField(max_length=20, primary_key=True)
    slName = models.CharField(max_length=100)
    slAge = models.IntegerField()
    slEmail = models.CharField(max_length=50)
    slPS = models.CharField(max_length=50, null=True)
    slStatus = models.CharField(max_length=10)

    def set_password(self, password):
        self.slPS = make_password(password)

    def check_password(self, password):
        return check_password(password, self.slPS)

class Room(models.Model):
    roomID = models.CharField(max_length=10, primary_key=True)
    roomBlock = models.CharField(max_length=15)
    roomCapacity = models.IntegerField()

class MeetingType(models.Model):
    typeID = models.CharField(max_length=10, primary_key=True)
    typeName = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True)

class Ticket(models.Model):
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    slID = models.ForeignKey(Staff_Lecturer, on_delete=models.CASCADE)
    roomID = models.ForeignKey(Room, on_delete=models.CASCADE)
    meetingType = models.ForeignKey(MeetingType, on_delete=models.CASCADE, null=True) 
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, null=True)
    comment = models.TextField(max_length=100, null=True)