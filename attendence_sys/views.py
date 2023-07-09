""""""
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views.generic import ListView
from .models import Student
from .models import Attendence
from django.template.loader import get_template
from io import BytesIO
# import xhtml2pdf.pisa as pisa

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Student, Attendence
from .filters import AttendenceFilter
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student
# from django.views.decorators import gzip

from .recognizer import Recognizer
from datetime import date



def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Students added successfully.')
            # return redirect('success')  # Redirect to a success page or desired URL
    else:
        form = StudentForm()
    return render(request, 'attendence_sys/add_student.html', {'form': form})


class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'

@login_required(login_url = 'login')
def home(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        # print(request.POST)
        stat = False 
        try:
            student = Student.objects.get(registration_id = request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id '+request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm':studentForm}
    return render(request, 'attendence_sys/home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendence_sys/login.html', context)

@login_required(login_url = 'login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def updateStudentRedirect(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(registration_id = reg_id, branch = branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form':updateStudentForm, 'prev_reg_id':reg_id, 'student':student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(request, 'attendence_sys/student_update.html', context)
def updateStudent(request, student_id):
    student = get_object_or_404(Student, registration_id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
        form.fields['firstname'].required = False
        form.fields['lastname'].required = False
        form.fields['student_id'].required = False
        form.fields['branch'].required = False
        form.fields['year'].required = False
        form.fields['section'].required = False
        
    context = {
        'form': form,
        'student': student
    }
    return render(request, 'attendence_sys/student_update.html', context)


@login_required(login_url = 'login')
def takeAttendence(request):
    if request.method == 'POST':
        details = {
            'branch':request.POST['branch'],
            'year': request.POST['year'],
            'section':request.POST['section'],
            'period':request.POST['period'],
            'faculty':request.user.faculty
            }
        if Attendence.objects.filter(date = str(date.today()),branch = details['branch'], year = details['year'], section = details['section'],period = details['period']).count() != 0 :
            messages.error(request, "Attendence already recorded.")
            return redirect('home')
        else:
            students = Student.objects.filter(branch = details['branch'], year = details['year'], section = details['section'])
            names = Recognizer(details)
            for student in students:
                if str(student.registration_id) in names:
                    attendence = Attendence(Faculty_Name = request.user.faculty, 
                    Student_ID = str(student.registration_id), 
                    period = details['period'], 
                    branch = details['branch'], 
                    year = details['year'], 
                    section = details['section'],
                    status = 'Present')
                    attendence.save()
                else:
                    attendence = Attendence(Faculty_Name = request.user.faculty, 
                    Student_ID = str(student.registration_id), 
                    period = details['period'],
                    branch = details['branch'], 
                    year = details['year'], 
                    section = details['section'])

                    attendence.save()
            attendences = Attendence.objects.filter(date = str(date.today()),branch = details['branch'], year = details['year'], section = details['section'],period = details['period'])
            context = {"attendences":attendences, "ta":True}
            messages.success(request, "Attendence taking Success")
            return render(request, 'attendence_sys/attendence.html', context)        
    context = {}
    return render(request, 'attendence_sys/home.html', context)

def searchAttendence(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter':myFilter, 'attendences': attendences, 'ta':False}
    return render(request, 'attendence_sys/attendence.html', context)


def facultyProfile(request):
    faculty = request.user.faculty
    form = FacultyForm(instance = faculty)
    context = {'form':form}
    return render(request, 'attendence_sys/facultyForm.html', context)


@login_required(login_url='login')
def deleteStudent(request, student_id):
    try:
        student = Student.objects.get(registration_id=student_id)
        student.delete()
        messages.success(request, 'Student deleted successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
    
    return redirect('student_list')




# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         ret,image = self.video.read()
#         ret,jpeg = cv2.imencode('.jpg',image)
#         return jpeg.tobytes()


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield(b'--frame\r\n'
#         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @gzip.gzip_page
# def videoFeed(request):
#     try:
#         return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         print("aborted")

# def getVideo(request):
#     return render(request, 'attendence_sys/videoFeed.html')

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


# def getPdf(request, *args, **kwargs):
#     context={}
    
#     pdf = render_to_pdf('attendence_sys/attendence.html',context_dict=context)
#     return HttpResponse(pdf, content_type='application/pdf')

def generate_pdf(request):
    # Get the data you want to display in the PDF
    # For example, if you have a table, fetch the data from your database or other sources

    # Render the template with the data
    template = get_template('attendence_sys/attendence.html')
    # context ={}
    context = {'data': Attendence}
    context['Attendence'] =Attendence.objects.all()
    # Pass your data to the template
    rendered_html = template.render(context)

    # Create a BytesIO object to receive the PDF output
    result = BytesIO()

    # Create the PDF object
    pdf = pisa.CreatePDF(BytesIO(rendered_html.encode('UTF-8')), result)

    # Check if PDF creation was successful
    if not pdf.err:
        # Set the return type of the response as PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="AttendanceReport.pdf"'

        # Write the PDF content to the response
        response.write(result.getvalue())

        # Close the PDF object
        return response

    return HttpResponse('Error generating PDF', status=500)
