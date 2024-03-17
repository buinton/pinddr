import pygame

pygame.init()
print("Pygame initialized successfully!")

# Check if a joystick is detected
num_joysticks = pygame.joystick.get_count()
print(f"Number of joysticks detected: {num_joysticks}")

if num_joysticks > 0:
    # Get the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick name: {joystick.get_name()}")
    print(f"Number of axes: {joystick.get_numaxes()}")
    print(f"Number of buttons: {joystick.get_numbuttons()}")
else:
    print("No joysticks found.")

pygame.quit()