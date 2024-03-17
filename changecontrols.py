import os
import sys

# Create a named pipe or file for communication
pipe_name = 'controller_pipe'

if sys.platform == 'win32':
    # Windows implementation
    import win32pipe
    import win32file

    # Create a named pipe on Windows
    pipe_handle = win32pipe.CreateNamedPipe(
        r'\\.\pipe\{}'.format(pipe_name),
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None
    )
    # Connect to the named pipe
    win32pipe.ConnectNamedPipe(pipe_handle, None)
else:
    # Unix-like systems implementation
    if not os.path.exists(pipe_name):
        print(f"Named pipe '{pipe_name}' does not exist. Make sure the main script is running.")
        sys.exit(1)

# Check command-line options
if len(sys.argv) != 2 or sys.argv[1] not in ['randomize', 'reset']:
    print("Usage: python changecontrols.py [randomize|reset]")
    sys.exit(1)

message = sys.argv[1]

try:
    # Write the message to the pipe
    if sys.platform == 'win32':
        # Write to the named pipe on Windows
        win32file.WriteFile(pipe_handle, message.encode())
    else:
        # Open the named pipe for writing on Unix-like systems
        with open(pipe_name, 'w') as pipe:
            pipe.write(message)
            pipe.flush()

    print(f"Sent message: {message}")

except KeyboardInterrupt:
    # Clean up and exit gracefully
    print("Exiting...")
    if sys.platform == 'win32':
        win32file.CloseHandle(pipe_handle)