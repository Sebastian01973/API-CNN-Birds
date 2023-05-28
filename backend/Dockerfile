FROM python:3.10-slim-buster

# set work directory
WORKDIR /code

# set environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=5000

# install dependencies
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# copy requeriments.txt
COPY requirements.txt requirements.txt

# install requirements
RUN pip install -r requirements.txt

# expose port 3000
EXPOSE 5000

# copy project
COPY . .

# run app
# CMD ["flask", "run", "--port=5000"]
CMD [ "python3", "src/app.py"]