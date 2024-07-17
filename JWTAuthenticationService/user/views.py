import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, APIException
from .serializers import UserSerializer
from .models import User
from datetime import datetime
import jwt, datetime
import requests
from rest_framework.response import Response

url = 'http://docker.for.mac.localhost:8022/api/users/'
urluser = 'http://docker.for.mac.localhost:8022/api/user'

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Invalid data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            response = requests.post(urluser, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Error occurred while registering user: %s", str(e))
            raise APIException(f'Error occurred while registering user: {str(e)}')

        if response.status_code == status.HTTP_201_CREATED:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Unexpected response from external service: %s", response.status_code)
            raise APIException(f'Unexpected response from external service: {response.status_code}')




class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
     #   url = 'http://docker.for.mac.localhost:8022/api/users/'
        try:
            response = requests.get(f'{url}{email},{password}')
            response.raise_for_status()
        except requests.RequestException as e:
            raise AuthenticationFailed(f'Error occurred while fetching user: {str(e)}')
        user_data = response.json()
        user = User(**user_data)
        if not user:
            raise AuthenticationFailed('User not found!')


        # Prepare JWT payload
        #return Response("user_data")
        payload = {
            'email': user.email,
            'password':password,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')
        email=payload['email']
        password=payload['password']
        try:
            response = requests.get(f'{url}{email},{password}')
            response.raise_for_status()
        except requests.RequestException as e:
            raise AuthenticationFailed(f'Error occurred while fetching user: {str(e)}')

        user_data = response.json()
        return Response(user_data)

    def put(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')

        email = payload['email']
        password = payload['password']

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            response = requests.put(f'{url}{email},{password}', json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            raise AuthenticationFailed(f'Error occurred while fetching user: {str(e)}')
        user_data = response.json()
        return Response(user_data)

class LogoutView(APIView):
    def get(self, request):
        try:
            response = Response({'message': 'success'}, status=status.HTTP_200_OK)
            response.delete_cookie('jwt')
            return response
        except Exception as e:
            logger.error("Error occurred during logout: %s", str(e))
            return Response(
                {"error": "An error occurred during logout."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )