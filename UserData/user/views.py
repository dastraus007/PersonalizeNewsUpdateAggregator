from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ViewSet):
    def list1(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error occurred while retrieving users: %s", str(e))
            return Response(
                {"error": "An error occurred while retrieving users."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error("Error occurred while creating a user: %s", str(e))
                return Response(
                    {"error": "An error occurred while creating the user."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            logger.error("Invalid data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, un=None, passw=None):
        """Handles retrieving a user."""
        try:
            user = User.objects.filter(email=un).first()
            if not user:
                logger.warning(f"User not found: {un}")
                raise AuthenticationFailed('User not found!')

            if not user.password==passw:
                logger.warning(f"Incorrect password for user: {un}")
                raise AuthenticationFailed('Incorrect password!')

            serializer = UserSerializer(instance=user)
            return Response(serializer.data)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Error in retrieving user: {e}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






    def update(self, request, un=None, passw=None):
        """Handles updating a user."""
        try:
            user = User.objects.filter(email=un).first()
            if not user:
                logger.warning(f"User not found: {un}")
                raise AuthenticationFailed('User not found!')

            if user.password != passw:
                logger.warning(f"Incorrect password for user: {un}")
                raise AuthenticationFailed('Incorrect password!')

            serializer = UserSerializer(instance=user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Error in updating user: {e}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)