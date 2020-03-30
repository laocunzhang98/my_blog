import xadmin
from article.models import Article, Tag


class ArticleAdmin(object):
    #  页面中显示的列
    list_display = ['title', 'click_num', 'love_num', 'user']
    # 搜索
    search_fields = ['title', 'id']
    # 可编辑的列
    list_editable = ['click_num', 'love_num']
    list_filter = ['date', 'user']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag)
