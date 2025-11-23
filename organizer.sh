#!/bin/bash

DIR="./archive"
# checking if derectory exists or not
mkdir -p "$DIR"

# Now checking if there is any csv file availabel
csv_files=( *.csv )

if [ ! -e "${csv_files[0]}" ]; then
    echo "No CSV files found."
    exit 1
fi

for file in "${csv_files[@]}"; do
    timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    new_file="grade-${timestamp}.csv"

    # Apennding the fiels in to organizer now
    {
        echo "Archiving Details: $file"
        echo "Time Archived: $timestamp"
        echo "New File Name: $new_file"
        echo "Content:"
        cat "$file"
        echo ""
    } >> "organizer.log"

  
    mv "$file" "$DIR/$new_file"
done
