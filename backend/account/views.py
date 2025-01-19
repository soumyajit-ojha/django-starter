from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm
from .models import Account
from django.conf import settings
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile


class RegistrationView(View):
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse(f"You are already authenticated as {request.user.email}")
        form = RegistrationForm()
        return render(request, self.template_name, {'registration_form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse(f"You are already authenticated as {request.user.email}")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        return render(request, self.template_name, {'registration_form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class LoginView(View):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, {'login_form': LoginForm()})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid email or password.")
        return render(request, self.template_name, {'login_form': form})



class AccountView(View):
    template_name = 'account/account.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        try:
            account = Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return HttpResponse("<h3 class='text-center'>Something went wrong.</h3>")

        context = {
            'user_id': account.id,
            'username': account.username,
            'email': account.email,
            'profile_image': account.profile_image.url if account.profile_image else None,
            'hide_email': account.hide_email,
            'is_self': request.user.is_authenticated and request.user == account,
            'is_friend': False,  # Placeholder for friend logic
            # 'BASE_URL': settings.BASE_URL
        }
        return render(request, self.template_name, context)


class UploadCroppedImageView(View):
    def post(self, request, *args, **kwargs):
        try:
            data_url = request.POST.get('image')
            if not data_url:
                return JsonResponse({"success": False, "error": "No image data provided."}, status=400)

            format, imgstr = data_url.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f"cropped_image.{ext}")

            account = request.user
            if account.profile_image:
                account.profile_image.delete()
            account.profile_image.save(image_data.name, image_data)

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)
