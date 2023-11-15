from rest_framework import serializers
from .models import CustomUser, ProgrammingLanguage, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'country', 'residence']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            age=validated_data.get('age', None),
            country=validated_data.get('country', ''),
            residence=validated_data.get('residence', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ['id', 'name', 'level']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'description', 'maximum_collaborators', 'collaborators']

class CollaborationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    skills = SkillSerializer(many=True)