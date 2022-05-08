from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, date, datetime


COVID_19_API_URL="https://covid19.mathdro.id/api"
S3_BUCKET = "covid-19-mathdroid"


default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 0,
    "retry_delay": timedelta(minutes=5)
}


def aws_configure():
    from airflow.models import Variable
    import os
    aws_auth = Variable.get("aws_authorization", deserialize_json=True)
    os.environ["AWS_ACCESS_KEY_ID"] = aws_auth["AWS_ACCESS_KEY_ID"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_auth["AWS_SECRET_ACCESS_KEY"]
    os.environ["AWS_DEFAULT_REGION"] = aws_auth["AWS_DEFAULT_REGION"]


def upload_csv_to_s3(df):
    import boto3
    from io import StringIO # python3; python2: BytesIO 
    aws_configure()
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    today = date.today()
    date_str = today.strftime("%b-%d-%Y")
    s3_resource.Object(S3_BUCKET, f"{date_str}/confirmed_cases.csv").put(Body=csv_buffer.getvalue())


def hit_covid_api():
    import requests
    confirmed_cases_response = requests.get(f"{COVID_19_API_URL}/confirmed")
    if (confirmed_cases_response.status_code == 200):
        return confirmed_cases_response.json()
    else:
        return {}


def fetch_nd_store_data_to_s3(**context: dict):
    import pandas as pd
    confirmed_cases_json = hit_covid_api()
    if confirmed_cases_json:
        confirmed_cases_df = pd.DataFrame.from_dict(confirmed_cases_json)
        upload_csv_to_s3(confirmed_cases_df)


with DAG(
        dag_id="covid_19_data_store",
        start_date=datetime(2021, 7, 1),
        schedule_interval="@daily",
        tags=["COVID"],
        default_args=default_args,
        catchup=False
) as dag:

    fetch_nd_store_data_to_s3 = PythonOperator(
            task_id="fetch_nd_store_data_to_s3",
            python_callable=fetch_nd_store_data_to_s3,
            provide_context=True
    )
