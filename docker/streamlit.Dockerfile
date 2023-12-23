FROM python:3.11

WORKDIR /usr/src/pyproject_starter/applications/streamlit

COPY ../applications/streamlit .

RUN pip install --upgrade pip \
	&& pip install \
        -r requirements.txt \
	&& apt update -y \
	# && apt -y upgrade \
	&& apt install -y\
		fonts-humor-sans \
        vim

ENV PYTHONPATH=/usr/src/pyproject_starter

CMD ["streamlit", "run", "app.py"]
