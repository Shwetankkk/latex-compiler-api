FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-pictures \
    latexmk \
    python3 \
    python3-venv \
    python3-pip \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv $VENV_PATH \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8080
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "server:app"]
