from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from .serializers import TeamSerializer, userSerializer
from .models import UserToken
from django.contrib.auth import authenticate, login
from .models import Team, submissiontime, contact, submissiontime


# Create your views here.
def home(request):
    user = request.user
    context = {'user': user}
    # check if team of user is created

    try:
        context['registration']= submissiontime.objects.get(tag='closingtime').submission_time.strftime("%B %d, %Y")
        context['idea']= submissiontime.objects.get(tag='idea').submission_time.strftime("%B %d, %Y")
        context['selection']= submissiontime.objects.get(tag='Top 40').submission_time.strftime("%B %d, %Y")
        context['hackathon']= submissiontime.objects.get(tag='hackathon').submission_time
        context['hackathon_end']= submissiontime.objects.get(tag='hackathon-end').submission_time
        team = Team.objects.get(leader=user)
        context['team'] = team
    except Exception as e:
        pass
    return render(request, "MainApp/index.html", context)


def register_user(request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    
    if not email or email.strip() == '':
        return JsonResponse({'error': 'Email is required'}, status=404)
    
    try:
        user = User.objects.get(username=email)
        user.is_active = False  # Deactivate the account
        user.save()
        created = False
    except User.DoesNotExist:
        user = User.objects.create(username=email, email=email, first_name=name)
        user.is_active = False  # Deactivate the account
        user.save()
        created = True
    
    # Generate a token for the user or regenerate if one exists
    user_token, _ = UserToken.objects.get_or_create(user=user)
    user_token.regenerate_token()  # Create or regenerate the token
    
    # Send the email (whether new user or existing user)
    domain = request.get_host()  # Get the domain dynamically
    protocol = 'https' if request.is_secure() else 'http'  # Check for HTTP/HTTPS

    mail_subject = 'Activate your account.'
    activation_link = f"{protocol}://{domain}/activate/{user.pk}/{user_token.token}/"

    # Render email content with context
    message = render_to_string('email_verification.html', {
        'user': user,
        'activation_link': activation_link,
    })

    # Create and send an email message as HTML
    email_message = EmailMessage(
        mail_subject,
        message,
        'your_email@gmail.com',  # From email
        [email],                 # To email
    )
    email_message.content_subtype = 'html'  # Set content type to HTML
    email_message.send()

    if created:
        return JsonResponse({'message': 'Verification link sent to your email'}, status=201)
    else:
        return JsonResponse({'message': 'Your account was deactivated and a new activation link was sent to your email'}, status=200)
    

def activate_user(request, uidb64, token):
    try:
        user = User.objects.get(pk=uidb64)
        user_token = UserToken.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, UserToken.DoesNotExist):
        return render(request,'MainApp/activation.html', {'message': 'Invalid activation link!'})

    if user_token.token == token:
        if not user_token.is_token_expired():  # Check if token is not expired
            if not user.is_active:
                user.is_active = True
                new_password = get_random_string(length=12)
                user.set_password(new_password)
                user.save()

                # Send the new password via email
                mail_subject = 'Your account has been activated'
                message = f"Hi {user.first_name},\n\nYour account has been activated. Your new password is: {new_password}\n\nPlease use this password to log in."
                send_mail(
                    mail_subject, 
                    message, 
                    'manojpatil9147@ieee.org',  # From email
                    [user.email],               # To email
                    fail_silently=False
                )
                
                return render(request, 'MainApp/activation.html', {'message': 'Account activated successfully! Check your email for the new password.'})
            else:
                return render(request, 'MainApp/activation.html', {'message': 'Account already activated!'})
        else:
            return render(request, 'MainApp/activation.html', {'message': 'Activation link expired!'})
    else:
        return render(request, 'MainApp/activation.html', {'message': 'Invalid activation link!'})

    
def create_team(request):
    print(request.POST)
    # get user
    user = User.objects.get(username=request.user.username)
    try:
        team = Team.objects.get(leader=user)
    except Exception as e:
        team = None
    if team:
        return JsonResponse({'error': 'Team already exists'}, status=400)
    userserializer = userSerializer(user)
    data={
        'name':request.POST.get('TeamName'),
        'leader_contact':request.POST.get('phoneno'),
        'member1_name':request.POST.get('member1'),
        'member2_name':request.POST.get('member2'),
        'member3_name':request.POST.get('member3'),
    }
    team = Team.objects.create(name=data['name'],leader=user,leader_contact=data['leader_contact'],member1_name=data['member1_name'],member2_name=data['member2_name'],member3_name=data['member3_name'])
    team.save()
    return redirect('MainApp:home')
    

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            print("success")
            return JsonResponse({'data':'success'}, status=200)
        else:
            return JsonResponse(status=401)
    return JsonResponse(status=404)


def get_form_closing_time(request):
    closingtime = submissiontime.objects.get(tag='closingtime')
    return JsonResponse({'form_closing_time':closingtime.submission_time}, status=200)

def contactview(request):
    if request.method == 'POST':
        email = request.POST.get('email_address')
        message = request.POST.get('message')
        comment=contact.objects.create(email=email,message=message)
        return render(request,'MainApp/activation.html', {'message': 'Your message has been sent successfully!'})
    return render(request,'MainApp/activation.html',{'message':"message couldnt not be send!!"})