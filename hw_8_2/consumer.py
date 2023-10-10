import json
import pika


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def send_message(contact_id):
    # contact = Contact.objects(id=contact_id).first()
    # if contact:
    #     contact.email_sent = True
    #     contact.save()
    # print(f"Email sent to {contact.fullname}")
    ...


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    fullname = message.get("fullname")
    email = message.get("email")
    contact_id = message.get("contact_id")

    print(f" [x] Message for {fullname} with email {email}/nText: {message}")
    send_message(contact_id)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
