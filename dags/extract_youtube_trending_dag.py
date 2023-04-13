from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

# from trending.extract.crawler import extract_trending_data 
from trending.service.service import extract_trending_youtube


default_args ={
    'owner': 'kpim'
}

with DAG(
    dag_id='daily_extract_youtube_trending_data',
    schedule_interval='@once',
    default_args=default_args,
    description='Daily Extract Youtube Trending Data',
    start_date=datetime(2022, 3, 2),
    tags=["example"],
) as dag:
    _extract_data = PythonOperator(
        task_id='extract_daily_command',
        python_callable=extract_trending_youtube
    )

_extract_data