FROM python:3.12.2
COPY . /flask-app-2024
WORKDIR /flask-app-2024
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
