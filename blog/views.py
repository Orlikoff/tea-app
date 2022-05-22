from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from .models import TeaItem, Profile, DebitCard

ADMIN_ACCOUNT = 'studyorlik@gmail.com'


class IndexPageView(View):
    template_name = 'source/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class MarketPageView(View):
    BUY = 'buying'
    SEL = 'selling'
    template_name = 'source/market.html'

    def get(self, request):
        # mode = request.session['market_mode']
        mode = MarketPageView.SEL
        request.session['previous_page'] = request.path
        context = {
            'mode': mode,
            'tea_items': MarketPageView.get_marketplace_tea() if mode == MarketPageView.BUY else
            MarketPageView.get_tea_for_sell(
                request)
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_marketplace_tea():
        return TeaItem.objects.filter(status=TeaItem.MAR)

    @staticmethod
    def get_tea_for_sell(request):
        return request.user.tea_collection.filter(status=TeaItem.COL)


class BuyTeaView(View):
    def get(self, request, tea_id):
        tea_item = TeaItem.objects.get(id=tea_id)
        tea_item.status = TeaItem.PRC
        tea_item.interaction_status = TeaItem.BUY
        tea_item.in_cart_of = request.user
        tea_item.save(update_fields=['status', 'interaction_status', 'in_cart_of'])
        return redirect(self.request.session['previous_page'])


class SellTeaView(View):
    def get(self, request, tea_id):
        tea_item = TeaItem.objects.get(id=tea_id)
        tea_item.status = TeaItem.PRC
        tea_item.interaction_status = TeaItem.SOL
        tea_item.in_cart_of = request.user
        tea_item.save(update_fields=['status', 'interaction_status', 'in_cart_of'])
        return redirect(self.request.session['previous_page'])


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
                request.session['market_mode'] = MarketPageView.BUY
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
        if not 0 <= mark <= 10:
            return render(request, CollectionView.template_name, {
                'tea_items': CollectionView.get_collection_items(request)
            })
        mark = (mark - 5) / self.coef
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


class ShipView(View):
    def get(self, request, tea_id):
        TeaItem.objects.get(id=tea_id).delete()
        return render(request, CollectionView.template_name, {
            'tea_items': CollectionView.get_collection_items(request)
        })


class TeaRemoverView(View):
    def get(self, request, tea_id):
        tea_item = TeaItem.objects.get(id=tea_id)
        tea_item.current_owner = None
        tea_item.previous_owner = request.user
        tea_item.status = TeaItem.MAR
        tea_item.save(update_fields=['current_owner'])
        return render(request, CollectionView.template_name, {
            'tea_items': CollectionView.get_collection_items(request)
        })


class AddTeaView(View):
    template_name = 'source/add_tea.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        tea_name = request.POST.get('tea_name')
        country_of_origin = request.POST.get('country')
        price = float(request.POST.get('price'))

        package_id = request.POST.get('package_id')

        if not tea_name or not country_of_origin or not self.validate_package(package_id) or price < 0:
            return render(request, self.template_name, {})

        TeaItem.objects.create(
            previous_owner=None,
            current_owner=request.user,
            in_cart_of=None,
            name=tea_name,
            origin_country=country_of_origin,
            price=price,
            status=TeaItem.COL,
            voted=False
        )

        return render(request, CollectionView.template_name, {
            'tea_items': CollectionView.get_collection_items(request)
        })

    def validate_package(self, package_id):
        return True


class CardsView(View):
    template_name = 'source/cards.html'

    def get(self, request):
        context = {
            'card_items': self.get_cards(request)
        }

        return render(request, self.template_name, context)

    @staticmethod
    def get_cards(request):
        return request.user.cards.all().order_by('-id')


class AddCardView(View):
    template_name = 'source/add_card.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        card_number = request.POST.get('card_number')
        card_date = request.POST.get('card_date')
        card_cvv = int(request.POST.get('card_cvv'))

        if not card_number or not card_date or not card_cvv or card_cvv < 0 or len(request.user.cards.all()) >= 3 or \
                self.check_for_double(request, card_number):
            return redirect('cards')

        for card_item in request.user.cards.all():
            card_item.active = False
            card_item.save(update_fields=['active'])

        DebitCard.objects.create(
            owner=request.user,
            number=card_number,
            date=card_date,
            cvv=card_cvv,
            active=True
        )

        return redirect('cards')

    @staticmethod
    def check_for_double(request, number):
        for card_item in request.user.cards.all():
            if card_item.number == number:
                return True
        return False


class ChooseCardView(View):
    def get(self, request, card_id):
        for card_item in request.user.cards.all():
            card_item.active = False
            card_item.save(update_fields=['active'])
        card = DebitCard.objects.get(id=card_id)
        card.active = True
        card.save(update_fields=['active'])
        return redirect('cards')


class RemoveCardView(View):
    def get(self, request, card_id):
        DebitCard.objects.get(id=card_id).delete()
        if request.user.cards.filter(active=True).count() == 0:
            if request.user.cards.all().count() > 0:
                card = request.user.cards.all()[0]
                card.active = True
                card.save(update_fields=['active'])
        return redirect('cards')
