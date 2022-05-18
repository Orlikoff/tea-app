from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    orders_num = models.PositiveIntegerField()
    rating = models.FloatField()
    registration_date = models.DateTimeField()

    def __str__(self):
        return self.nickname


class TeaItem(models.Model):
    previous_owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True,
                                       blank=True)
    current_owner = models.ForeignKey(Profile, related_name='tea_collection', on_delete=models.SET_NULL, null=True)
    in_cart_of = models.ForeignKey(Profile, related_name='cart_items', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=20)
    price = models.FloatField()
    status = models.CharField(max_length=20)
    voted = models.BooleanField()


class Drop(models.Model):
    author = models.ForeignKey(Profile, related_name='drops', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    article = models.TextField()
    creation_date = models.DateTimeField()
    popularity = models.IntegerField()


class DebitCard(models.Model):
    owner = models.ForeignKey(Profile, related_name='cards', on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    date = models.CharField(max_length=5)
    cvv = models.PositiveIntegerField()
