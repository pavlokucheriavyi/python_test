FROM python:latest
# Or any preferred Python version.
ADD test.py .
ADD requirements.txt requirements.txt
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "test.py"]