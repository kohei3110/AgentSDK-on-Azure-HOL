import json
import os
import azure.functions as func
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy
import logging
from azure.identity import DefaultAzureCredential

app = func.FunctionApp()

@app.function_name(name="get_weather")
@app.queue_trigger(arg_name="msg", queue_name="input",
                               connection="STORAGE_CONNECTION") 
def get_weather(msg: func.QueueMessage):
    logging.info('Python Queue trigger processed a message: %s',
                msg.get_body().decode('utf-8'))
    queue_client = QueueClient(
        os.environ["STORAGE_CONNECTION"],
        queue_name="output",
        credential=DefaultAzureCredential(),
        message_encode_policy=BinaryBase64EncodePolicy(),
        message_decode_policy=BinaryBase64DecodePolicy()
    )
    messagepayload = json.loads(msg.get_body().decode('utf-8'))
    location = messagepayload['location']
    result_message = {"weather": "sunny"}
    queue_client.send_message(json.dumps(result_message).encode('utf-8'))
    logging.info(f"Sent message to queue: output with message {result_message}")