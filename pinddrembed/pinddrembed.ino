enum ButtonPin {
  PIN_A = 5,
  PIN_B = 6,
  PIN_X = 10,
  PIN_Y = 11
};

const int NUM_BUTTONS = 10;
const ButtonPin buttonPins[NUM_BUTTONS] = {
  PIN_A,
  PIN_B,
  PIN_X,
  PIN_Y,
};

const String buttonNames[NUM_BUTTONS] = {
  "A",
  "B",
  "X",
  "Y"
};

bool buttonStates[NUM_BUTTONS] = {false};

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set pin modes
  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(buttonPins[i], OUTPUT);
  }
}

void loop() {
  // Check if data is available on the serial bus
  if (Serial.available()) {
    // Read the data from the serial bus
    String data = Serial.readStringUntil('\n');
    data.trim();

    // Parse the data
    int spaceIndex = data.indexOf(' ');
    if (spaceIndex >= 0) {
      String buttonName = data.substring(0, spaceIndex);
      String actionName = data.substring(spaceIndex + 1);

      // Find the corresponding button index
      int buttonIndex = -1;
      for (int i = 0; i < NUM_BUTTONS; i++) {
        if (buttonName == buttonNames[i]) {
          buttonIndex = i;
          break;
        }
      }

      // Update the button state based on the action
      if (buttonIndex >= 0) {
        if (actionName == "press") {
          buttonStates[buttonIndex] = true;
        } else if (actionName == "release") {
          buttonStates[buttonIndex] = false;
        }
      }
    }

    // Send a confirmation response back to Python
    Serial.println("Data processed");
  }

  // Set the pin states based on the button states
  for (int i = 0; i < NUM_BUTTONS; i++) {
    digitalWrite(buttonPins[i], buttonStates[i] ? HIGH : LOW);
  }
}