# https://hub.docker.com/layers/python/library/python/3.9/images/sha256-b7e449e11f8c466fbaf021dcc731563cb36a41321420db3cf506ba4d71d33a65?context=explore
FROM python:3.9-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# CMD [ "python", "./your-daemon-or-script.py" ]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
