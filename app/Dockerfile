FROM python:3.10.12
COPY . /app
# COPY requirements.txt /tmp/

WORKDIR /app
# COPY requirements.txt /app
# COPY Data_fetching.py /app
# COPY app.py /app

# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     libjpeg-turbo-dev zlib-dev

# RUN pip install --upgrade cython
RUN pip install --upgrade pip

# RUN pip freeze > requirements.txt
# RUN pip install --requirement /tmp/requirements.txt
RUN pip install -r requirements.txt
CMD sh -c "sleep 10s; python3 app.py"
	
