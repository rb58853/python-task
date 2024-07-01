# Client-Server in Python
## Objective
The main objective of this project is to develop a client-server application using Python that allows for bidirectional communication between a client and a server. The application is designed to be highly scalable and extendable, following best practices in programming.

## General Operation
### Client
- Generation of Strings: The client generates strings of text based on a specific set of predefined rules.
- Sending Files: Once the strings are generated, the client creates a file containing these strings and sends it to the server.
- Receiving Responses: The client receives a response from the server, processes this information, and creates a new file with the received response.
### Server
- Reception of Files: The server waits to receive files sent by the client.
- Data Processing: Once the file is received, the server processes the contained strings according to its internal logic.
- Sending Responses: Finally, the server sends a response to the client, which will be used by the latter to generate a new file.
## Technologies Used
- Python: Programming language used for both client and server development.
- Sockets: Built-in Python library for handling network connections and communications between client and server.
## Main Features
- Scalability: Designed to support a large number of simultaneous clients without significantly affecting performance.
- Extensibility: Allows easy addition of new features or modification of existing ones.
- Efficiency: Optimized to minimize resource usage and maximize processing speed.

# Run app
## Run Server
To start the server, open a terminal at the location of this file (README.md). First, navigate to the server directory by typing the following bash command: 

    ```
        cd src/server
    ```

Then, to run the server with the default parameters (`port = 8080`, `dir = '127.0.0.1'`), execute the following bash command:    

    ```
        python3 main.py
    ```

Additionally, you can pass the port and address it wishes to use with the commands.    

    ```
        python3 main.py --port 8080 --dir 127.0.0.1
    ```

## Run Client
To start the server, open a terminal at the location of this file (README.md). First, navigate to the server directory by typing the following bash command: 

    ```
        cd src/client
    ```

Then, to run the client with the default parameters (`port = 8080`, `dir = '127.0.0.1'`), execute the following bash command:    

    ```
    python3 main.py
    ```

Additionally, you can pass the port and address it wishes to use with the commands.    

    ```
    python3 main.py --port 8080 --dir 127.0.0.1 --filespath path/to/folder/for/files --responsespath path/to/folder/for/responses
    ```

