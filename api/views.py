from rest_framework import generics

#doc MODELS : TABLES FROM THE DATABASE
from .models import Parent, Child, Household, Invitation

#doc SERIALIZERS : CONVERT PYTHON OBJECTS TO JSON
from .serializers import ParentSerializer, ChildSerializer, HouseholdSerializer, InvitationSerializer

#doc PARENT LIST
class ParentList(generics.ListCreateAPIView): #doc Cette vue générique permet à la fois de lister (GET) et de créer (POST) des objets dans la base de données.
    queryset = Parent.objects.all() #doc Définit l'ensemble des objets à renvoyer dans la vue. Ici, tous les objets Parent de la base de données seront renvoyés par la vue.
    serializer_class = ParentSerializer #doc Indique à la vue d'utiliser le serializer ParentSerializer pour transformer les instances du modèle Parent en JSON, et vice-versa lors de la création d'un objet.

#doc CHILD LIST
class ChildList(generics.ListCreateAPIView): #doc Cette vue générique permet à la fois de lister (GET) et de créer (POST) des objets dans la base de données.
    queryset = Child.objects.all() #doc Définit l'ensemble des objets à renvoyer dans la vue. Ici, tous les objets Parent de la base de données seront renvoyés par la vue.
    serializer_class = ChildSerializer #doc Indique à la vue d'utiliser le serializer ParentSerializer pour transformer les instances du modèle Parent en JSON, et vice-versa lors de la création d'un objet.

#doc HOUSEHOLD LIST
class HouseholdList(generics.ListCreateAPIView): #doc Cette vue générique permet à la fois de lister (GET) et de créer (POST) des objets dans la base de données.
    queryset = Household.objects.all() #doc Définit l'ensemble des objets à renvoyer dans la vue. Ici, tous les objets Parent de la base de données seront renvoyés par la vue.
    serializer_class = HouseholdSerializer #doc Indique à la vue d'utiliser le serializer ParentSerializer pour transformer les instances du modèle Parent en JSON, et vice-versa lors de la création d'un objet.

#doc INVITATION LIST
class InvitationList(generics.ListCreateAPIView): #doc Cette vue générique permet à la fois de lister (GET) et de créer (POST) des objets dans la base de données.
    queryset = Invitation.objects.all() #doc Définit l'ensemble des objets à renvoyer dans la vue. Ici, tous les objets Parent de la base de données seront renvoyés par la vue.
    serializer_class = InvitationSerializer #doc Indique à la vue d'utiliser le serializer ParentSerializer pour transformer les instances du modèle Parent en JSON, et vice-versa lors de la création d'un objet.

