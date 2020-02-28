FROM arm32v6/python:3-alpine
WORKDIR /usr/src/app

# Install build tools
RUN apk --no-cache --update add gawk bc socat git gcc libc-dev linux-headers scons swig

# Install the python GPIO library
RUN pip install RPi.GPIO

# Copy over the required files
COPY ./fanctrl.py .

# Run the daemon
CMD python fanctrl.py

