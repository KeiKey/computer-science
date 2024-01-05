# Use official Python image
FROM python:3.9-slim-buster

# Set environment variable
#ENV PYTHONUNBUFFERED 1
#RUN pip3 install -r requirements.txt

# Install Python libraries 
RUN #pip3 install numpy matplotlib