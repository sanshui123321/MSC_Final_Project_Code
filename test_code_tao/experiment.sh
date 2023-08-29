#!/bin/bash

# Setting up variables
REFERENCE_IMAGE="/home/tao/test_code_tao/screenshot/google_nest.png" # Reference image
Para_file="/home/tao/test_code_tao/google_nest.txt" # File containing the parameters
experiment_name='google_nest' #slect from 'furbo','google_nest','withings','blink'
repeat_times=50

RESULT_FILE="/home/tao/test_code_tao/${experiment_name}_results.txt" # File for recording the results
PHONE="pixel3a" # The phone  ids/phone
SCREENSHOT_DIR="/home/tao/test_code_tao/screenshot" # Directory for screenshots
TRAFFIC_DIR="/home/tao/test_code_tao/traffic_pcap" # File for saving pcap file


# Create screenshot directory if it does not exist
mkdir -p "$SCREENSHOT_DIR"

# Function to wait for the phone to be ready
function waitphone {
    while [ -z "$PHONE_FOUND" ]; do
        echo "Phone not found, waiting for $PHONE/$ANDROID_SERIAL"
        sleep 5
        PHONE_FOUND=$(adb devices | grep "$ANDROID_SERIAL")
    done
}


# Check if the phone's id file exists
if [ ! -f "ids/$PHONE" ]; then
    echo "Devices ids/$PHONE does not exist. Aborting."
    exit 1
else
    # If it exists, get the phone's ID
    export ANDROID_SERIAL=$(cat "ids/$PHONE")
    echo "Phone is: $PHONE/$ANDROID_SERIAL"
    PHONE_FOUND=$(adb devices | grep "$ANDROID_SERIAL" | grep device)
    waitphone
    echo "Phone ready, proceeding..."
fi

# Wake up and unlocked the phone
adb shell input keyevent KEYCODE_WAKEUP
sleep 1
adb shell input swipe 560 1828 560 1000 1000
sleep 1

# Main loop
for ((i=0; i<repeat_times; i++)); do
    echo "Experiment $((i+1))"

    # Get the current date and time for each iteration
    DATE=$(date "+%m%d_%H%M%S") # The current date and time

    # Read the parameters from the file
    echo "Reading parameters from the file..."

    # Read the content of the file into the PARAMETERS variable
    PARAMETERS=$(<"$Para_file")

    # Split the PARAMETERS variable into an array by the semicolon delimiter
    IFS=';' read -ra PARAMS <<< "$PARAMETERS"

    # Assigning parameters to variables
    package=${PARAMS[0]}
    mac_address=${PARAMS[1]}
    crop_info=${PARAMS[2]}
    functions=("${PARAMS[@]:3}")

    # Start the monitor
    cd /opt/moniotr
    /opt/moniotr/bin/tag-experiment.sh start "$mac_address" "$experiment_name"
    sleep 5

    # Close app before opening it
    adb shell am force-stop "$package"
    sleep 1
    # Return to home screen
    adb shell input keyevent KEYCODE_HOME
    sleep 5

    # Launch the app
    adb shell -n monkey -p "$package" -c android.intent.category.LAUNCHER 1
    sleep 10

    # Execute the operations if they are set
    for function in "${functions[@]}"; do
        if [ -n "$function" ]; then
            waitphone
            adb shell -n input "$function"
            sleep 10
        fi
    done

    echo "The experimental operations have finished, taking a screenshot…"

    # Stop the monitor
    /opt/moniotr/bin/tag-experiment.sh stop "$mac_address" "$experiment_name" "$TRAFFIC_DIR"
    sleep 5

    # Take a screenshot and save it in the screenshot directory
    waitphone
    adb shell screencap -p /sdcard/screen.png
    adb pull /sdcard/screen.png "$SCREENSHOT_DIR/full_screen.png"
    adb shell rm /sdcard/screen.png

    # Create a unique file name for the screenshot
    SCREENSHOT_FILE="${experiment_name}_${DATE}.png"

    # Crop the screenshot according to the crop_info
    convert "$SCREENSHOT_DIR/full_screen.png" -crop "$crop_info" "$SCREENSHOT_DIR/$SCREENSHOT_FILE"
    rm "$SCREENSHOT_DIR/full_screen.png"

    # Compare the screenshot with the reference image
    compare_result=$(python3 /home/tao/test_code_tao/compare_images.py "$SCREENSHOT_DIR/$SCREENSHOT_FILE" "$REFERENCE_IMAGE")

    # Output the result of the comparison
    if [ "$compare_result" -eq 0 ]; then
        result_msg="Failure"
        echo "Experiment $((i+1)) is failure."
    else
        result_msg="Successful"
        echo "Experiment $((i+1)) is successful."
    fi

    # Save the result to the file
    echo -e "Experiment: $((i+1)), Date: $DATE, Result: $result_msg" >> "$RESULT_FILE"

    echo "Experiment $((i+1)) completed."
    echo
done

exit 0
