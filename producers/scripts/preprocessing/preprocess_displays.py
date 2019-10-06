"""
Preprocessing clicks table to extract display_id - ad_id mapping,
which is most likely mapped before the event or the click,
(they would have decided on the ad before displaying)
and saved into a table.
"""

# Import packages
import pandas as pd

input_file_path = '../../data/raw/clicks_train.csv'
output_file_path = '../../data/processed/display_ad.csv'

# Read file
df = pd.read_csv(input_file_path)

# Extract display-ad mapping
display_ad = df[['display_id', 'ad_id']]

# Save file to csv
display_ad.to_csv(output_file_path, index_label="daid")