# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install pyjwt 
RUN pip install google
RUN pip install datetime
RUN pip install google-resumable-media
RUN pip install google-cloud-storage
RUN pip install google-cloud-bigquery

 


# Copy local code to the container image.
WORKDIR /app
COPY . .

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080
ENV GOOGLE_APPLICATION_CREDENTIALS="{PATH-TO-SERVICE-ACCOUNT}"

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 --preload app:app
