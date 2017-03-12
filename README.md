## TUF-2000M challenge

This is a challenge designed by Gambit. Participants can test their developing skills.

Gambit has access to an ultrasonic energy meter from where [Live data](http://tuftuf.gambitlabs.fi/feed.txt) is available. This data comprises of a datetimestamp and values of first 100 registers. More information on registers are available on pages 39-42 of [docs/tuf-2000m.pdf](https://github.com/gambit-labs/tuf-2000m/blob/master/docs/tuf-2000m.pdf).

Developers are required to chose one of the two options to test their skills:

- Option 1:
Convert data available in Register into human readable data.

- Option 2:
Visualize the data.

I noted that there has not been new data available since 9th March 2017. I have access to limited data, only nine entries were saved in my database. Due to this constrained, I decided to tackle both the options mentioned above.

## Built With

* [Django](https://www.djangoproject.com) - The web framework used.
* [Celery](http://celery.readthedocs.io/en/latest/) - For performing periodic task in background with [Redis](https://redis.io) as message broker.
* [AWS S3](https://aws.amazon.com/s3/) - For storing static files.
* [D3.js](https://d3js.org) - For graphical visualisation of data.
* Python version 2.7 is used for backend programming.

## Deployment

This web application is deployed in [Heroku](http://gambit-challenge.herokuapp.com).

## Requirements

All dependencies can be installed using
```
pip install requirements.txt
```

## Description

The backend of this application is designed to receive data from Modbus every five minutes, convert the register values into human-readable, and stores the register values and human-readable data in a [PostgreSQL](https://www.postgresql.org) database. Multiple entries of same data is prevented by setting the datetimestamp as a unique field.

Clues provided in the challenge were used to design the data conversion methods. Details of backend, including data conversion, can be found [here](option1/dataProcessing.py). Integrating Celery and performing periodic tasks, are described [here](gambitChallenge/celery.py) and [here](option1/tasks.py) respectively.

The [views functions](dataApp/dataProcessing.py) are used for rendering front-end templates, and for sending required data to front-end when AJAX calls are made.

The [front-end](http://gambit-challenge.herokuapp.com) shows real-time information to users. The task described in Option1 is shown in a tabular format, whereas tasks for Option2 is shown in a graphical format. Front-end makes use of periodic AJAX calls to visualise real-time data.


## Data Conversion Testing with Clues Provided

This section validates the methods developed for converting modbus data to human-readable data. In particular, this section describes real4Conversion(), longConversion() and integerConversion() functions implemented in [dataApp/dataProcessing.py](dataApp/dataProcessing.py). In the demonstration, the functions take inputs of the registers described in [the challenge](https://github.com/gambit-labs/tuf-2000m), and checks if the output from these three functions match with the clue provided:
```
To help you on your way with data conversion I will give you a few clues based on the example data above:

Register 21-22, Negative energy accumulator is -56.
Register 33-34, Temperature #1/inlet is 7.101173400878906.
Register 92, Signal Quality is 38.
```

Activating django shell
```
$ python manage.py shell
```

Testing of Real4 datatype conversion to human readable
```
>>> from dataApp.dataProcessing import real4Conversion
>>> reg33 = 15568
>>> reg34 = 16611
>>> real4Conversion(reg33, reg34)
7.101173400878906
```

Testing of Long datatype conversion to human readable
```
>>> from dataApp.dataProcessing import longConversion
>>> reg21 = 65480
>>> reg22 = 65535
>>> longConversion(reg21, reg22)
-56
```

Testing of Integer datatype conversion to human readable
```
>>> from dataApp.dataProcessing import integerConversion
>>> reg92 = 806
>>> key = 92
>>> integerConversion(reg92, key)
[3, 38]
```
Description of Register number 92 states that the lower byte represents Signal Quality. The integerConversion function returns 38 as the lower byte, which is the value of Signal Quality.