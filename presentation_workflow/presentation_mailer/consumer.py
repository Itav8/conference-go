import json
import pika
import django
import os
import sys
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def main():
    # Set the hostname that we'll connect to
    parameters = pika.ConnectionParameters(host="rabbitmq")
    # Create a connection to RabbitMQ
    connection = pika.BlockingConnection(parameters)
    # Open a channel to RabbitMQ
    channel = connection.channel()
    # Create a queue if it does not exist
    channel.queue_declare(queue="presentation_approvals")
    # Configure the consumer to call the process_message function
    # when a message arrives
    channel.basic_consume(
        queue="presentation_approvals",
        on_message_callback=process_approval,
        auto_ack=True,
    )
    # Tell RabbitMQ that you're ready to receive messages
    channel.start_consuming()


def process_approval(ch, method, properties, body):
    print("  Received %r" % body)
    bio = json.loads(body)

    send_mail(
        "Your presentation has been accepted",
        f"{bio['presenter_name']}, we're happy to tell you that your presentation {bio['title']} has been accepted",
        "admin@conference.go",
        ["ita@dope.com"],
        fail_silently=False,
    )

    print("AFter sent")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
