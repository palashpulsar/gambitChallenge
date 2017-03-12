## TUF-2000M challenge

This is a challenge designed by Gambit. Participants can test their skills as Full-stack Developers.

Gambit has access to an ultrasonic energy meter from where [Live data](http://tuftuf.gambitlabs.fi/feed.txt) is available. This data comprises of a datetimestamp and values of first 100 registers. More information on registers are available on pages 39-42 of [docs/tuf-2000m.pdf](https://github.com/gambit-labs/tuf-2000m/blob/master/docs/tuf-2000m.pdf).

Developers are required to chose one of the two options to test their skills:

- Option 1:
Convert data available in Register into human readable data.

- Option 2:
Visualize the data.

I noted that there has not been any new data available since 9th March 2017. I have access only to limited data, only nine entries were stored in database. Due to this constrained, I decided to tackle the two options mentioned above.

## Built With

* [Django](https://www.djangoproject.com) - The web framework used.
* [Celery](http://celery.readthedocs.io/en/latest/) - For performing periodic task in background with [Redis](https://redis.io) as message broker.
* [AWS S3](https://aws.amazon.com/s3/) - For storing static files.
* [D3.js](https://d3js.org) - For graphical visualisation of data.
* Python version 2.7 is used for backend programming.

## Deployment

This web application is deployed in [heroku](http://gambit-challenge.herokuapp.com).

## Requirements

All dependencies can be installed using
```
pip install requirements.txt
```

## Description

The backend of this application is designed to receive data from Modbus every five minutes, convert the register values into human-readable, and stores the register values and human-readable data in a [PostgreSQL](https://www.postgresql.org) database. Multiple entries of same data is prevented by setting the datetimestamp as a unique field.

Clues provided in the challenge were used to design the data conversion methods. Details of backend, including data conversion, can be found [here](dataApp/dataProcessing.py). Integration of Celery into this application, and performing periodic tasks, are described [here](gambitChallenge/celery.py) and [here](dataApp/tasks.py) respectively.

The [views](dataApp/views.py) functions are used for rendering front-end templates, and for sending required data to front-end when AJAX calls are made.

The [front-end](http://gambit-challenge.herokuapp.com) shows real-time information to users. The task described in Option 1 is shown in a tabular format, whereas tasks for Option 2 is shown in a graphical format. Front-end makes use of periodic AJAX calls to visualise information real-time.


## Code Example WRITE IT ASAP

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.
