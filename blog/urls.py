import django.contrib.auth.views
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('info/', views.IndexPageView.as_view(), name='info'),
    path('', views.IndexPageView.as_view(), name='info'),
    path('market', views.MarketPageView.as_view(), name='market'),
    path('drops', views.DropsPageView.as_view(), name='drops'),
    path('profile', views.ProfilePageView.as_view(), name='profile'),
    path('login', django.contrib.auth.views.LoginView.as_view(), name='login'),
    path('register', django.contrib.auth.views.LoginView.as_view(), name='signup'),
    # path('profile/', login_required(views.index_page()))
]
