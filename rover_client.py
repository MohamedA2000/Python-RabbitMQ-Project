import sys
import greet_pb2_grpc
import greet_pb2
import grpc
import random
import hashlib
import uuid
import pika
import json


def send_demine_message(serial_number):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='demine-queue')

    body = {
        'serial_number': serial_number
    }
    bodyString = json.dumps(body).encode('utf-8')
    print(bodyString)

    channel.basic_publish(exchange='', routing_key='demine-queue', body=bodyString)
    connection.close()


def run(rover_num):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)

        # Print the response message
        with open("mines.txt") as f:
            mine_numbers = [line.strip() for line in f]
        # creates a grpc client stub for server channel to allow rpc requests
        stub = greet_pb2_grpc.GreeterStub(channel)
        # Call the FetchMap method
        # makes rpc request for fetch map method
        response = stub.FetchMap(greet_pb2.Empty())
        # Convert the map string to a 2D array
        map_data = response.data.split("\n")[1:]
        map_data = [row.split() for row in map_data]
        for row in map_data:
            print(" ".join(row))
        # print(map_data[4][1])
        # Traverse the 2D array
        for row in range(len(map_data)):
            for col in range(len(map_data[0])):
                if map_data[row][col] == "1":
                    print(f"A Bomb is located at ({col},{row})")

        response = stub.FetchCommands(greet_pb2.RoverNumber(num=int(rover_num)))

        # Print the response message
        print("Received commands: {}".format(response.commands))

        # Initialize the rover's position and direction
        pos_x = 0
        pos_y = 0
        direction = "SOUTH"
        dug_locations = []
        # Initialize a flag to keep track of whether the rover has encountered an obstacle
        obstacle_encountered = False
        bomb_dug = False

        # Execute the moves on the map
        idx = 0
        counter = 0
        # the moves copied from lab 1, conditional statements define the directions,
        # and what happens when a certain  move is executed
        commands = response.commands
        while idx < len(commands) and not obstacle_encountered:
            move = commands[idx]
            if move == 'L':
                # Turn left but stay in the same position
                if direction == "NORTH":
                    direction = "WEST"
                elif direction == "WEST":
                    direction = "SOUTH"
                elif direction == "SOUTH":
                    direction = "EAST"
                else:
                    direction = "NORTH"
            elif move == 'R':
                # Turn right but stay in the same position
                if direction == "NORTH":
                    direction = "EAST"
                elif direction == "EAST":
                    direction = "SOUTH"
                elif direction == "SOUTH":
                    direction = "WEST"
                else:
                    direction = "NORTH"
            elif move == 'M':
                if direction == "NORTH" and pos_y > 0:
                    pos_y -= 1
                elif direction == "EAST" and pos_x < len(map_data[0]) - 1:
                    pos_x += 1
                elif direction == "SOUTH" and pos_y < len(map_data) - 1:
                    pos_y += 1
                elif direction == "WEST" and pos_x > 0:
                    pos_x -= 1
            elif move == 'D':
                # Dig at the current position
                # print("Dug at position ({}, {})".format(pos_x, pos_y))
                # dug_locations.append((pos_y, pos_x))
                mine_number = greet_pb2.MineNumber(i=random.randint(5, 40))
                response = stub.GetMineSerialNumber(mine_number)

                # send rabbitmq message
                send_demine_message(response.serialNumber)
            else:
                # Invalid move
                print("Invalid move: {}".format(move))

            if map_data[pos_y][pos_x] == "1":
                if idx < len(commands) - 1 and commands[idx + 1] == "D":
                    # print(f"Bomb dug at ({pos_x},{pos_y})")
                    mine_number = random.choice(mine_numbers)
                    counter += 1
                    # print(f"Bomb dug at ({pos_x},{pos_y}), serial number: {mine_number}")
                    print(f"Bomb {counter} dug at ({pos_x},{pos_y})")

                    continue
                else:
                    # If the next move is not "D", break out of the loop
                    print("Stopped due to explosion at ({}, {})".format(pos_x, pos_y))

                    break

            idx += 1
        # Print the final position and direction of the rover
        print("Final Rover position: ({}, {})".format(pos_x, pos_y))
        print("Final Rover direction: {}".format(direction))

        mine_num = 1

        # for mine_number in range(1, counter + 1):
            # mine_number = greet_pb2.MineNumber(i=random.randint(5, 40))
            # response = stub.GetMineSerialNumber(mine_number)

            # print("Received serial number for mine {}: {}".format(mine_number.i, response.serialNumber))
            # sets random pin and preforms hashing function,
            # copied from lab 1
            # pin = random.randint(1, 99999999999)
            # tempKey = str(pin) + response.serialNumber
            # hash = hashlib.sha256(tempKey.encode()).hexdigest()
            # while (not str(hash).startswith("000")):
            #     pin = random.randint(1, 99999999999)
            #     tempKey = str(pin) + response.serialNumber
            #     hash = hashlib.sha256(tempKey.encode()).hexdigest()
            # print the various keys and serial numbers and hash values hashed
            # from the above code
            # print("Serial Number: " + response.serialNumber)
            # print("Temporary Key: " + tempKey)
            # print("Hash Value: " + str(hash))
            # print("pin:" + str(pin))
            # stub.PrintPin(greet_pb2.Pin(value=pin))
            # increment the mine number
            # mine_num += 1
            # # reset the mine number to 1 if it exceeds 45
            # if mine_num > 45:
            #     mine_num = 1

        hello_request = greet_pb2.HelloRequest()
        hello_reply = stub.SayHello(hello_request)
        print("Exeuction Complete!")
        print(hello_reply)


if __name__ == "__main__":
    rover_num = sys.argv[1]  # Get the rover number from the command line
    run(rover_num)  # run the program with the number from CLI as rover number input
