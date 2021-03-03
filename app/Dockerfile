# Use an official Python runtime as an image
FROM python:3.7

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install mariadb-server -y
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
#RUN apt update && apt install postgresql-dev gcc python3-dev musl-dev build-dep python-psycopg2
#RUN pip3 install psycopg2
CMD mkdir /root/.kaggle
COPY kaggle.json /root/.kaggle/

# Run app when the container launches
COPY . /app
#CMD wait 9999
CMD python3 create_db.py
CMD python3 wsgi.py