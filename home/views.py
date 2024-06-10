from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Post
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile


# Create your views here.
def home(request):
    return render(request,"home/home.html")


 

def contact(request):
    
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        desc=request.POST["desc"]
        if len(name)<2 or len(email) < 4 or len(phone)==0 or len(desc) < 4:
           messages.error(request,"Please fill the details correctly")
      
        else:
          contact=Contact(name=name,email=email,phone=phone,desc=desc)
          contact.save()
          messages.success(request,"Your message has been successfully sent")
    return render(request,"home/contact.html")


def search(request):
    query=request.GET['query']
    if len(query)>78:
        allpost=Post.objects.none()
    else:
        allpostitle= Post.objects.filter(title__icontains=query)
        allpostcontent= Post.objects.filter(content__icontains=query)
        allpost=allpostitle.union(allpostcontent)

    if allpost.count()==0:
    # if len(allpost)==0:
        messages.warning(request,"No search result found.Please refine your query")
    params={"allpost":allpost,"query":query}
    return render(request, 'home/search.html', params)

# We can also do this allpost.count like this
    # if len(query)>78:
    #     allpost=[]
        # if len(allpost)==0:
        # messages.warning(request,"No search result found.Please refine your query")
    
def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        pass1=request.POST.get("pass1")
        pass2=request.POST.get("pass2")

        if len(username)<10:
          messages.error(request,"Your username must be in under 10 characters")
          return redirect("home")
        if not username.isalnum():
          messages.error(request,"Your username contains only numbers and alphabets")
          return redirect("home")
        if pass1!=pass2:
          messages.success(request,"Passwords donot match")
          return redirect("home")
        user_obj= User.objects.filter(email=email)
        if user_obj.exists():
            messages.error(request,"email already exist")
            return redirect("home")

        user_obj=User.objects.create_user(username=username,email=email)
        user_obj.set_password(pass1)
        user_obj.first_name=fname
        user_obj.last_name=lname
        user_obj.save()
        
        messages.success(request,"Your account hase been created successfully, check your email to verify your account")
        return HttpResponseRedirect(request.path_info)
             
    return render (request,"home/home.html")

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')
        user_obj=User.objects.filter(username=loginusername)
        if not user_obj.exists():
                messages.error(request,"ACount not found")
                return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
                messages.error(request,"ACount not verified")
                return HttpResponseRedirect(request.path_info)


        user_obj=authenticate(username= loginusername, password= loginpassword)
        if user_obj:
            login(request, user_obj)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return render(request,"home/home.html")

    # return HttpResponse("login")
def activate_email(request, email_token):
    try:
        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        messages.success(request, "Account verrified")
        return redirect("home")
    except  Exception as e:
        return HttpResponse("invalid token") 

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
