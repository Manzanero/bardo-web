from django.contrib import admin

from world.models import Campaign, Map, Action


class CampaignAdmin(admin.ModelAdmin):
    pass


admin.site.register(Campaign, CampaignAdmin)


class ActionInline(admin.StackedInline):
    model = Action
    extra = 1


class MapAdmin(admin.ModelAdmin):
    inlines = [ActionInline]


admin.site.register(Map, MapAdmin)


class ActionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Action, ActionAdmin)
