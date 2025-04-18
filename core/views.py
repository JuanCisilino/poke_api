from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Pokemon
from .serializers import PokemonSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services.updater import update_pokemon_list

class PokemonListCreateView(generics.ListCreateAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

class PokemonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer


class CheckUpdateView(APIView):
    def get(self, request):
        result = update_pokemon_list()
        return Response(result)
