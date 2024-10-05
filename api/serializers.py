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
        read_only_fields = ['sender', 'created_at', 'accepted'] 

    def create(self, validated_data):
        #doc GET THE AUTHENTICATED USER
        user = self.context['request'].user
        
        #doc GET THE PARENT INSTANCE ASSOCIATED WITH THE USER
        try:
            sender = Parent.objects.get(user=user)
        except Parent.DoesNotExist:
            raise serializers.ValidationError("No Parent associated with this user")

        #doc ASSOCIATE THE INVITATION WITH THE SENDER AND CONTINUE CREATION
        validated_data['sender'] = sender
        return super().create(validated_data)  #doc CALL THE PARENT CLASS CREATE METHOD
