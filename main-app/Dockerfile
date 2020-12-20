FROM python:3
WORKDIR /app
RUN pip3 install uvicorn &&\
    easy_install SQLAlchemy &&\
    pip3 install fastapi &&\
    pip3 install pydantic &&\
    pip3 install python-multipart
COPY . /app
CMD uvicorn main:app --reload
