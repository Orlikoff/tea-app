from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('info/', views.IndexPageView.as_view(), name='info'),
    path('', views.IndexPageView.as_view(), name='info'),
    path('market', views.MarketPageView.as_view(), name='market'),
    path('market', views.MarketPageView.as_view(), name='drops'),
    path('market', views.MarketPageView.as_view(), name='profile'),
    # path('profile/', login_required(views.index_page()))
]
