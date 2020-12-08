from django.urls import path

from . import views

urlpatterns = [
    path('', views.load_world, name='load_world'),
    path('campaign/<str:campaign_id>', views.load_campaign, name='load_campaign'),
    path('campaign/<str:campaign_id>/property/<str:property_name>', views.load_campaign_property, name='load_property'),
    path('campaign/<str:campaign_id>/property/<str:property_name>/save', views.save_campaign_property, name='save_property'),
    path('campaign/<str:campaign_id>/property/<str:property_name>/default', views.default_campaign_property, name='default_property'),
    path('campaign/<str:campaign_id>/property/<str:property_name>/delete', views.delete_campaign_property, name='delete_property'),
    path('campaign/<str:campaign_id>/map/<str:map_id>', views.load_map, name='load_map'),
    path('campaign/<str:campaign_id>/map/<str:map_id>/properties', views.load_map_properties, name='load_map_properties'),
    path('campaign/<str:campaign_id>/map/<str:map_id>/save', views.save_map, name='save_map'),
    path('campaign/<str:campaign_id>/map/<str:map_id>/delete', views.delete_map, name='delete_map'),
    # path('campaign/<str:campaign_id>/actions/add', views.add_actions, name='add_action'),
    path('campaign/<str:campaign_id>/actions/reset', views.reset_actions, name='reset_actions'),
    path('campaign/<str:campaign_id>/actions/from/map/<str:map_id>', views.map_actions, name='map_actions'),
    path('campaign/<str:campaign_id>/actions/from/date/<str:datetime_iso>', views.update_actions, name='update_actions'),
]