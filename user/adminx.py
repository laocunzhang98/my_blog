import xadmin

from xadmin import views
from user.models import Friend_link

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '博客后台管理'
    site_footer = '王伟的博客公司'


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Friend_link)