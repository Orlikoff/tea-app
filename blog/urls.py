from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('info/', views.IndexPageView.as_view(), name='info'),
    path('', views.IndexPageView.as_view(), name='info'),
    path('market', views.MarketPageView.as_view(), name='market'),
    path('drops', views.DropsPageView.as_view(), name='drops'),
    path('profile', views.ProfilePageView.as_view(), name='profile'),
    path('login', views.LoginPageView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.RegisterPageView.as_view(), name='signup'),
    path('detailsProfile', views.DetailsProfileView.as_view(), name='detailsProfile'),
    # path('profile/', login_required(views.index_page()))
]
