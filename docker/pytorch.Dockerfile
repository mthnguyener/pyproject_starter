FROM nvcr.io/nvidia/pytorch:23.11-py3

ENV TORCH_HOME=/usr/src/pyproject_starter/cache

WORKDIR /usr/src/pyproject_starter

COPY . .

RUN pip install --upgrade pip \
	&& pip install -e .[all] \
	&& apt update -y \
	# && apt -y upgrade \
	&& apt install -y\
		fonts-humor-sans \
	# && conda update -y conda \
	# && while read requirement; do conda install --yes ${requirement}; done < requirements_pytorch.txt \
	# Clean up
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt clean -y

CMD [ "/bin/bash" ]

