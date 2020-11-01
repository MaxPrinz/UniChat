# ISD-Project-BullingerPilzPrinz-
Information Systems Developement Project for our studies at the uni li

# Remarks
This project was created using PyCharm

# Installations
1. Install the requirements included in requirements.txt. PyCharm has a own feature to do that
1. In the folder UniChatProject copy settings_local_template.py to settings_local.py and adjust parameters


Type the following commands in the terminal-window of PyCharm to create the database 
(in the UniChatProject folder):
1. python manage.py makemigrations
1. python manage.py migrate

Type the following commands in the terminal-window of PyCharm to create superuser and start server
(in the UniChatProject folder):
1. python manage.py createsuperuser
1. python manage.py runserver

# Usage
* use the /uniChat path in your browser for the application
* use the /admin path in your browser for the django-admin (you must be superuser to use that) 

# Documentation
Please follow [this Link](https://github.com/MaxPrinz/ISD-Project-BullingPilzPrinz/wiki).
