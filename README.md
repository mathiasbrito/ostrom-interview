# OSTROM Interview Challenge

- [Running the System](#running)
  * [Run with Docker](#run-with-docker)
  * [Deploy on Heroku](#deploy-on-heroku)
- [Experiment the API](#experiment-the-api)
- [Implementation Architecture](#implementation-architecture)
- [Technical Decisions](#technical-decisions)
  * [Why Python and FastAPI](#why-python-and-fastapi)
  * [Why pytest](#why-pytest)
- [Frameworks](#frameworks)
  * [For the Application](#for-the-application)
  * [For testing](#for-testing)

## Running

To run the application install it with:

```
$ pip install .
```

After the installation run with:

```
$ ostrom
```

### Run with Docker

- Build the image with `docker build -t ostrom .`
- Run with `docker run -p 8001:8001 ostrom`. Adjust port if necessary.

### Deploy on Heroku

- Install the Heroku CLI. [Instructions Here](https://devcenter.heroku.com/articles/heroku-cli)
- Authenticate with `heroku login`
- Push the code
  - ```
    $ git add .
    $ git commit -am "Ostrom at Heroky"
    $ git push heroku trunk:master
    ```

## Experiment the API

To use and experiment the API you can use the FastAPI `/docs` endpoint, in your browser
go to `127.0.0.1/docs`. There you can experiment the system by sending HTTP requests to
the server. The schemas and all the necessary information to use the routes are available
in details.

## Implementation Architecture

The solution is based on three pillars, the routers that exposes the API, the services that supports
the routers and the domain models. The logic resides on the services, while the classes in the domain
module represents objects from the application domain. No data models are used, since it was not required
by the problem description.
    
### Technical Decisions

#### Why Python and FastAPI

Python and FastAPI was choose due to the constrained time to develop the application.
Python and FastAPI allows advancing faster, while providing API documentation in the
`/docs` route. Python also helps keeping the code clean and easy to read. Despite not
being the most performant solution, both can deliver satisfactory performance. The
choice was also impacted by the level of knowledge from the author.
 
#### Why pytest

Pytest helps with structuring the tests in a comprehensive and clean way. Parametrized
arguments and fixtures in pytest helps to inject dependencies and mock objects if necessary.
Pytest compared to other solutions in pythons the python `assert` statement making tests
easier to read.


### Frameworks

#### For the Application

- FastAPI
- Pydantic

#### For testing

- Tox
- pytest

