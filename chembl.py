import pandas as pd
from chembl_webresource_client.new_client import new_client

# Search for coronavirus-related targets
target = new_client.target
target_query = target.search('coronavirus')
targets = pd.DataFrame.from_dict(target_query)

# Select a specific target
selected_target = targets.target_chembl_id[4]

# Retrieve bioactivity data for the selected target based on IC50 values
activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")

# Convert the results to a DataFrame
df = pd.DataFrame.from_dict(res)

# Save the raw bioactivity data to a CSV file
df.to_csv('bioactivity_data_raw.csv', index=False)

# Filter out rows with missing standard_value
df2 = df[df.standard_value.notna()].copy()

# Select relevant columns
selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
df3 = df2.loc[:, selection].copy()  # Use .loc to select columns and create a copy

# Classify bioactivity based on standard_value
bioactivity_class = []
for value in df3['standard_value'].astype(float):
    if value >= 10000:
        bioactivity_class.append("inactive")
    elif value <= 1000:
        bioactivity_class.append("active")
    else:
        bioactivity_class.append("intermediate")  # Optional: include intermediate

# Add bioactivity class to the DataFrame using .loc
df3.loc[:, 'bioactivity_class'] = bioactivity_class

# Save the preprocessed bioactivity data to a CSV file
df3.to_csv('bioactivity_data_preprocessed.csv', index=False)

# Display the first few rows of the preprocessed data
print(df3.head(3))
