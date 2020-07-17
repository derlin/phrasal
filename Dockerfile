FROM python:3.7

WORKDIR /app
RUN pip install --upgrade pip

# install module
COPY setup.py setup.cfg MANIFEST.in README.md ./
COPY src ./src
RUN pip install .[showcase]

# set gunicorn run mode
# $PORT is set by Heroku or the --env-vars argument, set default to 80
ENV PORT=${PORT:-80}

# open default http port (optional)
EXPOSE $PORT

# Run the app. CMD is required to run on Heroku (vs ENTRYPOINT)
# Note: set enableCORS to false so it works on Heroku,
#       as explained here: https://github.com/streamlit/streamlit/issues/443
CMD streamlit run src/showcase/lit.py  --server.port $PORT --server.enableCORS false