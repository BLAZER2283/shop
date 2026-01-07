from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.item_view, name='item_view'),
    path('buy/<int:id>/', views.buy_view, name='buy_view'),
]
