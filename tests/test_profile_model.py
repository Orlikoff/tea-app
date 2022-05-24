import pytest

from blog.models import Profile


@pytest.fixture(params=['TestUser1', 'Test User2'])
def create_temp_user(request):
    return Profile.objects.create(
        email=request.param,
        name=request.param,
        surname=request.param,
        address=request.param,
        password=request.param
    )


@pytest.mark.parametrize('test, expected', [('TestUser1', 'TestUser1'), ('Test User2', 'Test User2')])
def test_profile_creation(db, test, expected):
    new_profile = Profile.objects.create(
        email=test,
        name=test,
        surname=test,
        address=test,
        password=test
    )
    assert new_profile.email == expected
    assert new_profile.name == expected
    assert new_profile.surname == expected
    assert new_profile.address == expected
    assert new_profile.password == expected

    assert new_profile.rating == 0
    assert new_profile.orders_num == 0
    assert new_profile.registration_date is not None

    assert new_profile.last_login is not None
    assert not new_profile.is_admin
    assert new_profile.is_active
    assert not new_profile.is_staff
    assert not new_profile.is_superuser

    assert str(new_profile) == expected
    assert new_profile.has_perm(test) == new_profile.is_admin
    assert new_profile.has_module_perms(test)


def test_profile_insertion(db, create_temp_user):
    user = create_temp_user
    db_user = Profile.objects.get(id=user.id)
    assert user.email == db_user.email
    assert user.name == db_user.name
    assert user.surname == db_user.surname
    assert user.address == db_user.address
    assert user.password == db_user.password
    assert user == db_user


def test_profile_deletion(db, create_temp_user):
    user = create_temp_user
    assert Profile.objects.get(id=user.id).delete()[0] == 1
