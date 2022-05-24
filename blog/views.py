from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from .models import TeaItem, Profile, DebitCard, Drop
import logging


logger = logging.getLogger(__name__)


class IndexPageView(View):
    template_name = 'source/index.html'

    def get(self, request):
        context = {}
        logger.debug('Info page loaded')
        return render(request, self.template_name, context)


class MarketPageView(View):
    BUY = 'buying'
    SEL = 'selling'
    template_name = 'source/market.html'

    def get(self, request):
        mode = request.session.get('market_mode', MarketPageView.BUY)
        request.session['previous_page'] = request.path
        logger.debug(f'Market page loaded in mode {mode}')
        context = {
            'mode': mode,
            'tea_items': MarketPageView.get_marketplace_tea(request) if mode == MarketPageView.BUY else
            MarketPageView.get_tea_for_sell(request),
            'cart_amount': request.user.cart_items.count(),
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_marketplace_tea(request):
        logger.debug('Query for marketplace tea')
        return TeaItem.objects.filter(status=TeaItem.MAR).exclude(previous_owner=request.user)

    @staticmethod
    def get_tea_for_sell(request):
        logger.debug('Query for sell tea')
        return request.user.tea_collection.filter(status=TeaItem.COL)


class BuyTeaView(View):
    def get(self, request, tea_id):
        logger.debug('Query for buy cart tea')
        tea_item = TeaItem.objects.get(id=tea_id)
        if tea_item.previous_owner == request.user:
            return redirect(self.request.session.get('previous_page', 'info'))
        tea_item.status = TeaItem.PRC
        tea_item.interaction_status = TeaItem.BUY
        tea_item.in_cart_of = request.user
        tea_item.save(update_fields=['status', 'interaction_status', 'in_cart_of'])
        return redirect(self.request.session.get('previous_page', 'info'))


class SellTeaView(View):
    def get(self, request, tea_id):
        logger.debug('Query for sell cart tea')
        tea_item = TeaItem.objects.get(id=tea_id)
        tea_item.status = TeaItem.PRC
        tea_item.interaction_status = TeaItem.SOL
        tea_item.in_cart_of = request.user
        tea_item.save(update_fields=['status', 'interaction_status', 'in_cart_of'])
        return redirect(self.request.session.get('previous_page', 'info'))


class ChangeMarketModeView(View):
    def get(self, request, mode):
        logger.debug(f'Market mode changed to {mode}')
        request.session['market_mode'] = mode
        return redirect('market')


class CartView(View):
    template_name = 'source/cart.html'

    def get(self, request):
        logger.debug('Cart page loaded')
        context = {
            'cart_items': CartView.get_cart_items(request),
            'url_to_comeback': request.session.get('previous_page', 'info'),
            'cart_sum': sum([cart_item.price for cart_item in CartView.get_cart_items(request).filter(
                interaction_status=TeaItem.BUY
            )])
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_cart_items(request):
        logger.debug('Query for cart items')
        return request.user.cart_items.all()


class RemoveFromCartView(View):
    def get(self, request, cart_item_id):
        tea_item = TeaItem.objects.get(id=cart_item_id)
        RemoveFromCartView.remove_from_cart(tea_item)
        logger.debug(f'Item {tea_item.name} was removed from cart')
        return redirect('cart')

    @staticmethod
    def remove_from_cart(tea_item):
        if tea_item.interaction_status == TeaItem.SOL:
            tea_item.status = TeaItem.COL
        else:
            tea_item.status = TeaItem.MAR
        tea_item.interaction_status = TeaItem.NUL
        tea_item.in_cart_of = None
        tea_item.save(update_fields=['status', 'interaction_status', 'in_cart_of'])


class CartCleanerView(View):
    def get(self, request):
        logger.debug('Cart wa cleaned')
        tea_items = request.user.cart_items.all()
        for tea_item in tea_items:
            RemoveFromCartView.remove_from_cart(tea_item)
        return redirect('cart')


class PaymentConfirmationView(View):
    def get(self, request):
        if PaymentConfirmationView.check_for_card(request):
            cart_items = request.user.cart_items.all()
            for cart_item in cart_items:
                PaymentConfirmationView.apply_cart_changes(request, cart_item)
            logger.debug('Payment confirmed')
        else:
            redirect('cards')
            logger.debug('Payment declined')
        return redirect('cart')

    @staticmethod
    def apply_cart_changes(request, tea_item: TeaItem):
        if tea_item.interaction_status == TeaItem.SOL:
            tea_item.status = TeaItem.MAR
            tea_item.previous_owner = request.user
            tea_item.current_owner = None
            tea_item.in_cart_of = None
        else:
            tea_item.status = TeaItem.COL
            tea_item.current_owner = request.user
        tea_item.voted = False
        tea_item.in_cart_of = None
        tea_item.interaction_status = TeaItem.NUL
        tea_item.save(update_fields=['current_owner', 'previous_owner',
                                     'status', 'interaction_status', 'in_cart_of',
                                     'voted'])

    @staticmethod
    def check_for_card(request):
        cards_len = request.user.cards.all().count()
        if cards_len > 0:
            return True
        return False


class DropsPageView(View):
    template_name = 'source/drops.html'

    def get(self, request):
        mode = request.session.get('drops_mode', 'date')
        logger.debug(f'Drops page loaded in {mode}')
        context = {
            'drop_items': DropsPageView.get_drops(mode),
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_drops(mode):
        if mode == 'date':
            return Drop.objects.all().order_by('-creation_date')
        return Drop.objects.all().order_by('-popularity')


class AddDropView(View):
    template_name = 'source/add_drop.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        drop_name = request.POST.get('title')
        drop_desc = request.POST.get('description')
        drop_short_desc = drop_desc[:199].strip()

        if not drop_name or not drop_desc:
            return render(request, self.template_name, {})

        Drop.objects.create(
            author=request.user,
            title=drop_name,
            article=drop_desc,
            short_article=drop_short_desc,
        )
        logger.debug('Drop has been added')
        return redirect('drops')


class ChangeDropsModeView(View):
    def get(self, request, mode):
        request.session['drops_mode'] = mode
        logger.debug(f'Drops mode changed to {mode}')
        return redirect('drops')


class DropInfoView(View):
    template_name = 'source/drop_info.html'

    def get(self, request, drop_id):
        logger.debug('Drop has been loaded')
        request.session['prev_drop'] = request.path
        context = {
            'drop_item': Drop.objects.get(id=drop_id),
            'can_vote': Drop.objects.get(id=drop_id).author != request.user and not (
                        request.user in Drop.objects.get(id=drop_id).voted_people.all()),
        }
        return render(request, self.template_name, context)


class DropVoteView(View):
    coef = 0.05

    def get(self, request, mode, drop_id):
        drop = Drop.objects.get(id=drop_id)
        profile = drop.author
        if mode == 'pos':
            drop.popularity += 1
            profile.rating += self.coef
        else:
            drop.popularity -= 1
            profile.rating -= self.coef
        logger.debug(f'Voted for drop with {mode}')
        drop.voted_people.add(request.user)
        drop.save(update_fields=['popularity'])
        profile.save(update_fields=['rating'])
        return redirect(request.session.get('prev_drop', 'drops'))


class ProfilePageView(View):
    template_name = 'source/profile.html'

    def get(self, request):
        logger.debug('Profile page loaded')
        context = {
            'tea_sold': ProfilePageView.get_sold_items(request)
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_sold_items(request):
        return request.user.on_sell.filter(status=TeaItem.MAR)


class RegisterPageView(View):
    template_name = 'source/register.html'

    def get(self, request):
        logger.debug('Register page loaded')
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
                request.session['drops_mode'] = 'date'
                request.session['market_mode'] = MarketPageView.BUY
                login(request, new_user)
                logger.debug('Registered new user')
                return redirect('info')
            else:
                logger.debug('Bad form ')
                form = SignUpForm(request.POST)
        context = {'form': form}
        return render(request, self.template_name, context)


class LoginPageView(View):
    template_name = 'source/login.html'

    def get(self, request):
        logger.debug('Login page loaded')
        return render(request, self.template_name, {})

    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                logout(request)
                login(request, user)
                request.session['drops_mode'] = 'date'
                request.session['market_mode'] = MarketPageView.BUY
                logger.debug('Logged in')
                return redirect('/info')

        logger.debug('Bad login form')
        return render(request, self.template_name, {})


class DetailsProfileView(View):
    template_name = 'source/change_profile.html'

    def get(self, request):
        logger.debug('Loaded profile details page')
        context = {}
        return render(request, self.template_name, context)


class CollectionView(View):
    template_name = 'source/collection.html'

    def get(self, request):
        logger.debug('Collection page loaded')
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
        logger.debug(f'Removed item {item.name}')
        item.status = TeaItem.COL
        item.current_owner = item.previous_owner
        item.previous_owner = None
        item.save(update_fields=['status', 'current_owner', 'previous_owner'])
        return redirect('profile')


class ProfileRemoverView(View):
    def get(self, request, profile_id):
        logger.debug(f'Removed profile with id {profile_id}')
        logout(request)
        Profile.objects.filter(id=profile_id).delete()
        return render(request, IndexPageView.template_name, {})


class VoteView(View):
    template_name = 'source/vote.html'

    def get(self, request, tea_id):
        logger.debug('Vote view loaded')
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
        logger.debug(f'Voted for tea with {mark}')
        return render(request, CollectionView.template_name, context)


class ShipView(View):
    def get(self, request, tea_id):
        logger.debug('Tea has been shipped')
        TeaItem.objects.get(id=tea_id).delete()
        return render(request, CollectionView.template_name, {
            'tea_items': CollectionView.get_collection_items(request)
        })


class TeaRemoverView(View):
    def get(self, request, tea_id):
        logger.debug('Tea has been sent to marketplace')
        tea_item = TeaItem.objects.get(id=tea_id)
        tea_item.current_owner = None
        tea_item.previous_owner = None
        tea_item.status = TeaItem.MAR
        tea_item.save(update_fields=['current_owner', 'status', 'previous_owner'])
        return redirect('collection')


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
            logger.debug('Bad tea add form')
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

        logger.debug(f'Added tea with {tea_name}')

        return render(request, CollectionView.template_name, {
            'tea_items': CollectionView.get_collection_items(request)
        })

    def validate_package(self, package_id):
        return True


class CardsView(View):
    template_name = 'source/cards.html'

    def get(self, request):
        logger.debug('Cards page loaded')
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
            logger.debug('Bad card form')
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

        logger.debug(f'Cart with number {card_number} has been added')
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
        logger.debug(f'Card with number {card.number} has been chosen')
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
        logger.debug('Card has been removed')
        return redirect('cards')
