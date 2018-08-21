# MAD - Basic Python Webservice Setup

## General Remarks
I decided to use [Flask-RESTful](http://flask-restful.readthedocs.io/en/latest/) as framework to build our REST-APIs. The implementation is based on this [tutorial](https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful) and the respective [python file](https://github.com/miguelgrinberg/REST-tutorial/blob/master/rest-server-v2.py). To test / play with the server have a look at the [Flask-RESTful Quickstart Guide](http://flask-restful.readthedocs.io/en/latest/quickstart.html).

## Structure
- docker/: All files that are needed to deploy the webservice as docker container
- src: Python file for starting the Flask-RESTful-Server
    - resources/: All resources that are offered by the REST-API
    - ...

## Deploying the Server
To deploy the server just clone [this repo](https://github.com/juliangruendner/mlService_webserviceBase/) and change to the [docker-dirctory](docker/) and execute the command 
``` docker-compose up ``` 
in your terminal. The server will then be reachable on port 5000.

## Extending the API
If you want to extend the functionality of the server just create a new resource in the [resources-directory](src/resources/). Then import the new resource in the [API-file](src/api.py) and add the resource to the *api*-object by using the *add_resource*-function.

## Testing the server
After you have started the server you can test it by sending http requests. If the server is running on your local machine you could for instance execute the following [curl](https://curl.haxx.se/)-requests:
- get:
```
curl http://localhost:5000/example
curl http://localhost:5000/example/2
```
- delete:
```
curl http://localhost:5000/example/1 -X DELETE -v
```
- post:
```
curl -H "Content-Type: application/json" http://localhost:5000/example -d '{"data":"foo"}' -X POST -v
```
- put:
```
curl -H "Content-Type: application/json" http://localhost:5000/example/3 -d '{"data":"bar"}' -X PUT -v
```
