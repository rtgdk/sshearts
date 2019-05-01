from django.shortcuts import render
from app.models import AppFbUser
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
import base64, hmac, hashlib
import json
import os
from social_django.models import UserSocialAuth


def index(request):
    context_dict = {}
    if request.user.is_active:
        app_user = AppFbUser.objects.get(user=request.user)
        context_dict["app_user"] = app_user
    return render(request, 'index.html', context_dict)


def user_login(request):
    if request.user.is_active:
        return HttpResponseRedirect('/app/')
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/app/')


def user_deauthorize(request):
    if request.method == 'POST':
        print("here")
        try:
            deauth_request = request.POST['signed_request']
            encoded_signature, payload = deauth_request.split('.')
            payload_decoded = base64.urlsafe_b64decode(payload + "==").decode('utf-8')
            payload_decoded = json.loads(payload_decoded)
            if 'user_id' not in payload_decoded.keys():
                return HttpResponse(status=400, content='Invalid payload data')
            else:
                user_id = payload_decoded['user_id']
                secret = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')
                signature = base64.urlsafe_b64decode(encoded_signature + "==")
                expected_sig = hmac.new(bytes(secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256)
                if not hmac.compare_digest(expected_sig.digest(), signature):
                    return HttpResponse(status=400, content='Invalid request')
        except (ValueError, KeyError, TypeError, AttributeError):
            return HttpResponse(status=400, content='Invalid request')
        except json.JSONDecodeError:
            return HttpResponse(status=400, content='Could not decode payload')
        except:
            return HttpResponse(status=400, content='Could not decode the signed request')

        try:
            social_account = UserSocialAuth.objects.get_social_auth('facebook',uid=user_id)
            social_user = social_account.user
            social_user.is_active = False
            social_user.save()
            return HttpResponse(status=200)
        except UserSocialAuth.DoesNotExist:
            return HttpResponse(status=200) # since if we cannot find the user with that uid,
            # it might be that our database has already deleted that user, so sending 200 status
