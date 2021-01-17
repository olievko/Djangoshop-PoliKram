# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /Djangoshop

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile Pipfile.lock /Djangoshop/
RUN pipenv install --system

#ADD requirements.txt /Djangoshop/
#RUN pip install -r requirements.txt

# Copy project
ADD . /Djangoshop/