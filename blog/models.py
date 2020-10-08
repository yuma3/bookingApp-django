from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _  # 国際化
from django.core.mail import send_mail
from django.utils import timezone

# Create your models here.


""" Customize UserModel  """


class UserManager(BaseUserManager):
    """ User作成のためのヘルパークラス """

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """ メールアドレスでの登録を必須にする """
        if not username:
            raise ValueError("Users must have an name.")
        if not email:
            raise ValueError("The given email must be set.")

        """ normalizeで正規表現化 """
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        """ User作成 """
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """ is_staff(管理サイトにログインできるか),is_superuser(全ての権限)をFalse """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """ スーパーユーザーはis_staff, is_superuserをTrueに """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser must have is_superuser=Ture")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ カスタムユーザーモデル """

    username = models.CharField(_("username"), max_length=30, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts"
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    # usernameを入れないとcreatesuperuserで作成できない
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """ Return the first name plus the last name, with a space in between """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    def get_short_name(self):
        """ Return the short name for the user """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this user """
        send_mail(subject, message, from_email, [self.email], **kwargs)


""" Blog Model """


class Tag(models.Model):

    name = models.CharField("タグ名", max_length=255, unique=True)

    def __str__(self):

        if hasattr(self, "post_count"):
            return f"{self.name}({self.post_count})"
        else:
            return self.name


class Post(models.Model):

    title = models.CharField("タイトル", max_length=32)
    text = models.TextField("本文")
    tags = models.ManyToManyField(Tag, verbose_name="タグ", blank=True)
    thumbnail = models.ImageField(
        "サムネイル", upload_to="post_thumbnail/%Y/%m/%d", blank=True, null=True
    )
    relation_posts = models.ManyToManyField("self", verbose_name="関連記事", blank=True)
    is_public = models.BooleanField("公開可能か", default=True)
    description = models.TextField("記事の説明", blank=True, max_length=130)
    keywords = models.CharField("記事のキーワード", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField("作成日", default=timezone.now)
    updated_at = models.DateTimeField("更新日", default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):

    name = models.CharField("名前", max_length=255, default="名無し")
    text = models.TextField("本文")
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="対象記事")
    created_at = models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):
        return self.text[:20]


class Reply(models.Model):

    name = models.CharField("名前", max_length=255, default="名無し")
    text = models.TextField("本文")
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="対象コメント")
    created_at = models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):
        return self.text[:20]
