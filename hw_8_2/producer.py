import json
import pika
from faker import Faker
from models import Contact


fake = Faker()

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="task_mock", exchange_type="direct")
channel.queue_declare(queue="task_queue", durable=True)
channel.queue_bind(exchange="task_mock", queue="task_queue")


def main():
    for i in range(5):
        contact = Contact(fullname=fake.name(), email=fake.email())
        contact.save()

        contact_id = str(contact.id)

        message = {
            "contact_id": contact_id,
            "fullname": contact.fullname,
            "email": contact.email,
        }

        channel.basic_publish(
            exchange="task_mock",
            routing_key="task_queue",
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(" [x] Sent message for {contact.fullname}")
    connection.close()


if __name__ == "__main__":
    main()
