FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install pandas 
RUN pip install numpy

EXPOSE 80

COPY ./app /app