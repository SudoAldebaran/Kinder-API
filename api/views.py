from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied

#doc MODELS: TABLES FROM THE DATABASE
from .models import Parent, Child, Household, Invitation

#doc SERIALIZERS: CONVERT PYTHON OBJECTS TO JSON
from .serializers import ParentSerializer, ChildSerializer, HouseholdSerializer, InvitationSerializer

#--------------------------------------- ALL: GET POST -----------------------------------------------------------------#

#doc PARENT LIST
class ParentList(generics.ListCreateAPIView): #doc THIS GENERIC VIEW ALLOWS LISTING (GET) AND CREATING (POST) OBJECTS IN THE DATABASE.
    queryset = Parent.objects.all() #doc DEFINES THE SET OF OBJECTS TO RETURN IN THE VIEW. HERE, ALL PARENT OBJECTS IN THE DATABASE WILL BE RETURNED.
    serializer_class = ParentSerializer #doc INDICATES TO THE VIEW TO USE THE ParentSerializer TO CONVERT PARENT MODEL INSTANCES TO JSON AND VICE-VERSA DURING OBJECT CREATION.

#doc CHILD LIST
class ChildList(generics.ListCreateAPIView): #doc THIS GENERIC VIEW ALLOWS LISTING (GET) AND CREATING (POST) OBJECTS IN THE DATABASE.
    queryset = Child.objects.all() #doc DEFINES THE SET OF OBJECTS TO RETURN IN THE VIEW. HERE, ALL CHILD OBJECTS IN THE DATABASE WILL BE RETURNED.
    serializer_class = ChildSerializer #doc INDICATES TO THE VIEW TO USE THE ChildSerializer TO CONVERT CHILD MODEL INSTANCES TO JSON AND VICE-VERSA DURING OBJECT CREATION.

#doc HOUSEHOLD LIST
class HouseholdList(generics.ListAPIView): #doc THIS GENERIC VIEW ALLOWS LISTING (GET) OF OBJECTS IN THE DATABASE.
    queryset = Household.objects.all() #doc DEFINES THE SET OF OBJECTS TO RETURN IN THE VIEW. HERE, ALL HOUSEHOLD OBJECTS IN THE DATABASE WILL BE RETURNED.
    serializer_class = HouseholdSerializer #doc INDICATES TO THE VIEW TO USE THE HouseholdSerializer TO CONVERT HOUSEHOLD MODEL INSTANCES TO JSON.

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
        return Invitation.objects.filter(recipient=parent) #doc FILTER BY THE CONNECTED USER

    def perform_create(self, serializer):
        user = self.request.user

        #doc GET THE PARENT INSTANCE ASSOCIATED WITH THE USER (SENDER)
        try:
            sender = Parent.objects.get(user=user)
        except Parent.DoesNotExist:
            raise ValueError("No Parent associated with this user")

        recipient_id = self.request.data.get('recipient')

        #doc GET THE RECIPIENT
        try:
            recipient = Parent.objects.get(id=recipient_id)
        except Parent.DoesNotExist:
            raise ValidationError("No Parent found with this ID")

        #doc CHECK IF THE USER IS SENDING AN INVITATION TO THEMSELVES
        if sender == recipient:
            raise ValidationError("You can't send an invitation to yourself")
        
        #doc CHECK IF AN INVITATION ALREADY EXISTS
        if Invitation.objects.filter(sender=sender, recipient=recipient).exists():
            raise ValidationError("An invitation has already been sent to this recipient.")

        if Invitation.objects.filter(sender=recipient, recipient=sender).exists():
            raise ValidationError("You have already received an invitation from this parent.")

        #doc CREATE A NEW HOUSEHOLD WITH BOTH PARENTS
        household = Household.objects.create(parent1=sender, parent2=recipient)

        #doc SAVE THE INVITATION WITH THE NEWLY CREATED HOUSEHOLD
        serializer.save(sender=sender, recipient=recipient, household=household)

#doc ALL CHILDREN BY PARENTS
class ChildrenParentsList(generics.ListCreateAPIView):
    serializer_class = ChildSerializer

    def get_queryset(self):
        parent_id = self.kwargs['pk'] #doc GET THE PARENT ID FROM THE URL
        parent = Parent.objects.get(pk=parent_id)
        return parent.children.all()
    
#--------------------------------------- BY ID: GET PUT DELETE -----------------------------------------------------------------#

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

        #doc GET THE INVITATION BY ITS ID
        try:
            invitation = Invitation.objects.get(id=invitation_id)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invitation not found'}, status=status.HTTP_404_NOT_FOUND)

        #doc CHECK IF THE CONNECTED USER IS THE RECIPIENT OF THE INVITATION
        if invitation.recipient.user != request.user:
            raise PermissionDenied("You are not authorized to decline this invitation")

        #doc GET THE HOUSEHOLD ASSOCIATED WITH THE INVITATION
        household = invitation.household

        #doc DELETE THE INVITATION
        self.perform_destroy(invitation)

        #doc CHECK IF THE HOUSEHOLD SHOULD BE DELETED
        #doc DELETE THE HOUSEHOLD IF THE DECLINED INVITATION WAS THE ONLY THING LINKING BOTH PARENTS
        if household.parent1 and household.parent2:
            #doc CHECK IF THERE ARE OTHER INVITATIONS LINKING THESE TWO PARENTS
            remaining_invitations = Invitation.objects.filter(household=household)
            if remaining_invitations.count() == 0:
                #doc DELETE THE HOUSEHOLD IF THERE ARE NO MORE INVITATIONS
                household.delete()

        return Response({'message': 'Invitation declined and household deleted successfully'}, status=status.HTTP_200_OK)
    
#doc ACCEPT INVITATION
class AcceptInvitationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]  #doc ENSURE THE USER IS AUTHENTICATED
    queryset = Invitation.objects.all()  #doc THE QUERYSET OF INVITATIONS
    serializer_class = InvitationSerializer

    def update(self, request, *args, **kwargs):
        #doc GET THE INVITATION BY ITS ID
        invitation_id = kwargs.get('pk')  #doc GET THE INVITATION ID FROM THE URL
        try:
            invitation = Invitation.objects.get(id=invitation_id)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invitation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        #doc CHECK IF THE CURRENT USER IS THE RECIPIENT OF THE INVITATION
        if invitation.recipient.user != request.user:
            return Response({'error': 'You are not authorized to accept this invitation'}, status=status.HTTP_403_FORBIDDEN)
        
        #doc CHECK IF THE INVITATION HAS ALREADY BEEN ACCEPTED
        if invitation.accepted:
            return Response({'error': 'This invitation has already been accepted'}, status=status.HTTP_400_BAD_REQUEST)

        #doc ACCEPT THE INVITATION BY SETTING THE 'accepted' FIELD TO TRUE
        invitation.accepted = True
        invitation.save()

        #doc RETURN A SUCCESSFUL RESPONSE
        return Response({'message': 'Invitation accepted successfully'}, status=status.HTTP_200_OK)
