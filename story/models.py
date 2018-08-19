from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.utils.timezone import now
from django.db import models

# Create your models here.

TAGS = (
    (0, "なし"),
    (1, "雰囲気ぶっ壊しok"),
    (2, "異世界"),
    (3, "恋愛"),
    (4, "転生"),
    (5, "冒険"),
    (6, "r18"),
)


STARS = (
    (1, "★"),
    (2, "★★"),
    (3, "★★★"),
    (4, "★★★★"),
    (5, "★★★★★"),
)


class AuthUserManager(BaseUserManager):
    def create_user(self, username, email, password, age):
        if not email:
            raise ValueError('Users must have an email')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(username=username, email=email, password=password, age=age)
        user.already_start_story = False
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, age):
        user = self.create_user(username=username, email=email, password=password, age=age)
        user.already_start_story = False
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    def get_short_name(self):
        ...

    def get_full_name(self):
        ...

    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True)
    age = models.IntegerField("年齢", validators=[MaxValueValidator(150), MinValueValidator(1)], default=20)
    already_start_story = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'email'
    _USERNAME_FIELD_ = 'username'
    REQUIRED_FIELDS = ['username', 'age']
    objects = AuthUserManager()

    def get_username(self):
        """Return the identifying username for this User"""
        return getattr(self, self.USERNAME_FIELD)


class Story(models.Model):
    name = models.CharField("題名", max_length=50, default="")
    first_text = models.TextField("本文", max_length=5000, default="")
    starter = models.ForeignKey(AuthUser)
    start_datetime = models.DateTimeField(default=now)
    last_added = models.DateTimeField(default=now)
    last_added_user = models.CharField("最後に追加したユーザー名", default="", max_length=255)
    tag1 = models.IntegerField(choices=TAGS, default=0)
    tag2 = models.IntegerField(choices=TAGS, default=0)
    tag3 = models.IntegerField(choices=TAGS, default=0)

    def __str__(self):
        return self.name


class Entry(models.Model):
    text = models.TextField("本文", max_length=5000)
    user = models.ForeignKey(AuthUser)
    story = models.ForeignKey(Story)
    create_datetime = models.DateTimeField(default=now)

    def __str__(self):
        return self.text


class Profile(models.Model):
    # name = models.CharField("ハンドルネーム", max_length=255)
    profile_text = models.TextField("自己紹介", max_length=1000, default="")
    user = models.OneToOneField(AuthUser)

    def __str__(self):
        return self.user.username


class Write_Entry(models.Model):
    """次に書く人"""
    user = models.ForeignKey(AuthUser)
    story = models.ForeignKey(Story)

    def __str__(self):
        return self.user.username


class Evaluation(models.Model):
    """評価"""
    nice = models.IntegerField(default=0)
    story = models.OneToOneField(Story)
    nice_users = models.ManyToManyField(AuthUser)

    def __str__(self):
        return self.story.name


class Comment(models.Model):
    user = models.ForeignKey(AuthUser)
    story = models.ForeignKey(Story, null=True)
    star = models.IntegerField(choices=STARS, default=3)
    text = models.TextField(max_length=100, default="")

    def __str__(self):
        return self.user.username
