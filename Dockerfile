FROM python:3.10-slim

RUN groupadd cats && useradd floppa -g cats


WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./
RUN pip install --no-cache-dir --upgrade --root-user-action ignore pip setuptools wheel poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root  # Installs dependencies.

COPY ./enchanted_motorbike ./enchanted_motorbike


USER floppa
EXPOSE 8000
ENTRYPOINT ["python", "-m", "enchanted_motorbike"]
