from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings

# Create your models here.


def upload_avatar_path(instance: object, filename: str) -> str:
    """プロフィール画像のパスを返す"""
    # 拡張子を取得
    ext = filename.split(".")[-1]
    return "/".join(
        [
            "avatars",
            str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext),
        ]
    )


def upload_post_path(instance: object, filename: str) -> str:
    """ユーザーがポストした画像のファイルパスを返す"""
    ext = filename.split(".")[-1]
    return "/".join(
        ["posts", str(instance.userPost.id) + str(instance.title) + str(".") + str(ext)]
    )


class UserManager(BaseUserManager):
    """
    デフォルトでのユーザー作成の方法を、ユーザー名ではなくて、
    - メールアドレス
    - パスワード
    にする
    """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("email is must")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)

        # マルチデータベース環境の場合、以下の指定が必要。
        # 一つのデータベースしか使わない場合、using=self._dbは不要
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    django標準のユーザーモデルを、メールアドレス・パスワード認証にカスタマイズ。
    このクローンアプリを使うユーザーを作成する。
    """

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    # ユーザーネームのフィールドをデフォルトでemailにする
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    ユーザーのプロフィールのモデル
    """

    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="userProfile", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName


class Post(models.Model):
    title = models.CharField(max_length=100)
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userPost", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)

    # いいねのリレーションは多対多
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked", blank=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userComment", on_delete=models.CASCADE
    )

    # どのポストに対するコメントかを識別する。Postに紐付ける
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
