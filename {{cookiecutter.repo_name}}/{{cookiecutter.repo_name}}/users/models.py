# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
# from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField("Name of User", blank=True, max_length=255)

    def __unicode__(self):
        return self.username

    @models.permalink
    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
