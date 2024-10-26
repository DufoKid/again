from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from django.db.models import Q
from college.models import Student, Staff_Lecturer, Room,  MeetingType, Ticket


# Create your views here.
def index(request):
    return render (request , "main.html")

def sign_up(request):
    return render(request, 'sign_up.html')

def lecturer_detail(request):
    # Ensure the user is logged in and is a lecturer
    if request.session.get('role') == 'lecturer':
        user_id = request.session.get('user_id')
        try:
            lecturer = Staff_Lecturer.objects.get(slID=user_id)  # Get the logged-in lecturer's details
            return render(request, 'lecturer_detail.html', {'lecturer': lecturer})
        except Staff_Lecturer.DoesNotExist:
            return HttpResponse('Lecturer does not exist.')
    else:
        return HttpResponse('Unauthorized access.')

def student_detail(request):
    # Ensure the user is logged in and is a student
    if request.session.get('role') == 'student':
        user_id = request.session.get('user_id')
        try:
            student = Student.objects.get(studentID=user_id)  # Get the logged-in student's details
            return render(request, 'student_detail.html', {'student': student})
        except Student.DoesNotExist:
            return HttpResponse('Student does not exist.')
    else:
        return HttpResponse('Unauthorized access.')
    

def student_sign_up(request):
    if request.method == 'POST':
        studentID = request.POST.get('studentID')
        studentName = request.POST.get('studentName')
        studentAge = request.POST.get('studentAge')
        studentEmail = request.POST.get('studentEmail')
        studentPS = request.POST.get('studentPS')

        # Check if studentID or studentEmail already exists (validation)
        if Student.objects.filter(studentID=studentID).exists():
            return HttpResponse('Student ID already exists.')
        if Student.objects.filter(studentEmail=studentEmail).exists():
            return HttpResponse('Student Email already exists.')

        # Create new Student object
        student = Student(studentID=studentID, studentName=studentName, studentAge=studentAge, studentEmail=studentEmail, studentPS=studentPS)
        student.save()

        return redirect('index')  # Redirect to student details after sign-up
    return render(request, 'student_signup.html')

def lecturer_sign_up(request):
    if request.method == 'POST':
        slID = request.POST.get('slID')
        slName = request.POST.get('slName')
        slAge = request.POST.get('slAge')
        slEmail = request.POST.get('slEmail')
        slPS = request.POST.get('slPS')
        slStatus = request.POST.get('slStatus')

        # Check if lecturerID or lecturerEmail already exists (validation)
        if Staff_Lecturer.objects.filter(slID=slID).exists():
            return HttpResponse('Lecturer ID already exists.')
        if Staff_Lecturer.objects.filter(slEmail=slEmail).exists():
            return HttpResponse('Lecturer Email already exists.')

        # Create new Lecturer object
        lecturer = Staff_Lecturer(slID=slID, slName=slName, slAge=slAge, slEmail=slEmail, slPS=slPS, slStatus=slStatus)
        lecturer.save()

        return redirect('index')  # Redirect to lecturer details after sign-up
    return render(request, 'lecturer_signup.html')

