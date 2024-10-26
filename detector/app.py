from flask import Flask, request, jsonify
import os
import pika
import threading
from PIL import Image
import requests
import json
from tenacity import retry, wait_exponential, stop_after_attempt

app = Flask(__name__)

# Retry connection to RabbitMQ
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(10))
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='detection_queue')
    return channel

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files or 'user_id' not in request.form:
        print("Missing image or user_id")
        return jsonify({"error": "Missing image or user_id"}), 400

    image = request.files['image']
    user_id = request.form['user_id']

    # Save image to app/temp folder
    temp_dir = os.path.join(os.getcwd(), 'app/temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    image_path = os.path.join(temp_dir, image.filename)
    image.save(image_path)
    print(f"Image saved to {image_path}")

    # Send message to RabbitMQ
    channel = connect_to_rabbitmq()
    channel.basic_publish(exchange='', routing_key='detection_queue', body=f"{image.filename},{user_id}")
    print(f"Message sent to RabbitMQ: {image.filename}, {user_id}")

    return jsonify({"status": "Image received and queued"}), 200

def calculate(image_path):
    print(f"Processing image: {image_path}")
    # Create two copies of the image
    image = Image.open(image_path)
    image_name, ext = os.path.splitext(image_path)
    image_1_path = f"{image_name}_1{ext}"
    image_2_path = f"{image_name}_2{ext}"
    image.save(image_1_path)
    image.save(image_2_path)
    print(f"Image copies created: {image_1_path}, {image_2_path}")

    return image_1_path, image_2_path

def process_queue():
    channel = connect_to_rabbitmq()
    for method_frame, properties, body in channel.consume('detection_queue'):
        image_filename, user_id = body.decode().split(',')
        image_path = os.path.join(os.getcwd(), 'app/temp', image_filename)
        print(f"Processing message from queue: {image_filename}, {user_id}")

        # Process the image
        image_1_path, image_2_path = calculate(image_path)

        # Send result to tg_bot
        with open(image_1_path, 'rb') as img1, open(image_2_path, 'rb') as img2:
            # response = requests.post(f"http://tg_bot:5001/send_result", files={
            #     'image_1': img1,
            #     'image_2': img2,
            #     'json': ('json', json.dumps({"user_id": user_id}))
            # })
            response = requests.post("http://tg_bot:5001/send_result", files={'image_1': img1, 'image_2': img2}, data={'user_id': user_id})
            print(f"Response from tg_bot: {response.status_code}")

        # Acknowledge the message
        channel.basic_ack(method_frame.delivery_tag)

        # Clean up
        os.remove(image_path)
        os.remove(image_1_path)
        os.remove(image_2_path)
        print(f"Cleaned up files: {image_path}, {image_1_path}, {image_2_path}")

if __name__ == "__main__":
    threading.Thread(target=process_queue).start()
    app.run(host='0.0.0.0', port=5000)