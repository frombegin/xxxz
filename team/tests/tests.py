#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from team.models import Team, Invitation, Membership, avatar_upload


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@email.com', '123456')
        self.u1 = User.objects.create_user('u1', 'u1@email.com', '123456')
        self.u2 = User.objects.create_user('u2', 'u2@email.com', '123456')
        self.u3 = User.objects.create_user('u3', 'u3@email.com', '123456')
        self.team = Team.objects.create(creator=self.user, name=u'a test team', description=u'desc of the team')

    def tearDown(self):
        self.user.delete()
        self.team.delete()


class TeamTestCase(BaseTestCase):
    def test_joinable(self):
        team = Team.objects.create(creator=self.user, name=u'NON-piravte team')
        self.assertFalse(team.private)
        self.assertTrue(team.open_for_joining())

    def test_add_member(self):
        member = self.team.add_user(self.u1, Membership.Role.MEMBER)
        self.assertEquals(member.role, Membership.Role.MEMBER)
        self.assertEquals(member.status, Membership.Status.AUTO_JOINED)

        self.team.add_user(self.u2, Membership.Role.MEMBER)
        self.team.add_user(self.u3, Membership.Role.MANAGER)


class MembershipTestCase(BaseTestCase):
    def test_avatar_uploadto(self):
        path = avatar_upload(self.team, "hello world.jpg")
        self.assertTrue(path.startswith("avatars"))
        self.assertTrue(path.endswith(".jpg"))

    def test_membership_create(self):
        member = Membership.objects.create(team=self.team, user=self.user)
        self.assertEquals(self.team.members.count(), 1)
        self.assertEquals(member.role, Membership.Role.MEMBER)

        member = Membership.objects.create(team=self.team, user=self.user, role=Membership.Role.MANAGER)
        self.assertEquals(self.team.members.count(), 2)
        self.assertEquals(member.role, Membership.Role.MANAGER)

        member.delete()
        self.assertEquals(self.team.members.count(), 1)

    def test_membership_status(self):
        member = Membership.objects.create(team=self.team, user=self.user)
