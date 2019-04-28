# Facebook Authorising App for Social Sweethearts

## Explanation of Features

1. Used social-auth-app-django to implement facebook login. This module is helpful to extend the login to github, google and other oauth providers.
3. The access token provided by social-auth-app-django is long lived and is stored in the `User social auths` table under `extras` field
4. When user connects the facebook account, the pipeline function - `load_user_and_profile_pic` (app/pipeline.py) - to save the name, profile picture and profile url in AppFbUser table.
5. When user disconnects the app, the pipeline function - `disconnect_user` (app/pipeline.py) - makes user.is_active=false in the database and the user is logged out.


## Installation Instructions
1. Clone or download the repository. 
2. Create a new virtual environment for the project.
    ```bash
    virtualenv -p python3 venv
    source venv/bin/activate
    ```
3. Go into the repo and install required python libraries giving in the requirements.txt file.
    ```bash
    cd sshearts
    pip install -r requirements.txt
    ```
4. Run Django migrate.
    
    ```bash
    python manage.py migrate
    ```
    
5. Fill in the `SOCIAL_AUTH_FACEBOOK_KEY`  and `SOCIAL_AUTH_FACEBOOK_SECRET` environment variable in your machine.
    ```bash
    export SOCIAL_AUTH_FACEBOOK_KEY=<your-fb-app-id>
    export SOCIAL_AUTH_FACEBOOK_SECRET=<<your-fb-app-secret-key>
    ```
5. Start the application.
    ```bash
    python manage.py runserver
    ```

##Notes

1. I didn't know whether the profile picture should be saved in the database and should be picked up from facebook graph api. So I implemented both the scenario. After logging in, you would see 2 profile images - the left one is from graph api and the right one is from saved media picture.

2. Run with DEBUG=False in production, to redirect AuthCanceled error (when user cancels the facebook app request) to the home page.

3. I could have used class based view to make it more easily extendable and reusable but the amount of http request to be implemented is too less so I used function based view.

