from concurrent import futures
import time

import grpc
import greet_pb2
import greet_pb2_grpc
import requests
import numpy as np
import random
import hashlib
import pika
import threading
import json


class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def GetMineSerialNumber(self, request, context):
        # Implementation logic for GetMineSerialNumber
        mine_number = request.i
        # Read serial numbers from the 'mines.txt' file
        with open('mines.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) < mine_number:
                context.set_details("mine number out of range in mines.txt file")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                raise grpc.RpcError("")
            line = lines[mine_number - 1].strip()
            serial_number = line
        # Create a response message with the serial number
        mine_serial_number = greet_pb2.MineSerialNumber(serialNumber=serial_number)
        print(f"Mine serial number for mine {mine_number}: {serial_number}")
        # Print the serial number on the server side
        return mine_serial_number

    # method to print the pin of the disamed mine
    def PrintPin(self, request, context):
        print(f"The pin value for this mine : {request.value}")
        return greet_pb2.Empty()

    # method to fetch public api to get moves, and parse the data into a string
    def FetchCommands(self, request, context):
        # Construct the URL for the API endpoint
        url = 'https://coe892.reev.dev/lab1/rover/{}'.format(request.num)
        # Fetch command data from the API endpoint
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the response JSON data
            data = response.json()
            # Extract the moves field from the response data
            commands = data['data']['moves']
            # Create a RoverCommands message with the parsed commands
            rover_commands = greet_pb2.RoverCommands(hasCommands=True, commands=commands)
            return rover_commands
        else:
            # Handle the error
            context.set_details("Error fetching command data from API: status code {}".format(response.status_code))
            context.set_code(grpc.StatusCode.INTERNAL)
            return greet_pb2.RoverCommands()

    # reads map.txt file and returns the data as a string
    def FetchMap(self, request, context):
        try:
            # Read the contents of the map.txt file into a string
            with open('map.txt', 'r') as f:
                data = f.read()
            # Create a RoverMap message with the map data as the string
            rover_map = greet_pb2.RoverMap(data=data)
            return rover_map
        except FileNotFoundError:
            # Handle the error if the map.txt file is not found
            context.set_details("map.txt file not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return greet_pb2.RoverMap()

    # method to print completion message to the server once called by the client
    def SayHello(self, request, context):
        # prints a message to server when the mine has completed all tasks
        print("Exuection Complete!")
        print(request)
        hello_reply = greet_pb2.HelloReply()
        # hello_reply.message = f"{request.greeting} {request.name}"

        return hello_reply


def serve():
    # connects to localhost port and starts the server, prints message for server start and termination
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    print("Server started")
    server.wait_for_termination()
    print("Greet ended")


def defused_mines():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='defused-queue')

    def callback(ch, method, properties, body):
        body = json.loads(body.decode('utf-8'))

        serial_number = body['serial_num']
        pin = body['pin']
        print("Print defuse mine with " + serial_number + "and pin" + str(pin))

    channel.basic_consume(queue='defused-queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    # creates a new thread to consume the defused queue
    t = threading.Thread(target=defused_mines)
    t.start()

    serve()
