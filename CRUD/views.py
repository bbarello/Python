from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Users, Trips
import bcrypt

# Create your views here.
def login_index(request):

    return render(request, 'login.html')

# Function to handle registration
def register_user(request):
    all_errors = Users.objects.validator(request.POST)

    if len(all_errors) > 0:
        for _, val in all_errors.items():
            messages.error(request, val)
        return redirect('/')

    password = request.POST['registered_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    try:
        created_user = Users.objects.create(
            first_name = request.POST['registered_first_name'],
            last_name = request.POST['registered_last_name'],
            email = request.POST['registered_email'],
            password = pw_hash
        )
    except:
        messages.error(request, "You can't use that email address.")
        return redirect("/")
        
    request.session['user_id'] = created_user.id

    return redirect('/dashboard')

# Functions for handling login
def login_user(request):
    user_list = Users.objects.filter(email=request.POST['login_email'])
    if len(user_list) == 0:
        messages.error(request, "Please check your email/password")
        return redirect("/")

    if not bcrypt.checkpw(request.POST['login_password'].encode(), user_list[0].password.encode()):
        print("failed password")
        messages.error(request, "Please check your email/password")
        return redirect("/")

    request.session['user_id'] = user_list[0].id
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")

def dashboard(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect("/")
    
    all_trips = Trips.objects.all()
    for trip in all_trips:
        trip.start_date = trip.start_date.strftime("%m/%d/%Y")
        trip.end_date = trip.end_date.strftime("%m/%d/%Y")

    context = {
        "logged_user": Users.objects.get(id=request.session["user_id"]),
        "all_trips": all_trips
    }
    return render(request, "index.html", context)

def new(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect("/")
    
    context = {
        "logged_user": Users.objects.get(id=request.session["user_id"]),
    }
    return render(request, "new.html", context)

def create(request):
    trip_errors = Trips.objects.validator(request.POST)

    if len(trip_errors) > 0:
        for _, val in trip_errors.items():
            messages.error(request, val)

        return redirect('/trips/new')
    
    new_trip = Trips.objects.create(
        destination = request.POST['destination'],
        start_date = request.POST['start_date'],
        end_date = request.POST['end_date'],
        plan = request.POST['plan'],
        created_by = Users.objects.get(id=request.session["user_id"])
    )

    return redirect('/dashboard')

def trip(request, trip_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect("/")
    
    trip = Trips.objects.get(id=trip_id)
    trip.start_date = trip.start_date.strftime("%m/%d/%Y")
    trip.end_date = trip.end_date.strftime("%m/%d/%Y")
    trip.created_on = trip.created_on.strftime("%m/%d/%Y")
    trip.updated_on = trip.updated_on.strftime("%m/%d/%Y")
    
    context = {
        "logged_user": Users.objects.get(id=request.session["user_id"]),
        "trip": trip
    }
    return render(request, "trip.html", context)

def edit(request, trip_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect("/")

    trip = Trips.objects.get(id=trip_id)
    trip.start_date = trip.start_date.strftime("%Y-%m-%d")
    trip.end_date = trip.end_date.strftime("%Y-%m-%d")
    
    context = {
        "logged_user": Users.objects.get(id=request.session["user_id"]),
        "trip": trip
    }
    return render(request, "edit.html", context)

def update(request, trip_id):
    all_errors = Trips.objects.validator(request.POST)

    if len(all_errors) > 0:
        for _, val in all_errors.items():
            messages.error(request, val)
        return redirect(f'/trips/edit/{trip_id}')

    trip = Trips.objects.get(id=trip_id)
    trip.destination = request.POST['destination']
    trip.start_date = request.POST['start_date']
    trip.end_date = request.POST['end_date']
    trip.plan = request.POST['plan']
    trip.save()

    return redirect("/dashboard")

def join(request, trip_id):
    logged_user = Users.objects.get(id=request.session["user_id"])
    trip = Trips.objects.get(id=trip_id)
    trip.joined_by.add(logged_user)

    return redirect("/dashboard")

def cancel(request, trip_id):
    logged_user = Users.objects.get(id=request.session["user_id"])
    trip = Trips.objects.get(id=trip_id)
    trip.joined_by.remove(logged_user)

    return redirect("/dashboard")

def destroy(request, trip_id):
    Trips.objects.get(id=trip_id).delete()

    return redirect("/dashboard")