#!/bin/bash
# run_maps.sh

DATASET_DIR="/data/Twitter dataset"
mkdir -p logs

for file in "$DATASET_DIR"/geoTwitter20-*.zip; do
    echo "Launching mapper for $file"
    nohup python3 src/map.py --input_path "$file" --output_folder outputs > "logs/$(basename "$file").log" 2>&1 &
done

echo "All mapper processes have been launched."

