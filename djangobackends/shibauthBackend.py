# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

from django.contrib.auth.models import UserManager, Permission, Group
from accounts.models import User
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

class shibauthBackend:
    def authenticate(self, **kwargs):
        username = kwargs.get('username')
        firstname = kwargs.get('firstname')
        lastname = kwargs.get('lastname')
        mail = kwargs.get('mail')
        authsource = kwargs.get('authsource')
        if authsource != 'shibboleth':
            logger.info(f"Invalid auth source {authsource}")
            return None

        try:
            user = self._auth_user(username, firstname, lastname, mail)
        except Exception as e:
            logger.info("Exception occurred when authenticating user: {e}")
            return None

        if not user:
            logger.info(f"Could not authenticate username {username} firstname {firstname} lastname {lastname} mail {mail}")
            return None

        logger.info(f"Authenticated username {username} firstname {firstname} lastname {lastname} mail {mail}")
        return user

    def _auth_user(self, username, firstname, lastname, mail):
        try:
            user = User.objects.get(username__exact=username)
        # The user did not exist. Create one with no privileges
        except:
            logger.info(f"Could not find user {username} with mail {mail}")
            user = User.objects.create_user(username, mail, None)
            user.first_name = firstname
            user.last_name = lastname
            user.is_staff = False
            user.is_superuser = False
            user.is_active = False
            user.save()

        logger.info(f"Returning user {user}")
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
