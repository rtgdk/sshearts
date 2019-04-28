import urllib
from io import BytesIO

from app.models import AppFbUser
from django.core.files import File

"""
This function loads the data from facebook(name and profile picture) and saves it in AppFbUser model table 
and link it with the default Django Users table
Parameters:- 
strategy : The current strategy instance.
backend : The current backend instance. (facebook, google, github, etc.)
details : Basic user details generated by the backend, used to create/update the user model details 
        (this dict will contain values like username, email, first_name, last_name and fullname)
response : The server user-details response (more specifically facebook auth response)
user : The user instance (or None if it wasn’t created or retrieved from the database yet).
"""


def load_user_and_profile_pic(backend, strategy, details, response,
                              user=None, *args, **kwargs):
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/{0}/picture?type=large".format(response['id'])
        user.is_active = True
        user.save()
        httpresponse = urllib.request.urlopen(url)
        io = BytesIO(httpresponse.read())
        app_user = AppFbUser.objects.get_or_create(user=user)
        # get_or_create returns a tuple consisting of object and a boolean variable created
        # (created= True when new AppFbUser created, created =False when already present)
        if app_user[1] is True:
            app_user[0].name = response['name']
            app_user[0].profile_url = url
            app_user[0].profile_pic.save('profile_pic_{}.jpg'.format(user.pk), File(io))
            app_user[0].save()


"""
Disconnect user from the website and set user.is_active=False in the database.
"""


def disconnect_user(strategy, entries, *args, **kwargs):
    user = kwargs.get('user')
    user.is_active = False
    user.save()