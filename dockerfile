FROM apache/airflow:2.6.1-python3.8
RUN pip install --user --upgrade pip
RUN pip install mysql-connector
RUN pip install requests
RUN pip install google-cloud-storage