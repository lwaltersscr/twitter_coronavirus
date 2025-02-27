#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--hashtags',nargs='+',required=True)
args = parser.parse_args()

# imports
import argparse
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

def parse_day_from_filename(filename):
    """
    Extracts the day of the year from a filename.
    Expects a filename like "geoTwitter20-01-01.zip.lang"
    """
    base = os.path.basename(filename)
    if base.startswith("geoTwitter"):
        base = base[len("geoTwitter"):]
    # Expect something like "20-01-01.zip.lang"
    parts = base.split(".zip")
    if not parts or len(parts[0]) != 8:  # e.g., "20-01-01"
        return None
    date_str = parts[0]
    try:
        dt = datetime.strptime(date_str, "%y-%m-%d")
        return dt.timetuple().tm_yday
    except Exception as e:
        print("Error parsing date from filename:", filename, e)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Alternative reducer: plot daily tweet counts for given hashtags"
    )
    # Accept one or more hashtags
    parser.add_argument("hashtags", nargs="+", help="List of hashtags to plot")
    parser.add_argument(
        "--outputs_folder",
        default="outputs",
        help="Folder containing mapper output files (default: outputs)",
    )
    parser.add_argument(
        "--output_png",
        default="alternative_reduce.png",
        help="Filename for the output plot (default: alternative_reduce.png)",
    )
    args = parser.parse_args()

    # Initialize data structure: for each hashtag, store day -> count
    hashtag_data = {hashtag: {} for hashtag in args.hashtags}

    # Loop through files in the outputs folder that end with ".lang"
    for filename in os.listdir(args.outputs_folder):
        if not filename.endswith(".lang"):
            continue
        filepath = os.path.join(args.outputs_folder, filename)
        day = parse_day_from_filename(filename)
        if day is None:
            continue

        # Load the JSON data from the mapper output
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue

        # For each specified hashtag, get the count (summing over all languages)
        for hashtag in args.hashtags:
            count = 0
            if hashtag in data:
                # data[hashtag] is a dictionary like { "en": count, "es": count, ... }
                for lang, c in data[hashtag].items():
                    count += c
            # Record the count for this day; if no tweets, count is zero
            hashtag_data[hashtag][day] = count

    # Create the plot
    plt.figure(figsize=(10, 6))
    for hashtag, day_counts in hashtag_data.items():
        # Sort by day-of-year
        days = sorted(day_counts.keys())
        counts = [day_counts[d] for d in days]
        plt.plot(days, counts, marker="o", label=hashtag)

    plt.xlabel("Day of the Year")
    plt.ylabel("Tweet Count")
    plt.title("Daily Tweet Counts for Specified Hashtags")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.output_png)
    print("Plot saved to", args.output_png)

if __name__ == "__main__":
    main()
