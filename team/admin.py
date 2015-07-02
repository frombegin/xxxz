#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.contrib import admin
## from .models import YourModel


##def your_admin_action(modeladmin, request, queryset):
##	# queryset.update(promoted=True)
##    pass
##your_admin_action.short_description = _('Your action description.')
##
##class YourModelAdmin(admin.ModelAdmin):
##    list_display = ('actions_column', 'type_image', )
##    actions = [your_admin_action,]
##
### Register your models here.
##admin.site.register(YourModel, YourModelAdmin)


from django.contrib import admin
from .models import Team, Membership


def members_count(obj):
    return obj.members.count()


members_count.short_description = "Members Count"


class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", members_count, "creator",)
    fields = (
        'name',
        'description',
        'avatar',
        'creator',
        'private',
    )
    raw_id_fields = ("creator",)


class MembershipAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    list_display = ["team", "user", "status", "role"]
    list_filter = ["team"]
    search_fields = ["user__username"]


admin.site.register(Team, TeamAdmin)
admin.site.register(Membership, MembershipAdmin)
