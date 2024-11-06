'''---------------TO TRANSFORM THE SYMPTOMS DATASET INTO A FORMAT SUITABLE-------------------
----------------------------FOR TRAINING THE DECISION TREE-----------------------------------'''
import pandas as pd

# Load dataset
file_path = 'symptoms.csv' 
df = pd.read_csv(file_path)

# get unique symptoms
all_symptoms = set()
for col in df.columns[1:]:  #exclude disease column
    all_symptoms.update(df[col].dropna().str.strip())  # collect unique symptoms 
all_symptoms = sorted(all_symptoms) # Create a list of unique symptoms
# creation of a new dataframe with the symptoms as the column
output_data = []
for _, row in df.iterrows():
    disease = row['Disease']
    symptoms_present = row[1:].dropna().str.strip().tolist()  # Get symptoms for this row
    row_data = {symptom: 1 if symptom in symptoms_present else 0 for symptom in all_symptoms}
    row_data['disease'] = disease
    output_data.append(row_data)
output_df = pd.DataFrame(output_data)

# Save file
output_df.to_csv('training.csv', index=False)
print("Transformation complete. File saved as 'transformed_file.csv'.")
