from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
import random
import string

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)  # 이메일 필드를 추가하고 고유(unique)하게 설정
    nickname = models.CharField(max_length=30, unique=True) # 닉네임
    profile = models.CharField(max_length=255, null=True, blank=True) # 프로필
    profile_image = models.ImageField(upload_to='profile_images/%Y/%m/%d/', null=True, blank=True) # 프로필 사진
    region = models.CharField(max_length=30, null=True, blank=True) # 사는 지역 -> 후에 태그로 변환
    region_detail = models.CharField(max_length=30, null=True, blank=True) # 사는 지역 디테일

    def __str__(self):
        return self.nickname
    
    # 유저를 선택했을 때 사용할 유저의 이름
    USERNAME_FIELD = "email"

    #db에서의 테이블 이름 설정
    class Meta:
        db_table = "User"

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.generate_random_nickname()
        super().save(*args, **kwargs)

    def generate_random_nickname(self):
        # 랜덤한 문자열을 생성하는 예제
        # 여기서는 8자리의 랜덤한 소문자 문자열을 생성
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))