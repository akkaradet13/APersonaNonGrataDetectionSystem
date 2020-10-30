from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('getData', views.getData, name='getdata'),
    path('AllData', views.allData, name='AllData'),
    path('GroupData', views.groupData, name='GroupData'),
    path('SearchData', views.searchData, name='SearchData'),
    path('SettingCamera', views.settingCamera, name='SettingCamera'),
    path('ActionDoor', views.actionDoor, name='ActionDoor'),
    path('404', views.notFound, name='ActionDoor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
