FROM pytorch/pytorch
RUN pip install Flask
COPY backend/main.py .
COPY backend/full_model .
ENV FLASK_APP=main
CMD flask run --host 0.0.0.0