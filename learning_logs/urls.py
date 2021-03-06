"""定义learning_logs的URL模式。"""
from django.urls import path
from . import views
app_name = 'learning_logs'
urlpatterns = [
    #主页
    path('',views.index,name='index'),
    #显示所有主题
    path('topics/',views.topics,name='topics'),
    #显示单个主题的所有条目
    path('topics/<int:topic_id>',views.topic,name='topic'),
    #用于添加新主题的页面
    path('new_topic/',views.new_topic,name='new_topic'),
]