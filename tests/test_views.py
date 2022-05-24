from django.test import Client
from django.urls import reverse
from blog.views import *


def test_info(db):
    client = Client()
    response = client.get(reverse('info'))
    assert response.status_code == 200


def test_market(db):
    client = Client()
    response = client.get(reverse('market'))
    assert response.status_code == 302


def test_drops(db):
    client = Client()
    response = client.get(reverse('drops'))
    assert response.status_code == 200


def test_profile(db):
    client = Client()
    response = client.get(reverse('profile'))
    assert response.status_code == 302


def test_login(db):
    client = Client()
    response = client.get(reverse('login'))
    assert response.status_code == 200


def test_register(db):
    client = Client()
    response = client.get('register')
    assert response.status_code == 404


def test_logout(db):
    client = Client()
    response = client.get(reverse('logout'))
    assert response.status_code == 302


def test_details_profile(db):
    client = Client()
    response = client.get(reverse('detailsProfile'))
    assert response.status_code == 302


def test_remove_from_selling(db):
    client = Client()
    response = client.get('removeFromSelling/0')
    assert response.status_code == 404


def test_delete_profile(db):
    client = Client()
    response = client.get('deleteProfile/0')
    assert response.status_code == 404


def test_vote(db):
    client = Client()
    response = client.get('vote/0')
    assert response.status_code == 404


def test_vote_for(db):
    client = Client()
    response = client.get('voteFor/0')
    assert response.status_code == 404


def test_ship_tea(db):
    client = Client()
    response = client.get('shipTea/0')
    assert response.status_code == 404


def test_remove_tea(db):
    client = Client()
    response = client.get('removeTea/0')
    assert response.status_code == 404


def test_add_tea(db):
    client = Client()
    response = client.get(reverse('addTea'))
    assert response.status_code == 302


def test_cards(db):
    client = Client()
    response = client.get(reverse('cards'))
    assert response.status_code == 302


def test_add_card(db):
    client = Client()
    response = client.get(reverse('addCard'))
    assert response.status_code == 302


def test_choose_card(db):
    client = Client()
    response = client.get('chooseCard/0')
    assert response.status_code == 404


def test_remove_card(db):
    client = Client()
    response = client.get('removeCard/0')
    assert response.status_code == 404


def test_buy_tea(db):
    client = Client()
    response = client.get('buyTea/0')
    assert response.status_code == 404


def test_sell_tea(db):
    client = Client()
    response = client.get('sellTea/0')
    assert response.status_code == 404


def test_change_market_mode(db):
    client = Client()
    response = client.get('changeMarketMode/0')
    assert response.status_code == 404


def test_cart(db):
    client = Client()
    response = client.get(reverse('cart'))
    assert response.status_code == 302


def test_remove_from_cart(db):
    client = Client()
    response = client.get('removeFromCart/0')
    assert response.status_code == 404


def test_clean_cart(db):
    client = Client()
    response = client.get(reverse('cleanCart'))
    assert response.status_code == 302


def test_confirm_payment(db):
    client = Client()
    response = client.get(reverse('confirmPayment'))
    assert response.status_code == 302


def test_add_drop(db):
    client = Client()
    response = client.get(reverse('addDrop'))
    assert response.status_code == 302


def test_change_drops_mode(db):
    client = Client()
    response = client.get('changeDropsMode/0')
    assert response.status_code == 404


def test_drop_info(db):
    client = Client()
    response = client.get('dropInfo/0')
    assert response.status_code == 404


def test_drop_info_vote(db):
    client = Client()
    response = client.get('dropInfo/voteDrop/0')
    assert response.status_code == 404
