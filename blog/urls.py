from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('info/', views.IndexPageView.as_view(), name='info'),
    path('', views.IndexPageView.as_view(), name='info'),
    path('market', login_required(views.MarketPageView.as_view()), name='market'),
    path('drops', views.DropsPageView.as_view(), name='drops'),
    path('profile', login_required(views.ProfilePageView.as_view()), name='profile'),
    path('login', views.LoginPageView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.RegisterPageView.as_view(), name='signup'),
    path('detailsProfile', views.DetailsProfileView.as_view(), name='detailsProfile'),
    path('collection', views.CollectionView.as_view(), name='collection'),
    path('removeFromSelling/<int:tea_id>', views.ItemRemover.as_view(), name='removeItem'),
    path('deleteProfile/<int:profile_id>', views.ProfileRemoverView.as_view(), name='deleteProfile'),
    path('vote/<int:tea_id>', views.VoteView.as_view(), name='vote'),
    path('vote/voteFor/<int:tea_id>', views.VoteForView.as_view(), name='voteFor'),
]
