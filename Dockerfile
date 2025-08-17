# Usar imagen oficial de Python
FROM python:3.10-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Exponer puerto
EXPOSE 8000

# Ejecutar Gunicorn con logs visibles
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:8000", "--workers", "1", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-"]
