# Usar una imagen oficial de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la app
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:8000"]
