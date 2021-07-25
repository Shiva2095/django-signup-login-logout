import json
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout


class RegisterUser(APIView):
    """
    A view that can accept POST requests with JSON content.
    """

    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        try:
            data = []
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                account.is_active = True
                account.save()
                token = Token.objects.get_or_create(user=account)[0].key
                serializer_data = serializer.data

                serializer_data["message"] = "user registered successfully"
                serializer_data["token"] = token
                
            else:
                data = serializer.errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer_data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            raise ValidationError({"400": f'{str(e)}'})


class Login(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data = {}
        reqBody = json.loads(request.body)
        username = reqBody['username']
        print(username)
        password = reqBody['password']
        try:
            account = Profile.objects.get(username=username)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=account)[0].key
        print(token)
        if not check_password(password, account.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if account:
            if account.is_active:
                print(request.user)
                login(request, account)
                data["message"] = "user logged in"
                data["username"] = account.username

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})


class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()

        logout(request)

        return Response('User Logged out successfully')