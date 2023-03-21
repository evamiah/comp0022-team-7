# Use an official Python runtime as an image
FROM python:3.10

# The EXPOSE instruction indicates the ports on which a container
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction
# creates a directory with this name if it doesn’t exist
WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt

# Run app.py when the container launches
COPY app.py /app
COPY init.py /app
COPY rating.py /app
COPY movie_details.py /app
COPY req1_filter.py /app
COPY req5_predict.py /app
COPY tags.py /app
COPY helpers.py /app
COPY scripts/extension_scripts.py /app
COPY scripts/config.py /app
COPY templates /app/templates
COPY static /app/static
COPY data /app/data
CMD ["flask", "run", "--host", "0.0.0.0"]