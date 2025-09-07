from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Sum



def handleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = email.split("@")[0]
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            
            if request.user.is_authenticated:
                messages.success(request, 'Logged in Successfully!')
                return HttpResponseRedirect(reverse("mainpage"))
        
        messages.error(request, 'Authentication Failed! Please check credentials')
    return render(request, "login.html")


def handleSignup(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = email.split("@")[0]
        fullname = fullname.split()

        user = User.objects.create_user(username=username, email=email, password=password)

        user.first_name = fullname[0]
        if len(fullname) > 1:
            user.last_name = fullname[1]

        messages.success(request, "Successfully Signed Up! Please login now")

    return HttpResponseRedirect(reverse("login"))


def handleLogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, "Successfully Logged out!")
    return HttpResponseRedirect(reverse("mainpage"))


def mainpage(request):
    return render(request, "index.html")

def addPet(request):
    if request.method == "POST":
        pet_name = request.POST.get("pet_name")
        pet_type = request.POST.get("pet_type")
        pet_gender = request.POST.get("pet_gender")
        pet_years = request.POST.get("pet_years")
        pet_months = request.POST.get("pet_months")
        pet_notes = request.POST.get("pet_notes")
        owner_id = request.user.id

        pet = Pet(
            pet_type=pet_type,
            gender=pet_gender,
            age=str(pet_years) + " years " + str(pet_months) + " months",
            name=pet_name,
            owner_id=owner_id,
            notes=pet_notes
        )

        pet.save()

    all_pets = Pet.objects.filter(owner_id=request.user.id)

    return render(request, "add-pet.html", {"all_pets":all_pets})

def chat(request):
    return render(request, "chat.html")

def dashboard(request):
    if request.user.is_authenticated:
        pets = Pet.objects.filter(owner_id=request.user.id)
        return render(request, "dashboard.html", {"all_pets": pets})
    else:
        return HttpResponseRedirect(reverse("login"))
    
def petInfo(request, pet_id):
    pet = Pet.objects.filter(pet_id=pet_id)[0]
    age = pet.age.split()
    data = {
        "pet_id": pet.pet_id,
        "name": pet.name,
        "age_years": age[0],
        "age_months": age[2],
        "gender": pet.gender,
        "notes": pet.notes,
        "pet_type": pet.pet_type,
    }
    return JsonResponse(data)


def updatePetInfo(request):
    if request.method == "POST":
        pet_id = request.POST.get("pet_id")
        
        pet = Pet.objects.filter(pet_id=pet_id).first()
        if pet.owner_id != request.user.id:
            messages.error(request, "Sorry you're not the owner of this pet!")
            return HttpResponseRedirect(reverse("addPet"))
        
        edited_pet_name = request.POST.get("editName")
        edited_pet_type = request.POST.get("editType")
        edited_pet_gender = request.POST.get("editGender")
        edited_pet_years = request.POST.get("editYears")
        edited_pet_months = request.POST.get("editMonths")
        edited_pet_notes = request.POST.get("editNotes")

        pet.pet_type = edited_pet_type
        pet.gender = edited_pet_gender
        pet.age = f"{edited_pet_years} years {edited_pet_months} months"
        pet.name = edited_pet_name
        pet.notes = edited_pet_notes

        # Save
        pet.save()

        messages.success(request, "Pet Data updated successfully!")

    return HttpResponseRedirect(reverse("addPet"))


def chartData(request, pet_id):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # Aggregate by day
    pet_data = (
        PetData.objects.filter(
            pet_id=pet_id,
            created_at__date__range=[week_ago, today]
        )
        .values("created_at__date")
        .annotate(
            avg_heart_rate=Avg("heart_rate"),
            total_sleep_hours=Sum("sleep_hours"),
            total_miles_travelled=Sum("miles_travelled"),
            total_calories_burned=Sum("calories_burned"),
        )
        .order_by("created_at__date")
    )

    # Labels = days
    labels = [str(d["created_at__date"]) for d in pet_data]

    heart_rate = [d["avg_heart_rate"] or 0 for d in pet_data]
    sleep_hours = [d["total_sleep_hours"] or 0 for d in pet_data]
    miles_travelled = [d["total_miles_travelled"] or 0 for d in pet_data]
    calories_burned = [d["total_calories_burned"] or 0 for d in pet_data]

    max_calories = max(calories_burned) if calories_burned else 1

    data = {
        "labels": labels,

        "bar_heart_rate": {
            "labels": labels,
            "datasets": [{"label": "Avg Heart Rate", "data": heart_rate, "backgroundColor": "#DA7E66"}],
        },

        "bar_sleep_hours": {
            "labels": labels,
            "datasets": [{"label": "Total Sleep Hours", "data": sleep_hours, "backgroundColor": "#DA7E66"}]
        },

        "line_miles_travelled": {
            "labels": labels,
            "datasets": [{"label": "Miles Travelled", "data": miles_travelled}]
        },

        "radar_comparison": {
            "labels": ["Heart Rate", "Sleep Hours", "Miles Travelled", "Calories Burned"],
            "datasets": [{
                "label": "Weekly Avg",
                "data": [
                    sum(heart_rate) / len(heart_rate) if heart_rate else 0,
                    sum(sleep_hours) / len(sleep_hours) if sleep_hours else 0,
                    sum(miles_travelled) / len(miles_travelled) if miles_travelled else 0,
                    sum(calories_burned) / len(calories_burned) if calories_burned else 0
                ],
                "backgroundColor": "rgba(218, 126, 102, 0.2)", 
                "borderColor": "#DA7E66"
            }]
        },

        "pie_distribution": {
            "labels": ["Heart Rate", "Sleep Hours", "Miles Travelled", "Calories Burned"],
            "datasets": [{
                "data": [
                    sum(heart_rate),
                    sum(sleep_hours),
                    sum(miles_travelled),
                    sum(calories_burned)
                ],
                "backgroundColor": ["#f6e5dfff", "#DA7E66", "#f4a688", "#ffd1c1"]
            }]
        },

        "bubble_chart": {
            "datasets": [{
                "label": "Calories vs Miles vs HR",
                "data": [
                    {"x": m, "y": s, "r": (c / max_calories) * 20}  # max bubble = 20px
                    for m, s, c in zip(miles_travelled, sleep_hours, calories_burned)
                ],
                "backgroundColor": '#DA7E66',
            }]
        }
    }

    print(data)

    return JsonResponse(data)