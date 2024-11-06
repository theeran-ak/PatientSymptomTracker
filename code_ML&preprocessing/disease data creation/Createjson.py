'''---------------TO CREATE A JSON FILE CONTAINING THE CONTENT FOR RECOMMENDATIONS--------------'''
import pandas as pd
import json
import re

file_paths = ["description.csv", "precaution_after.csv", "workout_after.csv"] # list of file paths

# Load all CSV files into separate DataFrames, each indexed by the 'Disease' column
dfs = []
for file in file_paths:
    df = pd.read_csv(file)
    print(f"Columns in {file}: {df.columns.tolist()}")
    df.columns = df.columns.str.strip() # strip whitespace 

    if 'Disease' not in df.columns:
        raise KeyError(f"'Disease' column not found in {file}. Available columns: {df.columns.tolist()}")

    # handling files according to their formats
    if file == "description.csv":
        df['Description'] = df['Description'].astype(str)
        dfs.append(df.set_index("Disease"))
    elif file == "precaution_after.csv":
        df['Precaution'] = df['Precaution'].apply(lambda x: [item.strip(' []') for item in re.split(r',\s*', x.strip(' []')) if item.strip()] if isinstance(x, str) else [])
        dfs.append(df.set_index("Disease"))
    elif file == "workout_after.csv":
        df['Recommendation'] = df['Recommendation'].apply(lambda x: [item.strip(' []') for item in re.split(r',\s*', x.strip(' []')) if item.strip()] if isinstance(x, str) else [])
        dfs.append(df.set_index("Disease"))

combined_df = pd.concat(dfs, axis=1, join="outer") # merge all DataFrames on 'Disease'
combined_df = combined_df.reset_index() # reset the index to make 'Disease' a column again
combined_df.columns = ['Disease', 'Description', 'Precaution', 'Workout'] 
combined_json = combined_df.to_dict(orient="records") # convert dataframe to JSON format

current_json =combined_json

# Transform the JSON structure
transformed_json = {
    entry["Disease"]: {
        "Description": entry["Description"],
        "Precaution": entry["Precaution"],
        "Workout": entry["Workout"]
    } for entry in current_json
}

print(json.dumps(transformed_json, indent=4))

# save the transformed JSON to a file
with open("disease_data.json", "w") as json_file:
    json.dump(transformed_json, json_file, indent=4)

print("Data transformed and saved to 'disease_data.json'")