def user_login(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Authenticate manually based on the role
        if role == 'student':
            try:
                student = Student.objects.get(studentID=userID)
                if password == student.studentPS:  # Direct password comparison
                    # Set session for student
                    request.session['user_id'] = student.studentID
                    request.session['role'] = 'student'

                    # Redirect to student detail page
                    return redirect('student_detail')
                else:
                    return HttpResponse('Invalid login details')
            except Student.DoesNotExist:
                return HttpResponse('Student does not exist')

        elif role == 'lecturer':
            try:
                lecturer = Staff_Lecturer.objects.get(slID=userID)
                if password == lecturer.slPS:  # Direct password comparison
                    # Set session for lecturer
                    request.session['user_id'] = lecturer.slID
                    request.session['role'] = 'lecturer'

                    # Redirect to lecturer detail page
                    return redirect('lecturer_detail')
                else:
                    return HttpResponse('Invalid login details')
            except Staff_Lecturer.DoesNotExist:
                return HttpResponse('Lecturer does not exist')

    return render(request, 'main.html')

def room_student(request):
    # Retrieve all room objects from the database
    rooms = Room.objects.all()
    return render(request, 'room_student.html', {'rooms': rooms})

def room_lecturer(request):
    rooms = Room.objects.all()  # Retrieve all Room objects
    return render(request, 'room_lecturer.html', {'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        # Capture data from the POST request
        room_id = request.POST.get('roomID')
        room_block = request.POST.get('roomBlock')
        room_capacity = request.POST.get('roomCapacity')

        # Basic validation (you can add more validation if needed)
        if room_id and room_block and room_capacity:
            # Create a new Room object and save it to the database
            new_room = Room(roomID=room_id, roomBlock=room_block, roomCapacity=room_capacity)
            new_room.save()

            # Redirect to the room list page after saving
            return redirect('room_lecturer')  # Assuming 'room_list' is the name of the URL for listing rooms
        else:
            # If validation fails, re-render the form with an error message
            return render(request, 'add_room.html', {
                'error': 'All fields are required.'
            })
    
    # For GET request, simply render the empty form
    return render(request, 'room_add.html')


def update_room(request, roomID):
    # Get the room object by its roomID, or return a 404 if it doesn't exist
    room = get_object_or_404(Room, roomID=roomID)
    
    if request.method == 'POST':
        # Get updated data from the form submission
        room.roomBlock = request.POST.get('roomBlock')
        room.roomCapacity = request.POST.get('roomCapacity')
        
        # Save the updated room to the database
        room.save()
        
        # Redirect to the room list after saving
        return redirect('room_lecturer')
    
    # Render the update form with the current room details
    return render(request, 'room_update.html', {'room': room})

def delete_room(request, roomID):
    if request.method == 'POST':
        room = get_object_or_404(Room, roomID=roomID)
        room.delete()
        return redirect('room_lecturer')  # Redirect to the room list after deleting
    return HttpResponseNotAllowed(['POST'])

def meeting_student(request):
    # Retrieve all meeting type objects from the database
    meeting_types = MeetingType.objects.all()
    return render(request, 'meeting_student.html', {'meeting_types': meeting_types})

def meeting_lecturer(request):
    # Fetch all the meeting types from the database
    meeting_types = MeetingType.objects.all()
    # Pass the data to the template
    return render(request, 'meeting_lecturer.html', {'meeting_types': meeting_types})

def add_meeting_type(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        typeID = request.POST.get('typeID')
        typeName = request.POST.get('typeName')
        description = request.POST.get('description')

        # Create a new MeetingType object and save it to the database
        new_meeting_type = MeetingType(typeID=typeID, typeName=typeName, description=description)
        new_meeting_type.save()

        # Redirect to the meeting type list page after saving
        return redirect('meeting_list')
    
    # Render the form template
    return render(request, 'meeting_add.html')

def update_meeting_type(request, typeID):
    meeting_type = get_object_or_404(MeetingType, pk=typeID)
    
    if request.method == 'POST':
        meeting_type.typeName = request.POST.get('typeName')
        meeting_type.description = request.POST.get('description')
        meeting_type.save()
        return redirect('meeting_lecturer')  # Redirect to the list after updating
    
    return render(request, 'meeting_update.html', {'meeting_type': meeting_type})

def delete_meeting_type(request, typeID):
    meeting_type = get_object_or_404(MeetingType, pk=typeID)
    
    if request.method == 'POST':
        meeting_type.delete()  # Delete the meeting type
        return redirect('meeting_list')  # Redirect to the list after deleting

    return redirect('meeting_list')

def ticket_list_student(request):
    # Retrieve all ticket objects from the database
    tickets = Ticket.objects.select_related(
        'studentID', 'slID', 'roomID', 'meetingType'
    ).all()
    return render(request, 'ticketing_student.html', {'tickets': tickets})

def ticket_list_lecturer(request):
    # Retrieve all ticket objects from the database
    tickets = Ticket.objects.select_related(
        'studentID', 'slID', 'roomID', 'meetingType'
    ).all()
    
    return render(request, 'ticketing_lecturer.html', {'tickets': tickets})

def add_ticket(request):
    if request.method == 'POST':
        student_id = request.POST.get('studentID')
        sl_id = request.POST.get('slID')
        room_id = request.POST.get('roomID')
        meeting_type = request.POST.get('meetingType')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')
        comment = request.POST.get('comment')

        # Create and save the ticket
        ticket = Ticket(
            studentID=Student.objects.get(studentID=student_id),
            slID=Staff_Lecturer.objects.get(slID=sl_id),
            roomID=Room.objects.get(roomID=room_id),
            meetingType=MeetingType.objects.get(typeID=meeting_type),
            date=date,
            time=time,
            status=status,
            comment=comment
        )
        ticket.save()
        return redirect('ticket_list_student')  # Redirect after saving

    # Get all the necessary data for the dropdowns
    students = Student.objects.all()
    lecturers = Staff_Lecturer.objects.all()
    rooms = Room.objects.all()
    meeting_types = MeetingType.objects.all()

    return render(request, 'ticketing_add.html', {
        'students': students,
        'lecturers': lecturers,
        'rooms': rooms,
        'meeting_types': meeting_types
    })

def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    students = Student.objects.all()
    lecturers = Staff_Lecturer.objects.all()
    rooms = Room.objects.all()
    meeting_types = MeetingType.objects.all()

    if request.method == 'POST':
        # Update ticket logic here
        ticket.studentID_id = request.POST.get('studentID')
        ticket.slID_id = request.POST.get('slID')
        ticket.roomID_id = request.POST.get('roomID')
        ticket.meetingType_id = request.POST.get('meetingType')
        ticket.date = request.POST.get('date')
        ticket.time = request.POST.get('time')
        ticket.status = request.POST.get('status')
        ticket.comment = request.POST.get('comment')
        ticket.save()
        return redirect('ticket_list_lecturer')

    return render(request, 'ticketing_update.html', {
        'ticket': ticket,
        'students': students,
        'lecturers': lecturers,
        'rooms': rooms,
        'meeting_types': meeting_types,
    })

def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list_lecturer')
    
def ticket_list_student_view(request):
    search_query = request.GET.get('q', '')
    if search_query:
        tickets = Ticket.objects.filter(
            Q(id__icontains=search_query) | 
            Q(studentID__studentName__icontains=search_query) | 
            Q(slID__slName__icontains=search_query) | 
            Q(roomID__roomBlock__icontains=search_query) | 
            Q(roomID__roomID__icontains=search_query) | 
            Q(meetingType__typeName__icontains=search_query) | 
            Q(date__icontains=search_query) | 
            Q(time__icontains=search_query) | 
            Q(status__icontains=search_query) | 
            Q(comment__icontains=search_query)
        )
    else:
        tickets = Ticket.objects.all()

    context = {
        'tickets': tickets,
    }
    
    return render(request, 'ticketing_student.html', context)

def ticket_list_lecturer_view(request):
    search_query = request.GET.get('q', '')
    if search_query:
        tickets = Ticket.objects.filter(
            Q(id__icontains=search_query) | 
            Q(studentID__studentName__icontains=search_query) | 
            Q(slID__slName__icontains=search_query) | 
            Q(roomID__roomBlock__icontains=search_query) | 
            Q(roomID__roomID__icontains=search_query) | 
            Q(meetingType__typeName__icontains=search_query) | 
            Q(date__icontains=search_query) | 
            Q(time__icontains=search_query) | 
            Q(status__icontains=search_query) | 
            Q(comment__icontains=search_query)
        )
    else:
        tickets = Ticket.objects.all()

    context = {
        'tickets': tickets,
    }
    
    return render(request, 'ticketing_lecturer.html', context)
