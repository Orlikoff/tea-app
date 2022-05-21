from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from .models import TeaItem, Profile


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
        context = {
            'tea_sold': ProfilePageView.get_sold_items(request)
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_sold_items(request):
        return request.user.tea_collection.filter(status=TeaItem.MAR)


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
        return render(request, self.template_name, {})

    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                logout(request)
                login(request, user)
                return redirect('/info')

        return render(request, self.template_name, {})


class DetailsProfileView(View):
    template_name = 'source/change_profile.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class CollectionView(View):
    template_name = 'source/collection.html'

    def get(self, request):
        context = {
            'tea_items': CollectionView.get_collection_items(request)
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_collection_items(request):
        return request.user.tea_collection.filter(status=TeaItem.COL) | \
               request.user.tea_collection.filter(status=TeaItem.PEN)


class ItemRemover(View):
    def get(self, request, tea_id):
        item = TeaItem.objects.get(id=tea_id)
        item.status = TeaItem.COL
        item.save(update_fields=['status'])
        return render(request, ProfilePageView.template_name, context={
            'tea_sold': ProfilePageView.get_sold_items(request)
        })


class ProfileRemoverView(View):
    def get(self, request, profile_id):
        logout(request)
        Profile.objects.filter(id=profile_id).delete()
        return render(request, IndexPageView.template_name, {})


class VoteView(View):
    template_name = 'source/vote.html'

    def get(self, request, tea_id):
        context = {
            'tea_item': VoteView.get_tea_item(request, tea_id)
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_tea_item(request, tea_id):
        return request.user.tea_collection.get(id=tea_id)


class VoteForView(View):
    coef = 10

    def post(self, request, tea_id):
        mark = int(request.POST.get('mark'))
        mark = (mark-5)/self.coef
        tea_item = TeaItem.objects.get(id=tea_id)
        previous_owner = tea_item.previous_owner
        previous_owner.rating += mark
        previous_owner.save(update_fields=['rating'])
        tea_item.voted = True
        tea_item.save(update_fields=['voted'])
        context = {
            'tea_items': CollectionView.get_collection_items(request)
        }
        return render(request, CollectionView.template_name, context)

