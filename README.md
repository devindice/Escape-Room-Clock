# Escape-Room-Clock
Adjust the clock and unlock a door
- Tested on Debian GNU/Linux 11 (bullseye)
- Python 3.9

# Node Red
Import the included dashboard to get an idea how to integrate with this app.

# Raspbery Pi 4 Setup
- sudo raspi-config
- Enable interface options
  - enable ssh
  - enable i2c
- Avoid GPIO pins 3 and 5 as this is the serial communication for I2C (Motor Controller)
- Connect buttons to the 3v DC line
- Pins 4-8,15 appear to be busy, not sure if they are available.

Commands:
- Update the OS
  - sudo apt update
  - sudo apt upgrade
- Install required Packages
  - sudo apt install python3-pip
  - sudo pip3 install adafruit-circuitpython-motorkit
- Setup Cron to Autostart and auto-update. Also there is a Log-rotate to keep logs small
  - sudo ln -sf /home/pi/Escape-Room-Clock/scheduler.cron /etc/cron.d/escape-room-clock 
  - sudo ln -sf /home/pi/Escape-Room-Clock/logrotate.conf /etc/logrotate.d/escape-room-clock 
  - sudo chown root:root /home/pi/Escape-Room-Clock/scheduler.cron
  - sudo chown root:root /home/pi/Escape-Room-Clock/logrotate.conf
  - sudo chmod 644 /home/pi/Escape-Room-Clock/scheduler.cron
  - sudo chmod 644 /home/pi/Escape-Room-Clock/logrotate.conf

# Config options
These can be sent as a JSON string over MQTT to update in real time.
The same will be returned on update to update the Node Red Dashboard.

- ticksFullRotation: How many ticks does the motor need for a full 360 rotation?
- style: Motor step style, smoothest seems to be interleave. Options are: 'interleave', 'single', 'double', 'micro'
- currentHr: Where is the hour hand currently? Decimals may be used.
- currentMn: Where is the minute hand currently? Decimals may be used.
- defaultHr: Where should the hour hand go when not in game mode? This can be interactively updated for a game clock, Submit 0-60 for minutes.
- defaultMn: Where should the minute hand go when not in game mode? This can be interactively updated for a game clock, Submit 0-60 for seconds.
- defaultTimer: Enable game timer mode, send default values above as minutes and seconds, the minutes will be converted to hours for the hours motor. Options are 'true' or 'false'
- setHr: This is set by the buttons on the Raspberry Pi. Setting this will move the hour hand if in game mode.
- setMn: This is set by the buttons on the Raspberry Pi. Setting this will move the minute hand if in game mode.
- mode: What mode is the app in. Three options exist: 'play' - This is using the buttons to move the clock. 'gameTimer' - This shows the default values when idle and can be used as a game timer. 'calibrate' - This moves the hands to 12:00 for calibration. This calibrate option does not need to exist as hands go to 12:00 when toggling mode to 'play'.
- triggerHr: What hour should the trigger pin be activated?
- triggerMn: What hour should the trigger pin be activated?
- triggerPin: What pin should be activated when the hour and time match?
- movementDelay: How much delay between movements. 0.25 seems to be nice. A value of 0 would be smoother.
- movementMinuteStep: How many minutes should the hand move when pressed. 1, 2, or 5 seem to be good.
- motorHr: What motor should be used for the Hour hand? Options are 'Motor1' or 'Motor2'
- motorMn: What motor should be used for the Minute hand? Options are 'Motor1' or 'Motor2'
- motor1Reverse: Wire the motor backwards? Reverse it with the options of 'true' or 'false'
- motor2Reverse: Wire the motor backwards? Reverse it with the options of 'true' or 'false'
- mqttEnable: Enable MQTT? This is for Node Red or other MQTT integration. Strings are sent in JSON format. Values are 'true' or 'false'
- mqttBrokerAddress: Enter the DNS or IP of the MQTT Broker.
- mqttTopicIn: Enter the MQTT Topic for packets into the app. Default is /pi/clock/in
- mqttTopicOut: Enter the MQTT Topic for packets out of the app. Default is /pi/clock/out
- buttonModePin: What pin should trigger the 'Mode' button? Default is 19.
- buttonHrFwPin: What pin should trigger the 'Hour Forward' button? Default is 12.
- buttonHrRvPin: What pin should trigger the 'Hour Reverse' button? Default is 16.
- buttonMnFwPin: What pin should trigger the 'Minute Forward' button? Default is 20.
- buttonMnRvPin: What pin should trigger the 'Minute Reverse' button? Default is 21.
- buttonModeType: What button type is used for the 'Mode' button? Options are 'normOpen' or 'normClose'.
- buttonHrFwType: What button type is used for the 'Hour Forward' button? Options are 'normOpen' or 'normClose'.
- buttonHrRvType: What button type is used for the 'Hour Reverse' button? Options are 'normOpen' or 'normClose'.
- buttonMnFwType: What button type is used for the 'Minute Forward' button? Options are 'normOpen' or 'normClose'.
- buttonMnRvType: What button type is used for the 'Minute Reverse' button? Options are 'normOpen' or 'normClose'.
- reset: Set this to 'true' to trigger a reset.
- unlock: Set this to 'true' to trigger the relay.

# Logs
Logs can be found at /home/pi/Escape-Room-Clock/logs
- Console - This is a general overview of what the app is doing, errors can be displayed here.
- Error - This only contains errors and crashes to help pinpoint time.
- Debug - This is very detailed logs as to what the app and all modutes are doing.
