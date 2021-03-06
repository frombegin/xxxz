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
    def create_team(self, user, **kwargs):
        kwargs['creator'] = user
        team = self.create(**kwargs)
        team.add_member(user, Member.Role.OWNER)  # add owner as membership
        return team


class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    private = models.BooleanField(default=False)

    objects = TeamManager()

    def get_absolute_url(self):
        return reverse(TEAM_URL_DETAIL_NAME, args=[self.pk])

    def can_join(self, user):
        pass

    def can_leave(self, user):
        pass

    def can_apply(self, user):
        pass

    def is_member(self, user):
        return self.members.filter(user=user).exists()

    def is_manager(self, user):
        member = self.get_member_by_user(user)
        return member.role == Member.Role.MANAGER if member else False

    def is_owner(self, user):
        member = self.get_member_by_user(user)
        return member.role == Member.Role.OWNER if member else False

    def is_owner_or_manager(self, user):
        member = self.get_member_by_user(user)
        return member.role in (Member.Role.OWNER, Member.Role.MANAGER,) if member else False

    def is_on_team(self, user):
        pass

    def add_member(self, user, role):
        status = Member.Status.INVITED if self.private else Member.Status.AUTO_JOINED
        member, _ = self.members.get_or_create(
            user=user,
            defaults={"role": role, "status": status}
        )
        signals.member_added.send(sender=self, membership=member)
        return member

    def add_activity(self, user, text, uri=u''):
        return Activity.objects.create(team=self, creator=user, text=text, uri=uri)

    def get_member_by_user(self, user):
        try:
            return self.members.get(user=user)
        except Member.DoesNotExist:
            return None

    def __unicode__(self):
        return self.name


class TeamItem(models.Model):
    class Meta:
        abstract = True


class Activity(models.Model):
    team = models.ForeignKey(Team, related_name='activities')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    text = models.CharField(max_length=128, )
    uri = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.text, self.uri)


class Invitation(models.Model):
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inviter')
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invitee')
    text = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team)

    class Meta:
        unique_together = ('inviter', 'invitee', 'team',)


class Member(models.Model):
    class Role:
        MEMBER, MANAGER, OWNER = range(3)
        CHOICES = (
            (MEMBER, 'member'),
            (MANAGER, 'manager'),
            (OWNER, 'owner'),
        )

    class Status:
        APPLIED, INVITED, REJECTED, ACCEPTED, AUTO_JOINED = range(5)
        CHOICES = (
            (APPLIED, 'appled'),
            (INVITED, 'invited'),
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
