[![Build Status](https://travis-ci.org/HeliumEdu/platform.svg?branch=master)](https://travis-ci.org/HeliumEdu/platform)
[![codecov](https://codecov.io/gh/HeliumEdu/platform/branch/master/graph/badge.svg)](https://codecov.io/gh/HeliumEdu/platform)


# Helium Platform Project

## Prerequisites

* Python (>= 3.5)
* Pip (>= 9.0)
* MySQL (>= 5.7)
* Redis (>= 3.2)

## Getting Started
The Platform is developed using Python and [Django](https://www.djangoproject.com).

### Project Setup
To setup the Python/Django Platform build environment, execute:

```
make install
```

This project is configured to work with a Virtualenv which has now been setup in the `.venv` folder. If you're
unfamiliar with how this works, [read up on Virtualenv here](https://virtualenv.pypa.io/en/stable). The short version
is, virtualenv creates isolated environments for each project's dependencies. To activate and use this environment when
developing, execute:

```
source .venv/bin/activate
```

All commands below will now be run within the virtualenv (though `make` commands will always automatically enter the
virtualenv before executing).

To ensure the database is in sync with the latest schema, database migrations are generated and run with Django. To
run migrations, execute:

```
make migrate
```

Once migrations have been run, you can create a super user, which is a standard user that also has access to the
/admin site.

```
python manage.py createsuperuser
```

Before commits are made, be sure to run tests and check the generated coverage report.

```
make test
```

## Development
### Modules
The Platform project is split up into several modules, all contained within this repository. They are independent modules that can be deployed
separately, functioning on separate nodes for scalability.

The project's base configuration is defined under `conf`. Application-specific configuration variables should have their application name as their
prefix.

* auth
* common
* feed
* importexport
* planner

### Vagrant Development
To emulate a prod-like environment, use the Vagrant box. It's setup is described more thoroughly in the [deploy](https://github.com/HeliumEdu/deploy#readme)
project. This is the recommended way to develop and test for production as this environment is provisioned in the same way other prod-like
environments are deployed and interacts with related projects as necessary.

As the Vagrant environment does take a bit more time to setup (even though the setup is largely automated) and can consume more developer
and system resources, the local development environment described below is the quickest and easiest way to get up and running.

### Local Development
This is the simplest way to get started with minimal effort. To get going (assuming you have followed the "Getting Started"
directions above), you should have the `ENVIRONMENT` environment variable set to "dev".

Now you're all set! To start the development server, execute:

```
bin/runserver
```

A development server will be started at http://localhost:8000.

Note that credentials to third-party services (for example, AWS services like SES) need to be set in the `.env` file
before those services will work properly. Do NOT commit real credentials to third-party services, even in example files.

### Frontend
The frontend is served from a separate repository and can be found [here](https://github.com/HeliumEdu/frontend#readme).

Note that the frontend was previously bundled, rendered, and served as a part of this project, but it was pulled out
into its own project with the with `1.4.0` release. For reference, checkout the `1.3.8` tag or download it [here](https://github.com/HeliumEdu/platform/releases/tag/1.3.8)
to see how this was previously done. 

### Documentation

Auto-generated API documentation is accessible via any environment at /docs. Additional documentation can be found
on the [Platform Wiki](https://github.com/HeliumEdu/platform/wiki).
