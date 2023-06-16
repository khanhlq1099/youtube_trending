from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

from trending.service.service import extract_trending_youtube

default_args ={
    'owner': 'kpim'
}

with DAG(
    # Set up config DAG
    dag_id='daily_extract_youtube_trending_data',
    # schedule_interval='0 9,11,13,15 * * *',
    schedule_interval='@once',
    default_args=default_args,
    description='Daily Extract Youtube Trending Data',
    start_date=datetime(2023, 4, 24),
    tags=["example"],
    catchup=False,
) as dag:
    # Python Operator call function extract
    _extract_data = PythonOperator(
        task_id='extract_daily_command',
        python_callable=extract_trending_youtube
    )

_extract_data