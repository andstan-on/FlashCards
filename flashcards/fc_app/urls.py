from django.urls import path
from . import views
from .views import (
    DeckListView,
    DeckDetailView,
    DeckCreateView,
    DeckUpdateView,
    DeckDeleteView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('decks/', views.DeckListView.as_view(), name='decks'),
    path('decks/<int:pk>/', DeckDetailView.as_view(), name='deck_detail'),
    path('decks/create/', DeckCreateView.as_view(), name='deck_create'),
    path('decks/<int:pk>/update/', DeckUpdateView.as_view(), name='deck_update'),
    path('decks/<int:pk>/delete/', DeckDeleteView.as_view(), name='deck_delete'),
]

from .views import (
    CardCreateView,
    CardDetailView,
    CardUpdateView,
    CardDeleteView,
)

urlpatterns += [
    path('decks/<int:deck_pk>/cards/new/', CardCreateView.as_view(), name='card_create'),
    path('decks/<int:deck_pk>/cards/<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('decks/<int:deck_pk>/cards/<int:pk>/edit/', CardUpdateView.as_view(), name='card_update'),
    path('decks/<int:deck_pk>/cards/<int:pk>/delete/', CardDeleteView.as_view(), name='card_delete'),

]