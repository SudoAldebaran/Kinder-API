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

    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'created_at', 'accepted']
        read_only_fields = ['sender', 'created_at', 'accepted']  # Assure-toi que 'sender' est en lecture seule

    def create(self, validated_data):
        # Récupère l'utilisateur authentifié
        user = self.context['request'].user
        
        # Récupère l'instance Parent associée à l'utilisateur
        try:
            sender = Parent.objects.get(user=user)
        except Parent.DoesNotExist:
            raise serializers.ValidationError("No Parent associated with this user")

        # Associe l'invitation avec l'expéditeur (sender) et continue la création
        validated_data['sender'] = sender
        return super().create(validated_data)
