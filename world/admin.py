from django.contrib import admin

from world.models import Campaign, Map, Action, CampaignProperty


class CampaignPropInline(admin.StackedInline):
    model = CampaignProperty
    extra = 1


class ActionInline(admin.StackedInline):
    model = Action
    extra = 1


class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignPropInline, ActionInline]


admin.site.register(Campaign, CampaignAdmin)


class MapAdmin(admin.ModelAdmin):
    inlines = [ActionInline]


admin.site.register(Map, MapAdmin)


class ActionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Action, ActionAdmin)
