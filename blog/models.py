from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ProfileManager(BaseUserManager):
    def create_user(self, email, name, surname, address, password=None):
        if not email:
            raise ValueError('User must have email')
        if not name:
            raise ValueError('User must have name')
        if not surname:
            raise ValueError('User must have surname')
        if not address:
            raise ValueError('User must have address')

        user = self.model(
            email=self.normalize_email(email),
            name=str.capitalize(str.lower(name)),
            surname=str.capitalize(str.lower(surname)),
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, address, password):
        user = self.create_user(
            email=email,
            name=name,
            surname=surname,
            address=address,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    orders_num = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    registration_date = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'address', 'password']

    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class TeaItem(models.Model):
    MAR = 'MARKETPLACE'
    COL = 'COLLECTION'
    status_choices = (
        (COL, 'in collection'),
        (MAR, 'in marketplace')
    )
    previous_owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True,
                                       blank=True)
    current_owner = models.ForeignKey(Profile, related_name='tea_collection', on_delete=models.SET_NULL, null=True)
    in_cart_of = models.ForeignKey(Profile, related_name='cart_items', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=20)
    price = models.FloatField()
    status = models.CharField(max_length=20, choices=status_choices, default=MAR)
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
