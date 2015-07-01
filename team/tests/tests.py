#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from team.models import Team, Membership


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@email.com', '123456')
        self.team = Team.objects.create(creator=self.user, name=u'a test team', description=u'desc of the team')

    def tearDown(self):
        self.user.delete()
        self.team.delete()


class ModelTestCase(BaseTestCase):
    def test_membership_create(self):
        member = Membership.objects.create(team=self.team, user=self.user)
        self.assertEquals(self.team.members.count(), 1)
        self.assertEquals(member.role, Membership.Role.MEMBER)

        member = Membership.objects.create(team=self.team, user=self.user, role=Membership.Role.MANAGER)
        self.assertEquals(self.team.members.count(), 2)
        self.assertEquals(member.role, Membership.Role.MANAGER)

        member.delete()
        self.assertEquals(self.team.members.count(), 1)
