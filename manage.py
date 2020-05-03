# python manage.py run
# python manage.py run_worker

#import redis
#from rq import Connection, Worker
from flask.cli import FlaskGroup

from app import create_app

application = create_app()
cli = FlaskGroup(create_app=create_app)

"""
@cli.command("run_worker")
def run_worker():
    redis_url = app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config["QUEUES"])
        worker.work()
"""

if __name__ == "__main__":
    cli()