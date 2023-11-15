from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, ChangePasswordSerializer, SkillSerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, Skill, Project, ProgrammingLanguage, Collaboration

#REGISTER USER

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#LOGIN USER

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#LOGOUT USER

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#CHANGE PASSWORD

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_skill(request):
    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_skill(request, skill_id):
    if request.method == 'DELETE':
        try:
            skill = ProgrammingLanguage.objects.get(id=skill_id, user=request.user)
            skill.delete()
            return Response({'message': 'Skill removed successfully.'}, status=status.HTTP_200_OK)
        except ProgrammingLanguage.DoesNotExist:
            return Response({'error': 'Skill not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id):
    if request.method == 'DELETE':
        try:
            project = Project.objects.get(id=project_id, creator=request.user)
            project.delete()
            return Response({'message': 'Project deleted successfully.'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def express_interest(request, project_id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(id=project_id)
            collaboration, created = Collaboration.objects.get_or_create(project=project, user=request.user)
            if created:
                return Response({'message': 'Interest expressed successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'You have already expressed interest in this project.'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_collaboration(request, collaboration_id):
    if request.method == 'POST':
        try:
            collaboration = Collaboration.objects.get(id=collaboration_id, project__creator=request.user)
            collaboration.accepted = True
            collaboration.save()
            return Response({'message': 'Collaboration request accepted.'}, status=status.HTTP_200_OK)
        except Collaboration.DoesNotExist:
            return Response({'error': 'Collaboration request not found.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError:
            return Response({'error': 'You do not have permission to accept this collaboration request.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_collaboration(request, collaboration_id):
    if request.method == 'POST':
        try:
            collaboration = Collaboration.objects.get(id=collaboration_id, project__creator=request.user)
            collaboration.delete()
            return Response({'message': 'Collaboration request declined and deleted.'}, status=status.HTTP_200_OK)
        except Collaboration.DoesNotExist:
            return Response({'error': 'Collaboration request not found.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError:
            return Response({'error': 'You do not have permission to decline this collaboration request.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_statistics(request):
    if request.method == 'GET':
        projects_contributed = Project.objects.filter(collaborators=request.user).count()
        projects_created = Project.objects.filter(creator=request.user).count()
        return Response({'projects_contributed': projects_contributed, 'projects_created': projects_created}, status=status.HTTP_200_OK)