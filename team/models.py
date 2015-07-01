#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Invitation(models.Model):
    pass


class Membership(models.Model):
    class Role:
        MEMBER, MANAGER, OWNER = range(3)
        CHOICES = (
            (MEMBER, 'member'),
            (MANAGER, 'manager'),
            (OWNER, 'owner'),
        )

    class Status:
        pass

    team = models.ForeignKey(Team, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.IntegerField(default=Role.MEMBER, choices=Role.CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s of team_%d' % (self.user.username, self.team_id)
