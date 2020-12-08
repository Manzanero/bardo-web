from django.contrib import admin

from world.models import Campaign, Map, Action, CampaignProperty, MapProperty


class CampaignPropInline(admin.StackedInline):
    model = CampaignProperty
    extra = 1


# class ActionInline(admin.StackedInline):
#     model = Action
#     extra = 1


class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignPropInline]
    list_display = ('name', 'campaign_id')


admin.site.register(Campaign, CampaignAdmin)


class MapPropInline(admin.StackedInline):
    model = MapProperty
    extra = 1


class MapAdmin(admin.ModelAdmin):
    inlines = [MapPropInline]
    # inlines = [MapPropInline, ActionInline]
    list_display = ('name', 'map_id', 'campaign_name', 'campaign_id')

    @staticmethod
    def campaign_name(obj):
        return obj.campaign.name

    @staticmethod
    def campaign_id(obj):
        return obj.campaign.campaign_id


admin.site.register(Map, MapAdmin)


class ActionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Action, ActionAdmin)
