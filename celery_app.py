from celery import Celery

# amqp://user:pass@host:port/vhost
BROKER_URL = "amqp://guest:guest@localhost:5672//"

# rpc:// uses RabbitMQ itself to store results (good for dev/learning)
# For production you'd typically use Redis: redis://localhost:6379/0
RESULT_BACKEND = "rpc://"

celery = Celery(
    "celery_rabbitmq",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["tasks"],  # modules where tasks are defined
)

celery.conf.update(
    task_track_started=True,  # lets you see STARTED state (not just PENDING)
    result_expires=3600,      # results expire after 1 hour
)
