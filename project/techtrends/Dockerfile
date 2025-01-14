FROM python:3.8
LABEL maintainer="Igor Kramer"
COPY . ./app
WORKDIR /app
EXPOSE 3111
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "/bin/bash","-c","python init_db.py;python app.py" ]
