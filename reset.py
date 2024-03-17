import os

# Create a named pipe or file for communication
pipe_name = 'controller_pipe'
if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

try:
    # Open the named pipe for writing
    with open(pipe_name, 'w') as pipe:
        # Write a message to the pipe
        message = 'reset'
        pipe.write(message)
        pipe.flush()
        print(f"Sent message: {message}")

except KeyboardInterrupt:
    # Clean up and exit gracefully
    print("Exiting...")
