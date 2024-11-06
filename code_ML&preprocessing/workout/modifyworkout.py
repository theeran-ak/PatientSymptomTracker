'''-------------------TO MODIFY THE WORKOUT DATASET----------------------'''
import pandas as pd
df = pd.read_csv('workout_before.csv')# load dataset
df.columns = df.columns.str.strip()# remove whitespace
grouped_df = df.groupby('Disease')['Recommendation'].apply(lambda x: list(x)).reset_index()# group recommendations into list
grouped_df['Recommendation'] = grouped_df['Recommendation'].apply(lambda x: str(x).replace('\'', '')) # convert to string
grouped_df.to_csv('workout_after.csv', index=False)# Save file
print("Data combined and saved to 'output_recommendations.csv'")
