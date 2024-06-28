#!/bin/bash

setup_cron_job() {
    read -p "Do you want to set up a cron job? (yes/no): " cron_choice
    if [[ "$cron_choice" == "yes" ]]; then
        # Get the directory of the current script
        script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        script_path="$script_dir/air_quality.py"
        
        if [[ ! -f "$script_path" ]]; then
            echo "The Python script 'air_quality.py' does not exist in the same directory as this shell script."
            exit 1
        fi
        
        read -p "At what time do you want to run the script daily? (HH:MM format): " cron_time
        cron_hour=$(echo "$cron_time" | cut -d':' -f1)
        cron_minute=$(echo "$cron_time" | cut -d':' -f2)
        
        # Validate time input
        if ! [[ "$cron_hour" =~ ^[0-9]{1,2}$ ]] || ! [[ "$cron_minute" =~ ^[0-9]{1,2}$ ]] || [ "$cron_hour" -lt 0 ] || [ "$cron_hour" -gt 23 ] || [ "$cron_minute" -lt 0 ] || [ "$cron_minute" -gt 59 ]; then
            echo "Invalid time format. Please enter time in HH:MM format."
            exit 1
        fi

        # Add cron job
        (crontab -l 2>/dev/null; echo "$cron_minute $cron_hour * * * /usr/bin/python3 $script_path") | crontab -
        echo "Cron job set to run daily at $cron_time"
    else
        echo "Cron job setup skipped."
    fi
}

setup_cron_job
