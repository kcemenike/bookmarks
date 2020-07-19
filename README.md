# An image bookmarking site #BuiltWithDjango
This site allows users to bookmark images from any website on their personal profile.  
This is for educational purposes only! Don't run this as is in a production environment!!!  

## Features
- Create a bookmarklet on your favourite browser to bookmark your favourite images in your profile
- Sign up / sign in with your social media account (Facebook/Twitter/GooglePlus)
- Follow other users to see their activity
- A personalised activity stream to view follower activities
- A ranking of top images globally

[![An image bookmarking site with django](video_image.jpg)](https://youtu.be/aiHBDRMYXoE "An image bookmarking site with django")

## Language/frameworks
- HTML5
- CSS3
- JavaScript / JQuery
- Python (Django)
- SQLite3
- Redis

## Dependencies
### Django 2.2.12
Django 3.x removes six support and six is a dependency for some of the below dependencies
### django-extensions
Allows us to run the development server in https as
`python manage.py runserver_plus --cert-file cert.cert`
### easy-thumbnails
For allowing the display of smart thumbnails per image
### python-social-auth
For social login integration (Facebook, Twitter, Google+)
### redis
For fast caching

## Installation
- Install dependencies using conda (or pip). You can check the conda-forge channel if the dependency is not found in the default channel
- Configure your site name in `ALLOWED_HOSTS` of `settings.py`
- Initialise a redis server and change the values below in `settings.py` as desired
```
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
```
- To enable social media integration, change the following string variables in `settings.py`
```
SOCIAL_AUTH_FACEBOOK_KEY = 
SOCIAL_AUTH_FACEBOOK_SECRET =

SOCIAL_AUTH_TWITTER_KEY = 
SOCIAL_AUTH_TWITTER_SECRET = 

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 
```

## Deployment
- Run the server with either `python manage.py runserver` or
`python manage.py runserver_plus --cert-file cert.cert` if you want https support
- View site at https://mysite.com:8000/account
