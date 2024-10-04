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
        fields = ['id', 'name', 'age', 'parent']

#doc HOUSEHOLD SERIALIZER
class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ['id', 'parent1', 'parent2']

#doc INVITATION SERIALIZER
class InvitationSerializer(serializers.ModelSerializer):

    recipient = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all())
    household = serializers.PrimaryKeyRelatedField(queryset=Household.objects.all())

    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'household', 'created_at', 'accepted']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user # Définit l'expéditeur à l'utilisateur authentifié
        return super().create(validated_data) # Appelle la méthode create de la classe parente