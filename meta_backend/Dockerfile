FROM ubuntu:oracular

RUN mkdir /meta_backend

WORKDIR /meta_backend

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip

COPY ./requirements.txt .

RUN /meta_backend/venv/bin/pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "/meta_backend/venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" ]
