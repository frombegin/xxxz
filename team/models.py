#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

import os
import uuid

from . import signals


TEAM_AVATAR_PATH = "avatars"
TEAM_URL_DETAIL_NAME = "team:detail"


def avatar_upload(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = "%s%s" % (uuid.uuid4().hex, ext)
    return os.path.join(TEAM_AVATAR_PATH, filename)


class TeamManager(models.Manager):
    ''


class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    private = models.BooleanField(default=False)

    objects = TeamManager

    def get_absolute_url(self):
        return reverse(TEAM_URL_DETAIL_NAME, args=[self.pk])

    def open_for_joining(self):
        return not self.private

    def can_join(self, user):
        pass

    def can_leave(self, user):
        pass

    def can_apply(self, user):
        pass

    def is_member(self, user):
        return self.members.filter(user=user).exists()

    def is_manager(self, user):
        pass

    def is_owner(self, user):
        pass

    def is_owner_or_manager(self, user):
        pass

    def is_on_team(self, user):
        pass

    def add_user(self, user, role):
        status = Membership.Status.INVITED if self.private else Membership.Status.AUTO_JOINED
        member, _ = self.members.get_or_create(
            user=user,
            defaults={"role": role, "status": status}
        )
        signals.member_added.send(sender=self, membership=member)
        return member

    def get_membership_for_user(self, user):
        try:
            return self.memberships.get(user=user)
        except Membership.DoesNotExist:
            return None

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
        APPLIED, INVITED, DECLINED, REJECTED, ACCEPTED, AUTO_JOINED = range(6)
        CHOICES = (
            (APPLIED, 'appled'),
            (INVITED, 'invited'),
            (DECLINED, 'declined'),
            (REJECTED, 'rejected'),
            (ACCEPTED, 'accepted'),
            (AUTO_JOINED, 'auto_joined'),
        )

    team = models.ForeignKey(Team, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.IntegerField(default=Role.MEMBER, choices=Role.CHOICES)
    status = models.IntegerField(default=Status.APPLIED, choices=Status.CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s of team_%d' % (self.user.username, self.team_id)
