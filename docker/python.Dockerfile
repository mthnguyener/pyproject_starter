FROM python:latest

WORKDIR /usr/src/pyproject_starter

COPY . .

RUN pip3 install --upgrade pip \
	#&& pip3 install --no-cache-dir -r requirements.txt \
	&& pip3 install -e .[all] \
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt clean -y

CMD [ "/bin/bash" ]

