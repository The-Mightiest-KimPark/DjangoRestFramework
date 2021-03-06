from rest_framework import serializers
from .models import UserInfo, Follow, RecipeFavorite, Alarm
from refrigerator.models import Photo


# 사용자
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields= '__all__'

# 팔로우
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields= '__all__'

# 레시피 즐겨찾기
class RecipeFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeFavorite
        fields= '__all__'


# 식료품 알림
class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields= '__all__'


# # 팔로우 최신 사진 조회
# class CustomizingFollowSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(read_only=True)
#     class Meta:
#         model = Photo
#         fields= ('email, url, reg_date, name')


# 비밀번호 제외 유저정보
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = [
            'email',
            'age',
            'sex',
            'phone_number',
            'name',
            'guardian_name',
            'guardian_phone_number',
            'purpose',
            # 'img_url'
        ]

class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = [
            'email',
            'age',
            'sex',
            'phone_number',
            'name',
            'guardian_name',
            'guardian_phone_number',
            'purpose'
        ]