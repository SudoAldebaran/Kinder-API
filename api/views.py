from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

#doc MODELS : TABLES FROM THE DATABASE
from .models import Parent, Child, Household, Invitation

#doc SERIALIZERS : CONVERT PYTHON OBJECTS TO JSON
from .serializers import ParentSerializer, ChildSerializer, HouseholdSerializer, InvitationSerializer

#--------------------------------------- ALL : GET POST -----------------------------------------------------------------#

#doc PARENT LIST
class ParentList(generics.ListCreateAPIView): #doc Cette vue générique permet à la fois de lister (GET) et de créer (POST) des objets dans la base de données.
    queryset = Parent.objects.all() #doc Définit l'ensemble des objets à renvoyer dans la vue. Ici, tous les objets Parent de la base de données seront renvoyés par la vue.
    serializer_class = ParentSerializer #doc Indique à la vue d'utiliser le serializer ParentSerializer pour transformer les instances du modèle Parent en JSON, et vice-versa lors de la création d'un objet.

#doc CHILD LIST
class ChildList(generics.ListCreateAPIView): #doc Cette vue générique permet à la fois de lister (GET) et de créer (POST) des objets dans la base de données.
    queryset = Child.objects.all() #doc Définit l'ensemble des objets à renvoyer dans la vue. Ici, tous les objets Parent de la base de données seront renvoyés par la vue.
    serializer_class = ChildSerializer #doc Indique à la vue d'utiliser le serializer ParentSerializer pour transformer les instances du modèle Parent en JSON, et vice-versa lors de la création d'un objet.

#doc HOUSEHOLD LIST
class HouseholdList(generics.ListAPIView): #doc Cette vue générique permet à la fois de lister (GET) et de créer (POST) des objets dans la base de données.
    queryset = Household.objects.all() #doc Définit l'ensemble des objets à renvoyer dans la vue. Ici, tous les objets Parent de la base de données seront renvoyés par la vue.
    serializer_class = HouseholdSerializer #doc Indique à la vue d'utiliser le serializer ParentSerializer pour transformer les instances du modèle Parent en JSON, et vice-versa lors de la création d'un objet.

class InvitationList(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            parent = Parent.objects.get(user=user)
        except Parent.DoesNotExist:
            raise ValueError("No Parent associated with this user")
        return Invitation.objects.filter(recipient=parent)  # Filtre par l'utilisateur connecté
    
    def perform_create(self, serializer):
        recipient_id = self.request.data.get('recipient')
        household_id = self.request.data.get('household')

        try:
            recipient = Parent.objects.get(id=recipient_id)
        except Parent.DoesNotExist:
            raise ValueError("No Parent found with this ID")

        try:
            household = Household.objects.get(id=household_id)
        except Household.DoesNotExist:
            raise ValueError("No Household found with this ID")

        serializer.save(recipient=recipient, household=household)

     

#doc ALL CHILDREN BY PARENTS
class ChildrenParentsList(generics.ListCreateAPIView):
    serializer_class = ChildSerializer

    def get_queryset(self):
        parent_id = self.kwargs['pk'] # Récupère l'ID du parent depuis l'URL
        parent = Parent.objects.get(pk=parent_id)
        return parent.children.all()
    
#--------------------------------------- BY ID : GET PUT DELETE -----------------------------------------------------------------#

#doc PARENT DETAILS 
class ParentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

#doc CHILD DETAILS
class ChildDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer