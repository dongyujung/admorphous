"""
Processes the csv file for convenient use in generating simulated stream.

<Sorting>
Sorts the csv file according to timestamps
so that the stream is simulated in order.

<Time differences>
Read time differences between rows ahead to simulate stream with correct timing.

Needs to be run only once for initial setup.
"""

# Import packages
import sys
import pandas as pd

# Shell script input arguments
args = sys.argv

# There should be three input arguments:
# script, input file path, output file path
if len(args) == 3:
    input_file_path = args[1]
    output_file_path = args[2]
else:
    raise Exception('Need three input arguments.')

# Read file
df = pd.read_csv(input_file_path)

# Sorting
df = df.sort_values(by='timestamp').reset_index(drop=True)

# Read time difference ahead to simulate stream with correct timing
df['dt'] = -df['timestamp'].diff(periods=-1)

# Correct last row dt (which is NaN)
nrow, ncol = df.shape
df.loc[nrow-1,'dt'] = 0

df['dt'] = df['dt'].astype('int')

# Save file to csv
df.to_csv(output_file_path)