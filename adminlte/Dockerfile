# Use a imagem base do Python
FROM python:3.9

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Cria o ambiente virtual Python e instala as dependências
RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip \
    && /opt/venv/bin/python -m pip install -r requirements.txt

# Comando para iniciar sua aplicação, por exemplo:
# CMD ["python", "manage.py", "runserver"]
