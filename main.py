from tasks import process_task

if __name__ == '__main__':
    task_name = 'Task 1'
    process_task.delay(task_name)
    for i in range(2):
        process_task.delay(f'Task {i+2}')
