from django.shortcuts import render,redirect
from django.http import HttpRequest
from accounts.models import User, PendingUser, Token, TokenType
from django.contrib import messages, auth
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
from common.tasks import send_email
from django.contrib.auth import get_user_model
from accounts.decorators import redirect_authenticated_users

@redirect_authenticated_users
def home(request: HttpRequest):
    return render(request, 'home.html')


@redirect_authenticated_users
def register(request: HttpRequest):
    if request.method == "POST":
        print("POST data:", request.POST)  # Debug
        email : str =request.POST["email"]
        fullname : str =request.POST["fullname"]
        password : str =request.POST["password"]
        cleaned_email = email.lower()#to ensure uniformitys
        # Validate required fields
        if not all([email, fullname, password]):
            messages.error(request, "All fields are required")
            return redirect("register")
        
        #checking if email is registered on the plateform
        if User.objects.filter(email=cleaned_email).exists():
            messages.error(request, "This email already exist")
            return redirect("register")
        else:
            verification_code = get_random_string(6)
            PendingUser.objects.update_or_create(
                email=cleaned_email,
                fullname=fullname,
                defaults={
                    "password": make_password(password),
                    "verification_code": verification_code,
                    "created_at": datetime.now(timezone.utc)
                }
            )
            #send email
            send_email(
                "Verify your Account",
                [cleaned_email],
                "emails/email_verification_template.html",
                context= {"code": verification_code}
                ) 
            #function to send email to the use and let the user know
            messages.success(request, f"Verification code sent to {cleaned_email}")
            return render(request, "verify_account.html", context={"email": cleaned_email, "fullname": fullname})
    else:
        return render(request, "register.html")


def verify_account(request: HttpRequest):
    if request.method == "POST":
        code: str = request.POST["code"]
        fullname: str = request.POST["fullname"]
        email: str = request.POST["email"]
        pending_user = PendingUser.objects.filter(
            verification_code = code, email=email, fullname=fullname
        ).first()
        if pending_user and pending_user.is_valid():#remember we hava a method called is_valid used to check if verification code i valid or not
            user=User.objects.create(email=pending_user.email, fullname=pending_user.fullname, password=pending_user.password)
            pending_user.delete()
            auth.login(request, user)
            messages.success(request, "Account verified. You are now logged in")
            return redirect('home')
            
        else:
            messages.error(request, "Invalid or Expired verification code")
            return render(request, 'verify_account.html',{"email": email, "fullname": fullname}, status=400)
            
            
            
def login(request: HttpRequest):
    if request.method == "POST":#if it a post request we need to accept an email and a password
        email: str = request.POST.get("email")
        password: str = request.POST.get("password")
        
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            messages.success(request, "You are now logged in Welcome.")
            return redirect('home')
        
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("login")        
    else:
        return render(request, 'login.html')
    
def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request, "Successfully Logged-Out")
    return redirect("home")#we are redirecting the user to the home view


def send_password_reset_link(request: HttpRequest):
    if request.method == "POST":
        email:str = request.POST.get("email", "")
        user = get_user_model().objects.filter(email=email.lower()).first
        if user:
            #token, created
            token, _ = Token.objects.update_or_create(#this method is used bc we don't want multiple instances of token for the same user od token type it returns the created instance and a boolean
                user=user,
                token_type=TokenType.PASSWORD_RESET,
                defaults={
                    "token": get_random_string(6),
                    "created_at":datetime.now(timezone.utc)
                }
            )
            #sending token to the user
            email_data = {
                "email":email.lower(),
                "token": token.token
            }            
            send_email(
                "Your password reset link",
                [email],
                "emails/password_reset_template.html",
                email_data
            )
            messages.success(request, "Reset link  sent to your email")
            return redirect("reset_password_via_email")
        else:
            messages.error(request, "Email not found")
            return redirect("reset_password_via_email")
        
        
    else:
        return render(request, "forgot_password.html")
    
    
def verify_password_reset_link(request: HttpRequest):
    email = request.GET('email')
    reset_token = request.GET.get('token')
    
    #checking if we can find the token and the email in the database
    token = Token.objects.filter(#double underscore lookup used to query the related models
        user__email=email, token=reset_token, token_type=TokenType.PASSWORD_RESET
    ).first()
    if not token or not token.is_valid():
        messages.error(request, "Invalid or reset link")
        return redirect("reset_password_via_email")        
        
    else:
        return render(request, 'set_new_password_using_reset_token.html',
                      context={"email":email, "token":reset_token})
        
def set_new_password_using_reset_link(request: HttpRequest):
    if request.method == "POST":
        password1: str =request.POST.get('password1')
        password2: str =request.POST.get('password2')
        email: str =request.POST.get('email')#also accepting the hidden fields
        reset_token: str =request.POST.get('token')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'set_new_password_using_reset_token.html', 
                          {"email":email, "token":reset_token})
        token: Token = Token.objects.filter(
            token=reset_token, token_type=TokenType.PASSWORD_RESET, user__email=email
        ).first()
        if not token or not token.is_valid():
            
            messages.errors(request, 'Invalid or expired reset link')
            return redirect('reset_password_email')
        token.reset_user_password(password1)
        token.delete()
        messages.success(request, "Password changed successfully.")
        return redirect('login')
    
#a decorator is a function that takes an other function as an argument and enhances its behaviour