# tryDjango

cd ~/workspace/queryUnderstanding/demo
mkdir django-venv
enable python3:      vi ~/.bash_profile; add alias python3='/export/apps/python/3.6/bin/python3.6?; source ~/.bash_profile
create envi:              python3 -m venv ./django-venv/

?-activate the environment:
$ cd django-venv/
$ source bin/activate

??install related libs:
$ pip install django
$ pip install plotly
$ pip list --local

? tutorial on Django
https://docs.djangoproject.com/en/2.0/intro/tutorial01/

?start the server
$ python manage.py runserver


?-create database for app
define the classes derived from models.Model. 
add the corresponding app config	in INSTALLED_APPS of the mysite/settings.py
create the databases:  python manage.py makemigrations polls
apply the databases:    python manage.py migrate


?- play with the database API within the python shell
$ python manage.py shell
from polls.models import Question, Choice
Question.objects.all()

