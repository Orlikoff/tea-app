from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


class IndexPageView(View):
    template_name = 'source/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class MarketPageView(View):
    template_name = 'source/market.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class DropsPageView(View):
    template_name = 'source/drops.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class ProfilePageView(View):
    template_name = 'source/profile.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class RegisterPageView(View):
    template_name = 'source/register.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm()

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                new_user = authenticate(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )
                login(request, new_user)
                return redirect('info')
            else:
                form = SignUpForm(request.POST)
        context = {'form': form}
        return render(request, self.template_name, context)


class LoginPageView(View):
    template_name = 'source/login.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class DetailsProfileView(View):
    template_name = 'source/change_profile.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
