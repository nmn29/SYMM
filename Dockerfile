FROM python:3.9.1

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY symm.py /app/
COPY cogs/ /app/cogs/

WORKDIR /app
ENTRYPOINT [ "python", "symm.py" ]
