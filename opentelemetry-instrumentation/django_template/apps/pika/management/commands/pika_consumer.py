import json

from time import sleep

from django.core.management.base import BaseCommand

from django_template.apps.example.models import UserAttributes
from django_template.apps.pika import connection
from django_template.settings import CREATE_AUDIT_ACTION_DESTINATION_2
# from opentelemetry.instrumentation.pika import PikaInstrumentor


class Command(BaseCommand):
    help = "Consumer With PIKA"

    def handle(self, *args, **options):
        channel = connection.channel()
        # pika_instrumentation = PikaInstrumentor()
        # pika_instrumentation.instrument_channel(channel=channel)
        channel.queue_declare(queue=CREATE_AUDIT_ACTION_DESTINATION_2)

        def callback(ch, method, properties, body):
            print("Custom tracing - {}: {}".format("Consumer", "callback"))
            data = json.loads(body)
            print("DATA RECEIVED", data)
            sleep(10)
            user_id = data["user_id"]
            related_user = UserAttributes.objects.filter(id=user_id)
            print("Query result", related_user.count())

        channel.basic_consume(queue=CREATE_AUDIT_ACTION_DESTINATION_2, on_message_callback=callback, auto_ack=True)
        print("Started Consuming")
        channel.start_consuming()
        # channel.close()
