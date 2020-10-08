from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import Post
from .models import Comment
from .models import Reply
from .models import Tag

# Register your models here.


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email',)


class MyUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields':('username', 'email', 'password')}),
        (_('Personal info'),{'fields':('first_name', 'last_name')}),
        (_('Permissions'), {'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields':('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('username', 'email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class ReplyInline(admin.StackedInline):

    model = Reply
    extra = 5


class CommentAdmin(admin.ModelAdmin):

    inlines = [ReplyInline]


class PostAdmin(admin.ModelAdmin):

     search_fields = ('title', 'text')
     list_display = ['title', 'is_public', 'updated_at', 'created_at', 'title_len']
     list_filter = ['is_public', 'tags']
     ordering = ('-updated_at',)

     def title_len(self, obj):
         return len(obj.title)

     title_len.short_description = 'タイトルの文字数'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
admin.site.register(Tag)