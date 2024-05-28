from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import FormView


# Create your views here.


class UserSignupView(FormView):
    template_name = "account/signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account Created Successful")
        return super().form_valid(form)  


class UserLoginView(LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Logged In Successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Login Failed!")
        return super().form_invalid(form)


@login_required()
def user_logout(request):
    logout(request)
    return redirect("login")
