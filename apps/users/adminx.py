import xadmin
from xadmin import views
from .models import Banner, EmailVerifyRecord


class BaseSetting(object):
    enable_themes = True  # 可选多种页面主题
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "eduStack后台管理系统"
    site_footer = "eduStack(教育栈)"
    menu_style = "accordion"  # 左侧菜单栏可收缩


class BannerAdmin(object):

    list_display = ["index",  "image", "url", "create_time"]
    search_fields= ["image", "index", "url"]  # 搜索字段
    list_filter = ["index", "create_time"]  # 筛选字段


class EmailVerifyRecordAdmin(object):
    list_display = ["email", "code", "send_type", "send_time"]
    search_fields = ["email", "code"]
    list_filter = ["send_type", "send_time"]


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

