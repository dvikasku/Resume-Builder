from django.shortcuts import render , HttpResponse , redirect
from home.models import Person , UserOTP
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Email verification
from django.core.mail import send_mail
from verify_email.email_handler import send_verification_email      
from django.contrib.sites.shortcuts import get_current_site     
from django.template.loader import render_to_string      
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode     
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError   
from .utils import generate_token

# Create your views here.
def index(request):
    return render (request , 'home.html')

def logged(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to login first")
        return render (request , 'home.html')
    else:
        return render (request , 'home.html')

# Authanticate APIS
def handleSignUp(request):
    if request.method=="POST":        
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

         # check for errorneous input
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('/')
        if User.objects.filter(username=username).exists():
            messages.error(request, " User name already exist. Please enter unique username")
            return redirect('/')

        if User.objects.filter(email=email).exists():
            messages.error(request, " Email is already register with another username !")
            return redirect('/')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.is_active = False
        myuser.save()

        current_site = get_current_site(request)
        email_subject = 'Activate your account',
        mess = render_to_string('auth/activate.html',
        {
            'myuser': myuser,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        }
        )


        send_mail(
            "Welcome To resume - Verify Your Email",
            mess,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently= False
        )
        messages.success(request, "Please check your email to activate your account ")
        return redirect("/")

    else:
        return HttpResponse("404 - Not found")

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername , password = loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")
    return HttpResponse("login")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

@login_required(login_url='logged')
def resume(request):
    if request.method == 'GET':
        template_name = request.GET.get('template_name', ' ')
        params = {'template_name': template_name}
        print("The resume template name is ", template_name)
        return render(request, 'resume/getData.html', params)
    if request.method == "POST" and request.FILES['image']:
        template_name = request.POST.get('template_name', ' ')
        # personal information
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        linkedin=request.POST.get('linkedIn')
        address=request.POST.get('add')
        dob=request.POST.get('dob')
        phone=request.POST.get('phone')
        about=request.POST.get('about')
        image=request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name,image)
        uploaded_file_url = fs.url(filename)
        person = Person(first_name = first_name,last_name=last_name,gender=gender,email=email,linkedin=linkedin,address=address,dob=dob,phone=phone,about=about,image=image)
        person.save()
        # Academic Details
        ten_board = request.POST.get('ten-board', ' ')
        ten_marks = request.POST.get('ten-marks', ' ')
        twelve_board = request.POST.get('twelve-board', ' ')
        twelve_marks = request.POST.get('twelve-marks', ' ')
        degree = request.POST.get('degree', ' ')
        institute = request.POST.get('institute', ' ')
        cgpa = request.POST.get('cgpa', ' ')
        gre = request.POST.get('gre',' ')
        toefl = request.POST.get('toefl',' ')
        exam = {}
        certificate = {}

        i = 1
        no_of_exam = int(request.POST.get('no-of-exam'))
        # no_of_exam = int(no_of_exam)
        while(no_of_exam > 0):
            exam_name = request.POST.get(f'exam{i}')
            rank = request.POST.get(f'rank{i}')
            if(exam_name != None):
                exam[exam_name] = rank
            i = i+1
            no_of_exam = no_of_exam-1

        i = 1
        no_of_course = int(request.POST.get('no-of-course'))
        while(no_of_course > 0):
            course = request.POST.get(f'course{i}')
            duration = request.POST.get(f'duration{i}')
            if(course != None):
                certificate[course] = duration
            i = i+1
            no_of_course = no_of_course-1

        for x, y in exam.items():
            print(f'Exam: {x} Rank: {y}')
        for x, y in certificate.items():
            print(f'Course: {x} Duration: {y}')

        # WORK Experience
        experience_status = request.POST.get('experience-status')
        exp = {}
        print(experience_status)
        print(type(experience_status))
        if(experience_status == 'fresher'):
            # do nothing as exp is already
            exp = {}
        elif(experience_status == 'experienced'):
            i = 1
            no_of_company = int(request.POST.get('no-of-company'))
            while(no_of_company > 0):
                company_name = request.POST.get(f'company-name{i}')
                job_title = request.POST.get(f'job-title{i}')
                experience = request.POST.get(f'experience{i}')
                if(company_name != None):
                    exp[company_name] = [job_title, experience]
                i = i+1
                no_of_company = no_of_company-1
        for x, y in exp.items():
            print(f'Company: {x} Job-title: {y[0]} Experience: {y[1]}')

        # PROJECT Details
        project_status = request.POST.get('project-status')
        project = {}
        print(project_status)
        print(type(project_status))
        if(project_status == 'noProject'):
            # do nothing as exp is already
            project = {}
        elif(project_status == 'doneProject'):
            i = 1
            no_of_project = int(request.POST.get('no-of-project'))
            print(no_of_project)
            while(no_of_project > 0):
                project_title = request.POST.get(f'project-title{i}')
                print(project_title)
                project_description = request.POST.get(
                    f'project-description{i}')
                skills_used = request.POST.get(f'skills-used{i}')
                if(project_title != None):
                    project[project_title] = [project_description, skills_used]
                i = i+1
                no_of_project = no_of_project-1
        for x, y in project.items():
            print(
                f'Project: {x} Project-Description: {y[0]} Skills Used: {y[1]}')

        # INTERNSHIP Details
        internship_status = request.POST.get('internship-status')
        internship = {}
        print(internship_status)
        print(type(internship_status))
        if(internship_status == 'noInternship'):
            # do nothing as exp is already
            internship = {}
        elif(internship_status == 'doneInternship'):
            i = 1
            no_of_internship = int(request.POST.get('no-of-internship'))
            print(no_of_internship)
            while(no_of_internship > 0):
                internship_title = request.POST.get(f'internship-title{i}')
                internship_duration = request.POST.get(
                    f'internship-duration{i}')
                internship_description = request.POST.get(
                    f'internship-description{i}')
                internship_skills_used = request.POST.get(
                    f'internship-skills-used{i}')
                if(internship_title != None):
                    internship[internship_title] = [
                        internship_description, internship_duration, internship_skills_used]
                i = i+1
                no_of_internship = no_of_internship-1
        for x, y in internship.items():
            print(
                f'Internship: {x} Internship-Description: {y[0]} Internship-Description: {y[1]} Internship-Skills Used: {y[2]}')

        # SKILLS and Abilities
        skills = []
        i = 1
        no_of_skill = int(request.POST.get('no-of-skill'))
        print(no_of_skill)
        while(no_of_skill > 0):
            skill_possesed = request.POST.get(f'skill{i}')
            if(skill_possesed != None):
                skills.append(skill_possesed)
            i = i+1
            no_of_skill = no_of_skill-1
        print(skills)

        # Languages
        langs = []
        i = 1
        no_of_lang = int(request.POST.get('no-of-lang'))
        print(no_of_lang)
        while(no_of_lang > 0):
            lang_possesed = request.POST.get(f'lang{i}')
            if(lang_possesed != None):
                langs.append(lang_possesed)
            i = i+1
            no_of_lang = no_of_lang-1
        print(langs)

        # Hobbies
        hobs = []
        i = 1
        no_of_hob = int(request.POST.get('no-of-hob'))
        print(no_of_hob)
        while(no_of_hob > 0):
            hob_possesed = request.POST.get(f'hob{i}')
            if(hob_possesed != None):
                hobs.append(hob_possesed)
            i = i+1
            no_of_hob = no_of_hob-1
        print(hobs)
        params = {
                # Personal
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'email': email,
                'linkedin': linkedin,
                'dob': dob,
                'address': address,
                'phone': phone,
                'image': image,
                'about' : about,

                # Academic
                'ten_board' : ten_board,
                'ten_marks' : ten_marks,
                'twelve_board': twelve_board,
                'twelve_marks': twelve_marks,
                'degree' : degree,
                'institute' : institute,
                'cgpa' : cgpa,
                'exam' : exam,
                'certificate' :certificate,
                'gre': gre,
                'toefl': toefl,

                #Work,
                'work_experience' : exp,

                #Project,
                'project' : project,

                #Internship,
                'internship':internship,

                #Skills,
                'skills':skills,

                #Languages,
                'langs':langs,

                #Hobbies,
                'hobs':hobs,

                }
        return render(request,f'resume/{template_name}',params)
    return render(request, 'resume/getdata.html')


def about(request):
    return render(request,"about.html")

# Email verification
def get(request,uidb64,token):
        print(uidb64,token)
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except Exception as identifier:
            myuser = None
        if myuser is not None and generate_token.check_token(myuser,token):
            myuser.is_active = True
            myuser.save()
            messages.success(request, "Account activate Successfully. Now you can log in your account!")
            return redirect("/")
        return render(request,'auth/activate_failed.html', {"myuser": myuser})