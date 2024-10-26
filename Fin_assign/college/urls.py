from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index , name="index"),
    path('login/', views.user_login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('sign_up/student/', views.student_sign_up, name='student_sign_up'),
    path('sign_up/lecturer/', views.lecturer_sign_up, name='lecturer_sign_up'),
    path('student/detail/', views.student_detail, name='student_detail'),
    path('lecturer-detail/', views.lecturer_detail, name='lecturer_detail'),
    path('rooms/student', views.room_student, name='room_student'),
    path('rooms/lecturer', views.room_lecturer, name='room_lecturer'),
    path('add-room/', views.add_room, name='add_room'),
    path('rooms/update/<str:roomID>/', views.update_room, name='update_room'),
    path('rooms/delete/<str:roomID>/', views.delete_room, name='delete_room'),
    path('meetings/lecturer', views.meeting_lecturer, name='meeting_lecturer'),
    path('meeting/student', views.meeting_student, name='meeting_student'),
    path('meeting-types/add/', views.add_meeting_type, name='add_meeting_type'),
    path('meeting-type/update/<str:typeID>/', views.update_meeting_type, name='update_meeting_type'),
    path('meeting-type/delete/<str:typeID>/', views.delete_meeting_type, name='delete_meeting_type'),
    path('tickets/student', views.ticket_list_student, name='ticket_list_student'),
    path('tickets/lecturer/', views.ticket_list_lecturer, name='ticket_list_lecturer'),
    path('tickets/add/', views.add_ticket, name='add_ticket'),  # Add this lines
    path('tickets/update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),  # Add this line
    path('tickets/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),  # Add this line
    path('student/tickets/', views.ticket_list_student_view, name='ticket_list_student'),
    path('lecturer/tickets/', views.ticket_list_lecturer_view, name='ticket_list_lecturer'),

]