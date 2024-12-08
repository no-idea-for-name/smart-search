FROM python:3.12.3

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt --root-user-action=ignore

# Make port 5000 available to the world outside this container
EXPOSE 6000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
#future setup script: # Run setup shell script 
CMD ["/bin/bash", "/app/config/knowledge-manager.sh"]