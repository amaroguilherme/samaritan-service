FROM python:3.9-slim
ENV PYTHONPATH="."

ARG DATABASE_URI
ARG SECRET_KEY

ENV DATABASE_URI=${DATABASE_URI}
ENV SECRET_KEY=${SECRET_KEY}

COPY api /api
COPY storage /storage
COPY ["app.py", "main.py", "requirements.txt", "utils.py", "/"]

RUN pip install -r requirements.txt

CMD ["python", "main.py"]