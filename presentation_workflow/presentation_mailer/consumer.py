import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

while True:
    try:
        # ALL OF YOUR CODE THAT HANDLES READING FROM THE
        # QUEUES AND SENDING EMAILS

        def main():
            # Set the hostname that we'll connect to
            parameters = pika.ConnectionParameters(host="rabbitmq")
            # Create a connection to RabbitMQ
            connection = pika.BlockingConnection(parameters)
            # Open a channel to RabbitMQ
            channel_1 = connection.channel()
            channel_2 = connection.channel()
            # Create a queue if it does not exist
            channel_1.queue_declare(queue="presentation_approvals")
            channel_2.queue_declare(queue="presentation_rejections")
            # Configure the consumer to call the presentation_approvals function
            # when a message arrives
            channel_1.basic_consume(
                queue="presentation_approvals",
                on_message_callback=process_approval,
                auto_ack=True,
            )

            channel_2.basic_consume(
                queue="presentation_rejections",
                on_message_callback=process_rejection,
                auto_ack=True,
            )
            # Tell RabbitMQ that you're ready to receive messages
            channel_1.start_consuming()
            channel_2.start_consuming()

        def process_approval(ch, method, properties, body):
            print("  Received %r" % body)
            content = json.loads(body)

            send_mail(
                "Your presentation has been accepted",
                f"{content['presenter_name']}, we're happy to tell you that your presentation {content['title']} has been accepted",
                "admin@conference.go",
                [content["presenter_email"]],
                fail_silently=False,
            )

        def process_rejection(ch, method, properties, body):
            print("  Received %r" % body)
            content = json.loads(body)

            send_mail(
                "Your presentation has been rejected",
                f"{content['presenter_name']}, we're sorry to tell you that your presentation {content['title']} has been rejected",
                "admin@conference.go",
                [content["presenter_email"]],
                fail_silently=False,
            )

        if __name__ == "__main__":
            try:
                main()
            except KeyboardInterrupt:
                print("Interrupted")
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
