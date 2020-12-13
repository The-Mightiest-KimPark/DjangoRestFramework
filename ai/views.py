from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, status, filters

from .serializers import GrocerySerializer, AllGrocerySerializer
from refrigerator.serializers import PhotoSerializer
from refrigerator.models import Photo
from .models import Grocery, AllGrocery
from bigdata.views import BdRecommRecipe
from refrigerator.models import Refrigerator

from pytz import timezone

import json
import datetime

# from django.utils import timezone

# AI 이미지 분석을 통한 결과 저장
# 만든이 : snchoi
@api_view(['POST'])
def AiImgGrocery(request):
    # 이미지 정보 받음
    params = request.data
    url = params['url']
    reg_date = params['reg_date']
    # reg_date = datetime.datetime.now(timezone('Asia/Seoul'))
    # reg_date = datetime.datetime.strptime(reg_date, '%Y-%m-%d %H:%M:%S.%f')
    # reg_date = reg_date(timezone('Asia/Seoul'))

    print('reg_date : ', reg_date)
    fridge_number = params['fridge_number']

    # 냉장고 번호를 통해 아이디 값 가져오기
    refri = Refrigerator.objects.get(fridge_number=fridge_number)
    email = refri.email
    print('email : ', email)

    # 이미지 저장
    serializer = PhotoSerializer(data={"email":email,"file_name":fridge_number,"url":url,"reg_date":reg_date})
    if serializer.is_valid():
        serializer.save()
        print('이미지 저장 성공')
    else:
        print('이미지 저장 실패')

    # AI분석 로직
    ai_result = [{
        'all_grocery_id': 1,
        'name' : '바나나',
        'count' : 3,
        'coordinate' : "[[1,2],[3,2]]"
    },{
        'all_grocery_id': 2,
        'name' : '사과',
        'count' : 1,
        'coordinate' : "[[1,2],[3,2]]"
    },{
        'all_grocery_id': 3,
        'name' : '고구마',
        'count' : 2,
        'coordinate' : "[[1,2],[3,2]]"
    }]

    # 빅데이터 함수 호출(냉장고 번호와 재료들 넘겨줘야함?)
    BdRecommRecipe(data=ai_result, email= email)

    # 결과 저장
    for result in ai_result:
        result['email'] = email
        result['reg_date'] = reg_date
        print('result[reg_date] : ', result['reg_date'])
        result['gubun'] = 1

        serializer = GrocerySerializer(data=result)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# AI 이미지 분석을 통한 결과 저장 복사본
# 만든이 : snchoi
@api_view(['POST'])
def AiImgGroceryTest(request):
    # 이미지 정보 받음
    params = request.data
    url = params['url']
    reg_date = params['reg_date']
    # reg_date = datetime.datetime.now(timezone('Asia/Seoul'))
    # reg_date = datetime.datetime.strptime(reg_date, '%Y-%m-%d %H:%M:%S.%f')
    # reg_date = reg_date(timezone('Asia/Seoul'))

    print('reg_date : ', reg_date)
    fridge_number = params['fridge_number']

    # 냉장고 번호를 통해 아이디 값 가져오기
    refri = Refrigerator.objects.get(fridge_number=fridge_number)
    email = refri.email
    print('email : ', email)

    
    # 이전 날짜 이미지 다 삭제
    Photo.objects.filter(email=email).delete()
    
    # 이미지 저장
    serializer = PhotoSerializer(data={"email":email,"file_name":fridge_number,"url":url,"reg_date":reg_date})
    if serializer.is_valid():
        serializer.save()
        print('이미지 저장 성공')
    else:
        print('이미지 저장 실패')

    # AI분석 로직
    ai_result = [{
        'all_grocery_id': 1,
        'name' : '바나나',
        'count' : 3,
        'coordinate' : "[[1,2],[3,2]]"
    },{
        'all_grocery_id': 2,
        'name' : '사과',
        'count' : 1,
        'coordinate' : "[[1,2],[3,2]]"
    },{
        'all_grocery_id': 3,
        'name' : '고구마',
        'count' : 2,
        'coordinate' : "[[1,2],[3,2]]"
    }]

    # 빅데이터 함수 호출(냉장고 번호와 재료들 넘겨줘야함?)
    BdRecommRecipe(data=ai_result, email= email)

    # 이전 결과 다 삭제
    Grocery.objects.filter(email=email).delete()
    
    # 결과 저장
    for result in ai_result:
        result['email'] = email
        result['reg_date'] = reg_date
        print('result[reg_date] : ', result['reg_date'])
        result['gubun'] = 1

        serializer = GrocerySerializer(data=result)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



# 전체 재료 이름, 재료id 조회 - 직접 입력 시 존재하는 재료에서 선택하도록 
# 만든이 : snchoi
class AllGroceryName(generics.ListCreateAPIView):
    queryset = AllGrocery.objects.all()
    serializer_class = AllGrocerySerializer



# 가장 최근 재료 조회(gubun=1 : 이미지 인식 ,  gubun=2 : 직접입력) / 사용자 재료 입력
# 만든이 : snchoi
@api_view(['GET','POST', 'PUT', 'DELETE'])
def userInputGrocery(request):

    # 재료 조회(gubun=1 : 이미지 인식 ,  gubun=2 : 직접입력)
    if request.method == 'GET':
        gubun = request.GET.get('gubun')
        email = request.GET.get('email')

        # latest_date = Grocery.objects.filter(Q(gubun=gubun),Q(email=email)).order_by('-reg_date')[:1].values_list('reg_date', flat=True)
        # queryset = Grocery.objects.filter(Q(gubun=gubun),Q(email=email),Q(reg_date=latest_date))
        queryset = Grocery.objects.filter(Q(gubun=gubun),Q(email=email))
        serializer = GrocerySerializer(queryset, many=True)
        return Response(serializer.data)
    
    # 사용자 재료 입력
    elif request.method == 'POST':
        data = request.data
        data['gubun'] = 2 #구분값은 직접입력 값인 2로 지정
        serializer = GrocerySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 사용자 입력 재료 수정
    elif request.method == 'PUT':
        data = request.data
        email = data['email']
        name = data['name']
        count = data['count']
        all_grocery_id = data['all_grocery_id']
        try:
            grocery_queryset = Grocery.objects.get(Q(all_grocery_id=all_grocery_id),Q(email=email),Q(gubun=2))
            grocery_queryset.name = name
            grocery_queryset.count = count
            grocery_queryset.all_grocery_id = data['all_grocery_id']

            try:
                grocery_queryset.save()
                return Response({"result":True}, status=status.HTTP_201_CREATED)
            except:
                return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({"result":False}, status=status.HTTP_404_NOT_FOUND)


    # 사용자 입력 재료 삭제
    elif request.method == 'DELETE':
        data = request.data
        email = data['email']
        all_grocery_id = data['all_grocery_id']
        try:
            queryset = Grocery.objects.get(Q(all_grocery_id=all_grocery_id),Q(email=email))
            queryset.delete()
        except:
            return Response({"result":False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"result":True}, status=status.HTTP_201_CREATED)


        

