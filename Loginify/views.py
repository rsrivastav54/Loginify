from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def get_all_users(request):
    if request.method == "GET":
        users = UserDetails.objects.all()
        users_list = [{"username": user.username, "email": user.email} for user in users]
        return JsonResponse({"users": users_list}, status=200)
    return JsonResponse({"error": "GET method only"}, status=405)

def get_user_by_email(request, email):
    if request.method == "GET":
        try:
            user = UserDetails.objects.get(email=email)
            user_data = {"username": user.username, "email": user.email}
            return JsonResponse({"user": user_data}, status=200)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "GET method only"}, status=405)

@csrf_exempt
def update_user_details(request, email):
    if request.method == "PUT":
        try:
            user = UserDetails.objects.get(email=email)
            data = json.loads(request.body)
            user.username = data.get("username", user.username)
            user.password = data.get("password", user.password)
            user.save()
            return JsonResponse({"message": "User updated successfully"}, status=200)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "PUT method only"}, status=405)


@csrf_exempt
def delete_user(request, email):
    if request.method == "DELETE":
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "DELETE method only"}, status=405)


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check for unique email
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        # Save the new user
        UserDetails.objects.create(username=username, email=email, password=password)
        messages.success(request, "Signup successful! Please log in.")
        return redirect('login')  # Redirect to login page

    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                return redirect('success')  # Redirect to success page
            else:
                messages.error(request, "Invalid password!")
        except UserDetails.DoesNotExist:
            messages.error(request, "User does not exist!")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def success(request):
    return render(request, 'success.html')

def confirmation(request):
    return render(request, 'confirmation.html')

def home(request):
    return render(request, 'home.html')

def hello_world(request):
    return HttpResponse("Hello, world!")