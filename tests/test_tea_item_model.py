import pytest

from blog.models import TeaItem


@pytest.fixture(params=['TestTeaItem1', 'Test TeaItem2'])
def create_temp_tea_item(request):
    return TeaItem.objects.create(
        previous_owner=None,
        current_owner=None,
        in_cart_of=None,
        name=request.param,
        origin_country=request.param,
        price=10,
        voted=False
    )


@pytest.mark.parametrize('test, expected', [('TestTeaItem1', 'TestTeaItem1'), ('Test TeaItem2', 'Test TeaItem2')])
def test_profile_creation(db, test, expected):
    new_tea_item = TeaItem.objects.create(
        previous_owner=None,
        current_owner=None,
        in_cart_of=None,
        name=test,
        origin_country=test,
        price=10,
        voted=False
    )
    assert new_tea_item.previous_owner is None
    assert new_tea_item.current_owner is None
    assert new_tea_item.in_cart_of is None
    assert new_tea_item.name == expected
    assert new_tea_item.origin_country == expected
    assert new_tea_item.price == 10
    assert new_tea_item.status == TeaItem.COL
    assert new_tea_item.interaction_status == TeaItem.NUL
    assert not new_tea_item.voted


def test_tea_item_insertion(db, create_temp_tea_item):
    tea_item = create_temp_tea_item
    db_tea_item = TeaItem.objects.get(id=tea_item.id)
    assert tea_item.previous_owner == db_tea_item.previous_owner
    assert tea_item.current_owner == db_tea_item.current_owner
    assert tea_item.in_cart_of == db_tea_item.in_cart_of
    assert tea_item.name == db_tea_item.name
    assert tea_item.origin_country == db_tea_item.origin_country
    assert tea_item.price == db_tea_item.price
    assert tea_item.status == db_tea_item.status
    assert tea_item.interaction_status == db_tea_item.interaction_status
    assert tea_item.voted == db_tea_item.voted


def test_tea_item_deletion(db, create_temp_tea_item):
    tea_item = create_temp_tea_item
    assert TeaItem.objects.get(id=tea_item.id).delete()[0] == 1
