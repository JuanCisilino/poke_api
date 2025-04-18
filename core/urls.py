from django.urls import path
from .views import PokemonListCreateView, PokemonRetrieveUpdateDestroyView, CheckUpdateView

urlpatterns = [
    path('pokemon/', PokemonListCreateView.as_view(), name='pokemon-list-create'),
    path('pokemon/<int:pk>/', PokemonRetrieveUpdateDestroyView.as_view(), name='pokemon-detail'),
    path('pokemon/checkUpdate/', CheckUpdateView.as_view()),
]
