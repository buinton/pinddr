import os
import sys
import time
import random
import pygame
import serial
import serial.tools.list_ports

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check if an Xbox controller is connected
if pygame.joystick.get_count() > 0:
    # Get the first connected joystick (assuming it's an Xbox controller)
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Controller connected.")
else:
    print("No controller found.")
    pygame.quit()
    exit()

# Button mapping (adjust according to your controller)
original_button_map = {
    0: "Y",
    1: "A",
    2: "X",
    3: "B"
}
button_map = original_button_map.copy()

# Detect available serial devices
serial_devices = list(serial.tools.list_ports.comports())

if len(serial_devices) == 0:
    print("No serial devices found.")
    pygame.quit()
    exit()

# Display the menu to select the serial device
print("Available serial devices:")
for i, device in enumerate(serial_devices):
    print(f"{i + 1}. {device.device}")

selection = input("Enter the number of the serial device to use: ")
try:
    index = int(selection) - 1
    if 0 <= index < len(serial_devices):
        selected_device = serial_devices[index].device
    else:
        raise ValueError
except ValueError:
    print("Invalid selection. Exiting.")
    pygame.quit()
    exit()


# Configure the serial connection
baud_rate = 9600  # Replace with the desired baud rate

# Open the serial connection
ser = serial.Serial(selected_device, baud_rate)
print(f"Connected to serial device: {selected_device}")


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
else:
    # Unix-like systems implementation
    if os.path.exists(pipe_name):
        os.remove(pipe_name)
    os.mkfifo(pipe_name)

try:
    # Main loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                if button in button_map:
                    button_name = button_map[button]
                    print(f"Button pressed: {button_name}")
                    ser.write(f"{button_name} press\n".encode())  # Send the button press command
                else:
                    print(f"Unknown button pressed: {button}")
            elif event.type == pygame.JOYBUTTONUP:
                button = event.button
                if button in button_map:
                    button_name = button_map[button]
                    print(f"Button released: {button_name}")
                    ser.write(f"{button_name} release\n".encode())  # Send the button release command
                else:
                    print(f"Unknown button released: {button}")

        # Check if there is any message from the external executable
        if sys.platform == 'win32':
            # Read from the named pipe on Windows
            if win32pipe.PeekNamedPipe(pipe_handle, None):
                try:
                    data = win32file.ReadFile(pipe_handle, 4096)
                    message = data[1].decode().strip()
                except Exception as e:
                    message = ''
            else:
                message = ''
        else:
            # Read from the named pipe on Unix-like systems using non-blocking I/O
            if os.path.exists(pipe_name):
                try:
                    pipe_fd = os.open(pipe_name, os.O_RDONLY | os.O_NONBLOCK)
                    message = os.read(pipe_fd, 1024).decode().strip()
                    os.close(pipe_fd)
                except OSError:
                    message = ''
            else:
                message = ''

        if message:
            # Process the message and update the state accordingly
            if message == 'randomize':
                # Randomize the button mapping
                buttons = list(original_button_map.values())
                while True:
                    random.shuffle(buttons)
                    if buttons != list(button_map.values()):
                        break
                button_map = {i: buttons[i] for i in range(len(buttons))}
                print(f"Randomized button mapping: {button_map}")
            elif message == 'reset':
                # Reset the button mapping to the original layout
                button_map = original_button_map.copy()
                print("Button mapping reset to original layout")
            # Add more conditions as needed

        # Read the response from Arduino
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"Arduino response: {response}")

        # Add a small delay to avoid excessive CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up and exit gracefully
    print("Exiting...")
    ser.close()
    pygame.quit()
    if sys.platform == 'win32':
        win32file.CloseHandle(pipe_handle)
    else:
        os.remove(pipe_name)