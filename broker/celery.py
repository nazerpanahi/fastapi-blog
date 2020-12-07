from celery import Celery


app = Celery('broker')

app.config_from_object('conf.celeryconfig')

if __name__ == "__main__":
    app.start()
