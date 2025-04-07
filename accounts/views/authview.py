from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
import requests
from ..models import User
from ..serializers import UserIdentitySerializer


GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo/"


# class AuthenticationView(APIView):
#     permission_classes = [ AllowAny ]

#     def get(self, request):
#         logout(request)
#         return Response({'detail':'로그아웃 되었습니다'}, status.HTTP_200_OK)

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = authenticate(username=username, password=password)
#         if not user:
#             return Response({'detail':'아이디 혹은 비밀번호가 잘못되었습니다'}, status.HTTP_401_UNAUTHORIZED)
        
#         serializer = UserIdentitySerializer(user)
#         login(request, user)
#         return Response(serializer.data, status.HTTP_200_OK)
    

# class RegisterView(APIView):
#     permission_classes = [ AllowAny ]

#     def post(self, request):
#         serializer = UserIdentitySerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
#         user = serializer.save(role='STUDENT')
#         login(request, user)
#         return Response(serializer.data, status.HTTP_201_CREATED)
    

class GoogleAuthenticationView(APIView):
    permission_classes = [ AllowAny ]

    def get(self, request):
        logout(request)
        return Response({'detail':'로그아웃 되었습니다'}, status.HTTP_200_OK)
    
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'detail': 'Access token is required'}, status.HTTP_400_BAD_REQUEST)
        
        response = requests.get(GOOGLE_USER_INFO_URL, headers={
            'Authorization': f'Bearer {access_token}'
        })
        if response.status_code != 200:
            return Response({'detail':'Invalid access token'}, status.HTTP_400_BAD_REQUEST)
        
        user_data = response.json()
        email = user_data.get('email')
        name = user_data.get('name')

        user, created = User.objects.get_or_create(email=email, defaults={'username': name, 'email': email, 'role': 'STUDENT'})
        serializer = UserIdentitySerializer(user)
        login(request, user)
        return Response(serializer.data, status.HTTP_200_OK)