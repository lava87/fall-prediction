# Wearable Fall Prediction Device 
Software for a wearable fall prediction device that patients with foot drop condition can use to increase awareness of gait posture and prevent falls.

## Technology Used
- Arduino 
    - Write sensor data to serial comms
    - Control vibration motor
- Python
    - Gather sensor data from serial comms
    - Write data to csv 
    - Use threshold-based algorithm and gait cycle detection to predict foot positions that would likely lead to a fall
