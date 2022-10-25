# ERP project with Django Framework and Vue

[![Frontend CI](https://github.com/INGSOFT-I-PBC/ERPt/actions/workflows/frontend-check.yml/badge.svg)](https://github.com/INGSOFT-I-PBC/ERPt/actions/workflows/frontend-check.yml)
![Deployment](https://github.com/INGSOFT-I-PBC/AdminSite/actions/workflows/deploy.yml/badge.svg)

This repository contains the configuration
for an ERP with the Django Framework and the implementation
for an API REST implementation

## Installing dependencies

To install the dependencies that will be used on developement environment
you must run the next command:

#### GNU/Linux / MacOS

```
$ python -m pip install -r dev_requirements.txt
```

Or

```
$ pip3 install -r dev_requirements.txt
```

#### Windows

```
> py -m pip install -r dev_requirements
```

Or

```
> pip install -r dev_requirements
```

## Django Backend

### General Configuration

Before using the system we need to create the `.env` file where
the configurations will be setting up, to create a `.env` copy the file
`.env.example` and remove the `.example` extension.

### Database

After that we need the creation of the database that will hold all the information,
to create this database we need to run:

```
> python manage.py migrate
```

This command will create all the base structure of the database, included the base data needed to manage the roles, permission and users.

### User creation

To start using the backend we need an admin user, to create a new
superuser run the next command:

```
> python manage.py createuser --admin
```

To create a normal/manual user run without `--admin` switch. Like:

```
> python manage.py createuser
```

Also, you can provide the username without the need to write on the
terminal form:

```
> python manage.py createuser [--admin] --username <Username>
```

If the creation of the user was sucessfully the next message will be
shown:

```
> python manage.py createuser --username 'Super admin'
...
Successfully created the user 'super_admin'
```

### Run server

To run the Django's server we start the server with the following options

```
> python manage.py runserver [<ip/hostname>:<port>]
```

## Frontend

### Requirements

To starting working on the frontend we need the following tools:

- [Node.JS](https://nodejs.org/es/)
- [PNPM](https://pnpm.io/installation)

NOTE: We use Composition API as a recommended way to make Vue.js components.
### Dependencies and useful commands

To start the project we'll need to install the dependencies with the following commands:
```{sh}
cd frontend/
pnpm install
```

After that all the dependencies must be installed. To run the development server, you must run the command:
```
$ pnpm dev
```

For fix the files with the linter:
```
$ pnpm lint
```

### Useful Links

The frontend use [Vite.JS](https://vitejs.dev/guide/) as a frontend tooling and [Vue 3](https://vuejs.org/).

Most of the required knowledge can be readed from the documentation of Vue:

- [Introduction to Vue](https://vuejs.org/guide/introduction.html): Introduction to Vue
- [Essentials](https://vuejs.org/guide/essentials/template-syntax.html): Essentials about vue syntax
- [Components](https://vuejs.org/guide/components/registration.html): Components essentials
- [Vitest](https://vitest.dev/guide/): for Unit Testing
- [Vue Router:](https://router.vuejs.org/api/#to) for route management
