# Work at Olist - Call Management App

[![Maintainability](https://api.codeclimate.com/v1/badges/b06a048c737cafabf4c9/maintainability)](https://codeclimate.com/github/andresmachado/work-at-olist/maintainability)

This app implements the logical requested at [Work at Olist challenge](https://github.com/olist/work-at-olist)

## Installing and test instructions

1. Clone this repo to your local machine
2. Run `pip install requirements.txt`
3. After installing all requirements, you should run `make build`
4. Then `make run` and we're good to go

> Obs. The db.sqlite3 file within this repository contains some data that can be tested.

## Running the tests

Just `./manage.py test api` - all tests should pass.

## Heroku app

Alternatively you can access the app on Heroku via https://call-management.herokuapp.com/api/v1/

## API Endpoints

The base URL for access the API is at `http://localhost:8000/api/v1/`

You can access the brief API documentation at `{base_url}/docs/`

## Starting a Call

To start a call, just send a POST to `{base_url}/calls` containing the data below

```
{
    "source":  // Source phone number following the format AAXXXXXXXXX
    "destination": // Destination number following the format AAXXXXXXXXX
    "timestamp": // Optional - The timestamp of when the call started, if not informed, will assume today.now().
}
```

You will receive a response containing the identifier for your call which must be used to end the call.

## Ending a call

To end a call, send a *PUT* request to `{base_url}/calls/{identifier}/end-call/` containing the data below

```
{
    "identifier":  // Identifier of the call
    "timestamp": // The timestamp of when the call has_ended.
}
```

As response, you will receive a json containing the *duration* and the *cost* of this call. If the *timestamp* won't be informed, will assume now();


## Getting a bill report

To get a bill report, send a *GET* request to `{base_url}/bills/` informing the `?phone` and optionally `&period` params, if `&period` won't be informd, will assume the last closed period.

## Environment briefing

### Computer
ASUS Core I5 8Gb Ram

### System
Distributor ID:	Ubuntu
Description:	Ubuntu 16.04.3 LTS
Release:	16.04
Codename:	xenial

### Languages and Frameworks

- Python 3.5.2 (3.6.4 at Heroku)
- Django 1.11
- Django Rest Framework 3.3.1
- Django Rest Swagger

### Libraries

- psycopg2
- gunicorn
- Django Whitenoise
- flake8
- ipdb

### Tools

- VSCode
- iPython
- Git / Github
- Heroku cli
- DBeaver