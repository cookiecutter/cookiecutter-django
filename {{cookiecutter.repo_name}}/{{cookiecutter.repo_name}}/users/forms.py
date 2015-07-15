# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from .models import User


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just the name field.
        fields = ("name", )
