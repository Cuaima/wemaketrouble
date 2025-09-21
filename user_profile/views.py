from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, StylistProfile, CustomerProfile

def landing(request):
    return render(request, "landing.html")

# ---- Signup Forms ----
class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email"]  # password1, password2 are added automatically

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.is_stylist = False
        if commit:
            user.save()
            CustomerProfile.objects.create(user=user)
        return user


class StylistSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_stylist = True
        user.is_customer = False
        if commit:
            user.save()
            StylistProfile.objects.create(user=user)
        return user


# ---- Views ----
def signup_customer(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in after signup
            return redirect("dashboard")  # redirect after signup
    else:
        form = CustomerSignUpForm()
    return render(request, "registration/signup_customer.html", {"form": form})


def signup_stylist(request):
    if request.method == "POST":
        form = StylistSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = StylistSignUpForm()
    return render(request, "registration/signup_stylist.html", {"form": form})


@login_required
def dashboard(request):
    """Redirect users based on type"""
    if request.user.is_stylist:
        return render(request, "dashboard/stylist_dashboard.html")
    elif request.user.is_customer:
        return render(request, "dashboard/customer_dashboard.html")
    else:
        return render(request, "dashboard/generic_dashboard.html")
