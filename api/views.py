from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied


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

#doc INVITATION LIST
class InvitationList(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            parent = Parent.objects.get(user=user)
        except Parent.DoesNotExist:
            raise ValueError("No Parent associated with this user")
        return Invitation.objects.filter(recipient=parent)

    def perform_create(self, serializer):
        user = self.request.user

        # Récupérer l'instance Parent associée à l'utilisateur (expéditeur/sender)
        try:
            sender = Parent.objects.get(user=user)
        except Parent.DoesNotExist:
            raise ValueError("No Parent associated with this user")

        recipient_id = self.request.data.get('recipient')

        # Récupérer le destinataire
        try:
            recipient = Parent.objects.get(id=recipient_id)
        except Parent.DoesNotExist:
            raise ValidationError("No Parent found with this ID")

        # Vérifier que l'utilisateur ne s'envoie pas l'invitation à lui-même
        if sender == recipient:
            raise ValidationError("You can't send an invitation to yourself")
        
        if Invitation.objects.filter(sender=sender, recipient=recipient).exists():
            raise ValidationError("An invitation has already been sent to this recipient.")

        if Invitation.objects.filter(sender=recipient, recipient=sender).exists():
            raise ValidationError("You have already received an invitation from this parent.")

        # Créer un nouveau ménage (household) avec les deux parents
        household = Household.objects.create(parent1=sender, parent2=recipient)

        # Sauvegarder l'invitation avec le ménage nouvellement créé
        serializer.save(sender=sender, recipient=recipient, household=household)

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

#doc INVITATION DETAILS + DECLINE INVITATION
class InvitationDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        invitation_id = kwargs.get('pk')

        # Récupérer l'invitation via son ID
        try:
            invitation = Invitation.objects.get(id=invitation_id)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invitation not found'}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur connecté est bien le destinataire de l'invitation
        if invitation.recipient.user != request.user:
            raise PermissionDenied("You are not authorized to decline this invitation")

        # Récupérer le ménage (household) associé à l'invitation
        household = invitation.household

        # Supprimer l'invitation
        self.perform_destroy(invitation)

        # Vérifier s'il faut supprimer le ménage (household)
        # On supprime le ménage si l'invitation refusée est la seule chose qui relie les deux parents
        if household.parent1 and household.parent2:
            # Vérifier s'il y a d'autres invitations qui lient ces deux parents
            remaining_invitations = Invitation.objects.filter(household=household)
            if remaining_invitations.count() == 0:
                # S'il n'y a plus d'invitations pour ce ménage, on le supprime
                household.delete()

        return Response({'message': 'Invitation declined and household deleted successfully'}, status=status.HTTP_200_OK)
    
#doc ACCEPT INVITATION
class AcceptInvitationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]  # Assure que l'utilisateur est authentifié
    queryset = Invitation.objects.all()  # Le queryset des invitations
    serializer_class = InvitationSerializer

    def update(self, request, *args, **kwargs):
        # Récupérer l'invitation via son ID
        invitation_id = kwargs.get('pk')  # Récupère l'ID de l'invitation depuis l'URL
        try:
            invitation = Invitation.objects.get(id=invitation_id)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invitation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifie que l'utilisateur actuel est bien le destinataire de l'invitation
        if invitation.recipient.user != request.user:
            return Response({'error': 'You are not authorized to accept this invitation'}, status=status.HTTP_403_FORBIDDEN)
        
        #doc VERIFIER QUE L'INVITATION N'EST PAS DEJA ACCEPTEE
        if invitation.accepted:
            return Response({'error': 'This invitation has already been accepted'}, status=status.HTTP_400_BAD_REQUEST)

        # Accepte l'invitation en mettant à jour le champ `accepted` à True
        invitation.accepted = True
        invitation.save()

        # Retourne la réponse avec succès
        return Response({'message': 'Invitation accepted successfully'}, status=status.HTTP_200_OK)