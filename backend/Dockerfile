FROM python:3.8-alpine

# set work directory
WORKDIR /code

# set environment variables
ENV FLASK_APP=src/main.py
ENV FLASK_RUN_HOST=0.0.0.0

# install dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# copy requeriments.txt
COPY requirements.txt requirements.txt

# install requirements
RUN pip install -r requirements.txt

# expose port 3000
EXPOSE 5000

# copy project
COPY . .

# run app
CMD ["flask", "run", "--port=5000"]