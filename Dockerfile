FROM python:3.8

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
# create work dir
RUN mkdir /app


# Copy reqs
COPY ./requirements.txt .
# Install reqs
RUN pip install -r requirements.txt

RUN pip install --upgrade pip
# Copy all stuff
COPY . /app
# Define work dir
WORKDIR /app

# Run python  manage.py
CMD python3 manage.py runserver

