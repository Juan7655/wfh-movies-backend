# Welcome to HeyMovie POC!

The objective of the POC is to enable the service to be able to support 1000 user requests per second in the endpoint used to create ratings.

![Diagram](https://i.postimg.cc/Qxv2LzTg/base-de-datos-2.png)

  To achieve this goal a load balancer was proposed to redirect the requests based in the endpoint that is going to be consumed. 
  For POC effects, the load balancer is simulated by manually redirecting the requests to different servers.
 
If the endpoint is the create rating endpoint, the request is redirected to the google cloud pub/sub subscriber service, then is queued and finally is sent to the backend in an ordered way according to its availability.

 # Setup and Execution
The first step to set up the backend and the subscriber is to clone the repository and move to the respective branch for each one.
 
## Backend Branch

The POC backend codebase can be found in the  repository branch **POC-dev**.


## Subscriber Branch

The POC Subscriber Script can be found in the repository branch **POC-subscriber**.

## Backend Setup

This service is deployed in Heroku, so no further configurations are required to 
this service to work. It may be accessed through the following address: https://hey-movie-2.herokuapp.com/rating 

## Subscriber Setup 

To process the queued messages at least one instance of the subscriber should be in execution, the subscriber is a python script that requires two environment variables: 

 1. **DATABASE_URL**
 2. **GOOGLE_APPLICATION_CREDENTIALS**
 3. **SQLALCHEMY_DATABASE_URI**

GOOGLE_APPLICATION_CREDENTIALS requires the route to the JSON file that contains the google cloud platform credentials.

**NOTE:**  To obtain the JSON file and the database_url value, please contact Juan Rodriguez at  David.Rodriguez@endava.com,
as the credentials file has to be created and the user registered in GCP.

The requests may be sent to the Heroku server, and those message will be queued in the GCP Pub/Sub service. 
In order to process those requests, one instance of the Subscriber module has to be running (it may run locally).
To execute the code, it is required python 3.7+. 

First it is required to install dependencies `pip install -r requirements.txt`

After installing requirements, the code may be run: `python comms/subscriber.py`. 
It is running without problems if tou can read the message `Listening for messages on {TopicPath}..`

As soon as the module gets running, you will begin seeing the messages received from Pub/Sub.

## Send Requests

There are two ways to send requests to the service:

### Using Mobile App
To ease the process of sending the requests to the service, a mobile iOS was created, this app gives the 
option to send 1 request individually or send all the 1000 requests as fast as the device can.

**NOTE:** To receive access to the app, please contact Daniel Beltran at daniel.beltran@endava.com


###  Direct requests:

Send requests using a post method directly to https://hey-movie-2.herokuapp.com/rating adding a JSON with the following format as body:
{"user": 1, "movie": 1, "rating": 4.0}

The rating may have different values.
