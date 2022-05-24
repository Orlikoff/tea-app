import pytest

from blog.models import Drop


@pytest.fixture(params=['TestDrop1', 'Test Drop2'])
def create_temp_drop(request):
    return Drop.objects.create(
        author=None,
        title=request.param,
        article=request.param,
        short_article=request.param
    )


@pytest.mark.parametrize('test, expected', [('TestDrop1', 'TestDrop1'), ('Test Drop2', 'Test Drop2')])
def test_profile_creation(db, test, expected):
    new_drop = Drop.objects.create(
        author=None,
        title=test,
        article=test,
        short_article=test
    )
    assert new_drop.author is None
    assert new_drop.title == expected
    assert new_drop.article == expected
    assert new_drop.short_article == expected
    assert new_drop.creation_date is not None
    assert new_drop.popularity == 0
    assert new_drop.voted_people.count() == 0


def test_tea_item_insertion(db, create_temp_drop):
    drop = create_temp_drop
    db_drop = Drop.objects.get(id=drop.id)
    assert drop.author == db_drop.author
    assert drop.title == db_drop.title
    assert drop.article == db_drop.article
    assert drop.short_article == db_drop.short_article
    assert drop.creation_date == db_drop.creation_date
    assert drop.popularity == db_drop.popularity
    assert drop.voted_people.count() == db_drop.voted_people.count()


def test_tea_item_deletion(db, create_temp_drop):
    drop = create_temp_drop
    assert Drop.objects.get(id=drop.id).delete()[0] == 1
