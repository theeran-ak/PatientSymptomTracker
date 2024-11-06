'''---------------TO MODIFY THE PRECAUTION DATASET--------------'''
import pandas as pd
# load dataset
df = pd.read_csv('precaution_before.csv')
# Combine columns
df['Precaution'] = df[['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].apply(
    lambda x: [item for item in x if pd.notnull(item)], axis=1
)
final_df = df[['Disease', 'Precaution']]
final_df['Precaution'] = final_df['Precaution'].apply(lambda x: str(x).replace('\'', '')) # Convert the list to a string format 

print(final_df)

# save CSV file
final_df.to_csv('precaution_after.csv', index=False)

print("Data transformed and saved to 'transformed_precautions.csv'")
