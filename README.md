# DRF Simple Referral API

A Django app that provides a RESTful API interface simple referral program with registration 
and authentication using phone number.
It also generates referral code for each user, and it can be entered in special field by another users.

## Basic Features

- Allows users to register using phone number.
- Phone number verification by sms-code.
- Can set expiration time and length on generated tokens for phone verification.
- Generate referral code for each user.
- Referral code can be entered by any user.
- User can enter referral code just once.
- Detail view of any user profile with list of users which entered referral code.

## Quick Start

Clone this repository to your local machine and rename the `.env.example` file found in the root directory of the project to folder `.envs/local/.django`, `.envs/local/.postgres` and update the environment variables accordingly. Then you can start the project using Docker or manually using virtual environment.

Using Docker:

```
$ docker compose -f local.yml up
$ docker-compose -f local.yml exec web python manage.py migrate 
$ docker-compose -f local.yml exec web python manage.py createsuperuser
```

or, manually:

1. Create a Python virtual environment and activate it.
2. Open up your terminal and run the following command to install the packages used in this project.

```
$ pip install -r local/requirements.txt
```

3. Set up a Postgres database for the project.
4. Run the following commands to setup the database tables and create a superuser.

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

5. Run the development server using:

```
$ python manage.py runserver
```

6. Open a browser and go to http://localhost:8000/admin

