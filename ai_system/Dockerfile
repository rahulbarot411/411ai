FROM python:3.12-slim AS runtime
WORKDIR /app
COPY ai_system/backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY ai_system/backend/app /app/app
COPY ai_system/frontend /app/frontend
COPY ai_system/data /app/data
COPY ai_system/cli/ai_cli.py /usr/local/bin/ai-cli
RUN chmod +x /usr/local/bin/ai-cli
EXPOSE 8080
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
