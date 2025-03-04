#!/bin/bash

# Kill any running conky instances
killall conky

# Wait a moment
sleep 1

# Start the main conky
conky -c /home/nick/repos/personal/conky-themes/retro-scifi/.dateconkyrc &

# Start the date/time conky
conky -c /home/nick/repos/personal/conky-themes/retro-scifi/.conkyrc &

# Start CPU Conky
conky -c /home/nick/repos/personal/conky-themes/retro-scifi/.cpuconkyrc &
