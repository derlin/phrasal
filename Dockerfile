FROM python:3.7

WORKDIR /app

# copy module sources and setup files
COPY setup.py setup.cfg requirements.txt ./
RUN pip install -r requirements.txt

# install module
COPY src ./src
RUN python setup.py install

# set gunicorn run mode
# $PORT is set by Heroku or the --env-vars argument, set default to 80
ENV PORT=${PORT:-80}

# open default http port (optional)
EXPOSE $PORT

# Run the app. CMD is required to run on Heroku (vs ENTRYPOINT)
# Note: set enableCORS to false so it works on Heroku,
#       as explained here: https://github.com/streamlit/streamlit/issues/443
CMD streamlit run src/lit.py  --server.port $PORT --server.enableCORS false