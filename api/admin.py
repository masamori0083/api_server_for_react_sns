"""管理画面の認証のカスタマイズをする"""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models


# emailで認証ができるように、認証フィールドをカスタマイズする
# djangoデフォルトのUserAdminをオーバーライト
# デコレーターはUserAdminクラスをUserモデルに関連付けて管理画面に登録する
# 管理画面の各ユーザーページで表示されるフィールドを設定。
@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ["email"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',), # タプルかリスト
        }),
        (_('Important dates'), {'fields': ('last_login',)}), # タプルかリスト
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2'),
        }),
    )

# 各モデルを管理サイトに登録
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Comment)