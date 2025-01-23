import logging

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from django.views.decorators.cache import never_cache
from django import forms
#from registration.models import RegistrationProfile
from django_registration.backends.activation.views import ActivationView
from django_registration.exceptions import ActivationError
from accounts.models import UserProfile

from edumanage.forms import UserProfileForm
from edumanage.models import Institution

logger = logging.getLogger('debugging')


@never_cache
def activate(request, activation_key):
    account = None
    if request.method == "GET":
        # Normalize before trying anything with it.
        activation_view = ActivationView()
        logger.warning(f"GET: activation_key {activation_key} activation_view {activation_view}")
        try:
            #rp = RegistrationProfile.objects.get(activation_key=activation_key)
            username = activation_view.validate_key(activation_key=activation_key)
            logger.warning(f"GET: username {username} has validated using key {activation_key}")
        except ActivationError:
            logger.warning(f"GET: An error has occurred. Redirecting to activate page")
            return render(
                request,
                'registration/activate.html',
                {
                    'account': account,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
                }
            )
        try:
            #user_profile = rp.user.userprofile
            user_profile = activation_view.get_user(username)
            logger.warning(f"GET: username = {username} user_profile = {user_profile}")
        except ActivationError:
            logger.warning(f"GET: ActivationError")
            return render(
                request,
                'registration/activate.html',
                {
                    'account': account,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
                }
            )
        form = UserProfileForm(instance=user_profile)
        form.fields['user'] = forms.ModelChoiceField(
            queryset=User.objects.filter(pk=user_profile.pk), empty_label=None
        )
        form.fields['institution'] = forms.ModelChoiceField(
            queryset=Institution.objects.all(), empty_label=None
        )
        logger.warning(f"GET: Loading activate_edit.html")
        return render(
            request,
            'registration/activate_edit.html',
            {
                'account': account,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'form': form
            }
        )
    if request.method == "POST":
        request_data = request.POST.copy()
        activation_view = ActivationView()
        try:
            user = User.objects.get(pk=request_data['user'])
            up = user.userprofile
            up.institution = Institution.objects.get(
                pk=request_data['institution']
            )
            logger.warning(f"POST: Saved user {user} up {up} institution {up.institution}")
            up.save()

        except Exception as e:
            logger.warning(f"POST: Exception occurred: {e}")
            return render(
                request,
                'registration/activate_edit.html',
                {
                    'account': account,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
                }
            )
        # Normalize before trying anything with it.
        logger.warning(f"POST: Activation key: {activation_key}")
        try:
            #rp = RegistrationProfile.objects.get(activation_key=activation_key)
            username = activation_view.validate_key(activation_key=activation_key)
            logger.warning(f'POST: Activating username {username} with activation key {activation_key}')
            account = activation_view.get_user(username)
            logger.warning(f'POST: Activating account {account}')
            up.user.is_active = True
            up.is_social_active = True
            up.save()
        except Exception as e:
            logger.info('POST: An error occured: %s' % e)
            pass

        if account:
            # A user has been activated
            email = render_to_string(
                'registration/activation_complete.txt',
                {
                    'site': get_current_site(request),
                    'user': account
                }
            )
            send_mail(
                _('%sUser account activated') % settings.EMAIL_SUBJECT_PREFIX,
                email,
                settings.SERVER_EMAIL,
                account.email.split(';')
            )
        else:
            logger.warning(f"POST: Account {account} is falsey, refusing to send email.")

        return render(
            request,
            'registration/activate.html',
            {
                'account': account,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
            }
        )
