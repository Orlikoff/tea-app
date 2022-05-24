import pytest

from blog.models import DebitCard
from test_profile_model import create_temp_user


@pytest.fixture(params=['TestDebitCard1', 'Test DebitCard2'])
def create_temp_debit_card(request, create_temp_user):
    return DebitCard.objects.create(
        owner=create_temp_user,
        number=request.param,
        date='te/st',
        cvv=111
    )


@pytest.mark.parametrize('test, expected', [('TestDebitCard1', 'TestDebitCard1'), ('Test DebitCard2', 'Test DebitCard2')])
def test_debit_card_creation(db, test, expected, create_temp_user):
    card_owner = create_temp_user
    new_card = DebitCard.objects.create(
        owner=card_owner,
        number=test,
        date='te/st',
        cvv=111
    )
    assert new_card.owner == card_owner
    assert new_card.number == expected
    assert new_card.date == 'te/st'
    assert new_card.cvv == 111
    assert not new_card.active


def test_debit_card_insertion(db, create_temp_debit_card):
    card = create_temp_debit_card
    db_card = DebitCard.objects.get(id=card.id)
    assert card.owner == db_card.owner
    assert card.number == db_card.number
    assert card.date == db_card.date
    assert card.cvv == db_card.cvv
    assert card.active == db_card.active


def test_debit_card_deletion(db, create_temp_debit_card):
    card = create_temp_debit_card
    assert DebitCard.objects.get(id=card.id).delete()[0] == 1
