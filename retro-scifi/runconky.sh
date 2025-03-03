#!/bin/bash

# Kill any running conky instances
killall conky

# Wait a moment
sleep 1

# Start the main conky
conky -c ~/.conky/.conkyrc &

# Start the date/time conky
conky -c ~/.conky/.dateconkyrc &
