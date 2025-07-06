FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY . .

RUN conda env create -f environment.yml

# Activate environment and install extra pip requirements
# RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate chatbot && pip install -r requirements.txt"

SHELL ["/bin/bash", "-c"]

CMD ["conda", "run", "-n", "chatbot", "python", "main.py"]
