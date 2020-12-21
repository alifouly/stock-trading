FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN easy_install SQLAlchemy &&\
    pip3 install fastapi &&\
    pip3 install pydantic &&\
    pip3 install python-multipart
COPY ./app /app
