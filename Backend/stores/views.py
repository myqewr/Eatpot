import random
from django.shortcuts import render
from stores.serializers import StoreSerializer, StoreRandomSerializer, Stores_Information, Serializers_Images
from .models import Images, Stores
from accounts.models import Users
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.http import JsonResponse 
import requests
from .secrets import KAKAO_API_KEY
import json
import selenium
from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
from selenium.webdriver.common.by import By
from Eatpository.settings import SECRET_KEY
import jwt


@api_view(['GET'])
def selected_stores(request):
    selected_editor = request.GET.get("editor")
    selected_category = request.GET.get("category")
    editor_num = 0
    store_list = []

    for i in selected_editor:
        editor_num = editor_num + 1
        if i == '1':

            user = Users.objects.get(user_num=editor_num)
            category_num = 0
            for j in selected_category:
                category_num = category_num + 1
                if j == '1':

                    if category_num == 1:
                        category = "한식"
                    elif category_num == 2:
                        category = "중식"

                    elif category_num == 3:
                        category = "일식"
                    elif category_num == 4:
                        category = "양식"

                    try:
                        stores = Stores.objects.filter(
                            user=user, category=category)
                    except:
                        pass
                    obj_num = stores.count()

                    for x in range(obj_num):
                        store = StoreSerializer(stores[x])
                        store_list.append(store.data)

    return Response({"stores": store_list})


@api_view(['GET'])
def random_store(request):
    try:
        access_token = request.META['HTTP_AUTHORIZATION']
        print(access_token)
        tok = jwt.decode(access_token, key=SECRET_KEY, algorithm='HS256')
        pk = tok.get('user_id')
        user = get_object_or_404(Users, pk=pk)
    except:
        return Response({"message": "acceess 토큰 필요함. 로그인 요구"})
    if user is not None:
        store_num = Stores.objects.count() + 1
        random_num = random.randrange(1, store_num)
        store = Stores.objects.get(id=random_num)
        store = StoreRandomSerializer(store)
        return Response({"random_sotre": store.data})


@api_view(['GET', 'POST'])
def edit(request):
    if request.method == "GET":
        return render(request, 'index.html')
    elif request.method == "POST":
        store = request.POST.get("store_name")
        searching = '홍대' + store

        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(
            searching)
        headers = {
            "Authorization":  KAKAO_API_KEY
        }
        try:
            places = requests.get(url, headers=headers).json()['documents'][0]
        except:
            return render(request, 'index2.html', {"message": "식당 정보를 불러올 수 없음"})

        data = {}

        data['id'] = places['id']
        data['store_name'] = places['place_name']
        data['main_menu'] = places['category_group_name']
        data['address'] = places['road_address_name']
        data['longitude'] = places['x']
        data['latitude'] = places['y']
        data['phone_number'] = places['phone']

        img_folder_path = r".\static\selenium_images"

        if not os.path.isdir(img_folder_path):
            os.mkdir(img_folder_path)

        # 노션에 있는 크롬 드라이버 설치 후 C 드라이브에 저장
        driver = webdriver.Chrome(r"C:\chromedriver.exe")
        driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

        search = "홍대" + store
        elem = driver.find_element(By.NAME, "q")
        elem.send_keys(search)
        elem.send_keys(Keys.RETURN)

        images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
        image_url = {}
        for i in range(10):
            try:
                images[i].click()
                time.sleep(0.5)
                imgUrl = driver.find_element(
                    By.XPATH, "//*[@id='Sva75c']/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img").get_attribute('src')
                # urllib.request.urlretrieve(
                #     imgUrl, f"{img_folder_path}/{places['id']}_{i+1}.jpg")
                # print(f"Image saved: {places['id']}_{i+1}.jpg")
                image_url[str(i+1)] = imgUrl
            except Exception as e:
                print(e)

        driver.close()

        return render(request, 'index2.html', {'info': data, 'image': image_url})


@api_view(['POST'])
def save(request):
    info = request.POST.get('info').replace("'", "\"")
    info = json.loads(info)
    print(info)
    image = request.POST.get('image').replace("'", "\"")
    image = json.loads(image)
    user = request.POST.get('user')
    image1 = request.POST.get('image1')
    image2 = request.POST.get('image2')
    image3 = request.POST.get('image3')
    image1 = image[image1]
    image2 = image[image2]
    image3 = image[image3]

    comment = request.POST.get('comment')
    user = Users.objects.get(username=user)
    store = Stores.objects.create(
        store_name=info['store_name'],
        main_menu=request.POST.get('main_menu'),
        address=info['address'],
        longitude=info['longitude'],
        latitude=info['latitude'],
        time=request.POST.get('time'),
        phone_number=info["phone_number"],
        user=user,
        category=request.POST.get('category'),
        admin_comment=comment
    )
    Images.objects.create(image1=image1, image2=image2,
                          image3=image3, store=store)
    return redirect('edit')


@api_view(['GET'])
def stores_information(request):
    if request.method == "GET":
        try:
            store_id = request.GET.get('store_id')
            store = Stores.objects.get(id=store_id)
            store_info = Stores_Information(store)
            images = Images.objects.get(store=store)

            images = Serializers_Images(images)
            return Response({"store_information": store_info.data, "store_images": images.data})
        except:
            return Response({"message": "error"})