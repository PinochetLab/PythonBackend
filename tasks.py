from celery import Celery

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//')

@app.task
def process_task(task_name):
    print('Обработка задачи:', task_name)
