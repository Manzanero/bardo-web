from django.urls import path

from . import views

urlpatterns = [
    path('<str:campaign_name>/<str:map_name>/save', views.save_map, name='save_map'),
    path('<str:campaign_name>/<str:map_name>/load', views.load_map, name='load_map'),
    path('<str:campaign_name>/<str:map_name>/delete', views.delete_map, name='delete_map'),
    path('<str:campaign_name>/<str:map_name>/actions/add', views.add_actions, name='add_action'),
    path('<str:campaign_name>/<str:map_name>/actions/reset', views.reset_actions, name='reset_actions'),
    path('<str:campaign_name>/<str:map_name>/actions/from/beginning', views.all_actions, name='all_actions'),
    path('<str:campaign_name>/<str:map_name>/actions/from/<str:datetime_iso>', views.load_actions, name='load_actions'),
]