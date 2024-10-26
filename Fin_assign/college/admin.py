from django.contrib import admin

# Register your models here.
from college.models import Student, Staff_Lecturer, Room, MeetingType, Ticket

admin.site.register(Student)
admin.site.register(Staff_Lecturer)
admin.site.register(Room)
admin.site.register(MeetingType)
admin.site.register(Ticket)