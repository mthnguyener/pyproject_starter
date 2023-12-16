FROM python:3.10

WORKDIR /usr/src/pyproject_starter/pyproject_starter/app/streamlit

COPY ../app/streamlit .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/pyproject_starter/pyproject_starter

COPY ../app/__init__.py .

COPY ../app/__init__.py ./app

ENV PYTHONPATH=/usr/src/pyproject_starter

CMD ["streamlit", "run", "app/streamlit/app.py"]
