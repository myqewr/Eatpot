import jwt
import json
from Eatpository.settings import SECRET_KEY
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib import auth
from django.contrib.auth import login, logout
from .models import Users
from Eatpository import settings


import random
import string


#from Eatpository.settings import JWT_ALGORITHM, JWT_SECRET_KEY
# Create your views here.
@api_view(['POST'])
def loginCheck(request):

    try:
        access_token = request.META['HTTP_AUTHORIZATION']

        access_token = access_token[7:]
        access_token = jwt.decode(
            access_token, key=SECRET_KEY, algorithm='HS256')
        pk = access_token.get('user_id')
        user = Users.objects.get(pk=pk)
    except:
        return Response({'message': 'user does not exist'})
    if user is not None:
        return Response({'message': 'success'})
    else:
        return Response({'message': 'noAccess'})


@api_view(['POST'])
def loginValidate(request):
    try:
        # 클라이언트에게 refresh_token 받기
        refresh_token = request.META['HTTP_AUTHORIZATION']
        refresh_token = refresh_token[7:]
        refresh_token_deco = jwt.decode(
            refresh_token, key=SECRET_KEY, algorithm='HS256')

        pk = refresh_token_deco.get('user_id')
        user = Users.objects.get(pk=pk)
    except:
        return Response({'message': 'loginAgain'})

    # refresh token 존재하는지 확인
    if user is not None:
        # 유효한 refresh token인지 확인
        if user.refresh_token == refresh_token:
            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)

            return Response({'message': 'access_token_update', 'access_token': access_token})
    else:
        return Response({'message': 'loginAgain'})

# 회원가입
@api_view(['POST'])
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get("user_id")
        password = data.get("password")
        phone_number = data.get("phone_number")
        user = Users.objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number,
            role=False)
        user.save()

        auth.login(request, user)

        return Response({"message": "회원가입 성공"})

# 로그인
@api_view(['POST'])
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get("user_id")
        password = data.get("password")

        try:
            # 사용자가 입력한 user_id 를 Users 모델 내 username filed로
            user = Users.objects.get(username=username)
        except:
            return Response({"message": "error"})

        if auth.authenticate(request, username=username, password=password):
            auth.login(request, user)

            # 로그인시 refresh_token 발급
            token = RefreshToken.for_user(user)
            refresh_token = str(token)

            # 발급한 refresh_token을 user 객체에 저장
            user.refresh_token = refresh_token
            user.save()

            # access_token 발급
            access_token = str(token.access_token)

            # 클라이언트에 access_totken과 refresh_token 전달
            response = Response(
                {"message": "success", "access_token": access_token, "refresh_token": refresh_token})

            return response

        else:
            return Response({"message": "UserNot"})


def home(request):
    return render(request, 'index.html')


def user_logout(request):
    logout(request)
    return redirect('home')


# 아이디 찾기
@api_view(['GET'])
def user_id(request):
    if request.method == "GET":
        try:
            phone_number = request.GET.get("phone_number")
            user_id = Users.objects.get(phone_number=phone_number).username
        except:
            return Response({"message": "error"})

        if user_id is not None:
            return Response({"user_id": user_id})
        else:
            return Response({"message": "user does not exist"})

# 비밀번호 찾기
@api_view(['GET'])
def user_password(request):
    if request.method == "GET":
        try:
            user_id = request.GET.get("user_id")
            phone_number = request.GET.get("phone_number")

            user = Users.objects.get(username=user_id)
        except:
            return Response({"message": "user does not exist : except occurs"})
        if user is not None:
            # 전화 번호로 유효한 user 확인
            if user.phone_number == phone_number:
                # 새로 입력한 password를 user 객체에 저장
                new_pw = request.GET.get("new_password")
                user.set_password(new_pw)
                user.save()

                # 로그인
                auth.login(request, user)
                return Response({"message": "비밀번호 변경"})
            else:
                return Response({"message": "user does not exist : phone_num not correct"})
        else:
            return Response({"message": "user does not exist : user_id not correct"})

# 비밀번호 재설정
@api_view(['PATCH'])
def new_password(request):
    if request.method == "PATCH":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("user_id")
        password = data.get("password")
        re_password = data.get("re_password")

        try:
            user = Users.objects.get(username=username)
        except:
            return Response({"message": "user does not exist"})

        # 기존 password
        if user.password == password:
            user.password = re_password
            user.save()
            return Response({"message": "password changed"})
        else:
            return Response({"message": "user does not exist"})
