from rest_framework import serializers

#doc IMPORTING ALL THE MODELS
from .models import Parent, Child, Household, Invitation

#doc PARENT SERIALIZER
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent 
        fields = ['id', 'name', 'email']

#doc CHILD SERIALIZER
class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'name', 'parent']

#doc HOUSEHOLD SERIALIZER
class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ['id', 'parent1', 'parent2']

#doc INVITATION SERIALIZER
class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'household', 'created_at', 'accepted']

