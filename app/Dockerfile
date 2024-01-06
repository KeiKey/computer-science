# Use official Python image
FROM python:3.9-alpine

WORKDIR /app

# Install X11 utilities and XVFB
RUN apk --no-cache add \
    xorg-server \
    xinit \
    xvfb \
    && pip install --upgrade pip

# Copy requirements file and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Copy the content from the host /code directory into the image
COPY /code /app

# Set environment variables for X11
ENV DISPLAY=:0.0

# Run a command to keep the container running
CMD ["tail", "-f", "/dev/null"]
