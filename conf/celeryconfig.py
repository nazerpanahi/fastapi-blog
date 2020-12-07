broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'

include = ['broker.tasks']

task_serializer = 'json'
result_serializer = 'json'

timezone = 'Asia/Tehran'
enable_utc = True
