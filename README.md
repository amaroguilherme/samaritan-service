# Samaritan

Samaritan is a service that allows users to create transactional orders amongst each other, in order to exchange it for goods. An "order", can be anything.

# Installation and setup
- Make sure you're on a virtual environment by doing the following:

```
python3 -m venv venv
source venv/bin/activate
```
- Then, install the requirements with:
```
pip install -r requirements.txt
```
- Once that is done, make sure you have a Postgres server INSTALLED AND RUNNING locally on your machine, and a JWT configuration in place with a `SECRET_KEY` created.

# Running the application locally
- The development server can be started with the command:
```
python main.py
```
More information on how to use the API can be found on the Swagger Documentation (Coming Soon).

# Running the application on a Docker container
- This can also be run on a container by first, creating a Postgres container:
```
docker run -p 5432:5432 -v /tmp/database:/var/lib/postgresql/data -e POSTGRES_USER=$USER -e POSTGRES_PASSWORD=$PASSWORD -d $CONTAINER_NAME
```
- Get the Postgres container IP address, in order to add it as a `HOST` on the Postgres `DATABASE_URI`:
```
docker inspect $CONTAINER_ID
```
- Build samaritan's image:
```
docker build --build-arg DATABASE_URI=${DATABASE_URI} --build-arg SECRET_KEY=${SECRET_KEY} -t ${CONTAINER_NAME} .
```
Where, `DATABASE_URI` is the configured Postgres URI ('postgresql://$USER:$PASSWORD@$HOST:$PORT/$DATABASE').
And, `SECRET_KEY` is the JWT Secret created earlier.

- Run the application with:
```
docker run -d -p 5000:5000 $IMAGENAME
```

# Running Unit tests
- Pretty straightforward, by running the command:
```
pytest
```