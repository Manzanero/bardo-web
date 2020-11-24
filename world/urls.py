from django.urls import path

from . import views

urlpatterns = [
    path('campaign/<str:campaign_name>', views.load_campaign, name='load_campaign'),
    # path('campaign/<str:campaign_name>/property/<str:property_name>', views.load_property, name='load_property'),
    # path('campaign/<str:campaign_name>/property/<str:property_name>/save', views.save_property, name='save_property'),
    # path('campaign/<str:campaign_name>/property/<str:property_name>/delete', views.delete_property, name='delete_property'),
    path('campaign/<str:campaign_name>/map/<str:map_name>', views.load_map, name='load_map'),
    path('campaign/<str:campaign_name>/map/<str:map_name>/save', views.save_map, name='save_map'),
    path('campaign/<str:campaign_name>/map/<str:map_name>/delete', views.delete_map, name='delete_map'),
    path('campaign/<str:campaign_name>/actions/add', views.add_actions, name='add_action'),
    path('campaign/<str:campaign_name>/actions/reset', views.reset_actions, name='reset_actions'),
    path('campaign/<str:campaign_name>/actions/from/map/<str:map_name>', views.all_actions, name='all_actions'),
    path('campaign/<str:campaign_name>/actions/from/date/<str:datetime_iso>', views.load_actions, name='load_actions'),
]