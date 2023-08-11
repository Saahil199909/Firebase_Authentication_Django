from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from Firebase_Auth.settings import authe,database  # Import settings
import firebase_admin
from firebase_admin import credentials,db,auth


# Initialize the Firebase Admin SDK with the serviceAccountKey.json file
cred = credentials.Certificate('/data/IMP_Projects/Django_Projects/FirebaseAuthentication/authentication-web-application-firebase-adminsdk-g3or9-cbc6e22bd8.json')
firebase_admin.initialize_app(cred, {
   'databaseURL':"https://authentication-web-application-default-rtdb.firebaseio.com"
})

# Get a reference to the root of the database
db_ref = db.reference('/')


def is_email_registered(email):
    try:
        user_list = auth.list_users() 
        for user in user_list.users:
            if user.email == email:
                return True
        
    except Exception as e:
        # Handle exceptions
        return False


def signIn(request):
    return render(request,"login.html")

def signUp(request):
    return render(request,"signup.html")


def home(request):
    return render(request,"homepage.html")
 

def postsignIn(request):
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,passw)
        user_data = db_ref.child('data').get()
        matching_user = None
        for user_key, user_info in user_data.items():
             if user_info.get('email') == email:
                 matching_user = user_info
                 return render(request,"homepage.html", {'matching_user': matching_user})
                 break
        
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"login.html",{"message":message})

 
def logout(request):
    return render(request,"login.html")
 

def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    conpass = request.POST.get("pass-repeat")
    name = request.POST.get('name')
    dob =  request.POST.get('dob')
    location =  request.POST.get('location')
    number =  request.POST.get('number')
    try:
        if is_email_registered(email) is True:
            message="EmailID Already Exists, Try Another EmailID"
            return render(request,"login.html",{"message":message}) 
        else:
            if passs == conpass:
                 
                user = authe.create_user_with_email_and_password(email,passs)
                user_data = {"username": name,"email": email,"dob":dob,"location":location,"number":number}
                db_ref.child('data').push(user_data)
                user_data = db_ref.child('data').get()
                matching_user = None
                for user_key, user_info in user_data.items():
                    if user_info.get('email') == email:
                        matching_user = user_info
                        return render(request,"homepage.html", {'matching_user': matching_user})
                        break
            else:
                message="Password and confirm Password Dont Match! Please ChecK "
                return render(request,"signup.html",{"message":message})

    except:
        return render(request, "signup.html")

def reset(request):
	return render(request, "reset.html")

def postReset(request):
	email = request.POST.get('email')
	try:
		authe.send_password_reset_email(email)
		message = "A email to reset password is successfully sent"
		return render(request, "reset.html", {"msg":message})
	except:
		message = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "reset.html", {"msg":message})


