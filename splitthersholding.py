import pandas as pd

# Load the Excel file
file_path = r'files/Final_RTQ_Binary_Vertical.xlsx'
df = pd.read_excel(file_path)

# Split the dataframe and rename the columns
df_Alice = df[['Binary_DOSS1']].rename(columns={'Binary_DOSS1': 'Alice'})
df_Bob = df[['Binary_DOSS2']].rename(columns={'Binary_DOSS2': 'Bob'})
df_Charlie = df[['Binary_DOSS3']].rename(columns={'Binary_DOSS3': 'Charlie'})

# Save the DataFrames to new Excel files in .xls format
df_Alice.to_excel(r'files/Threshold_Alice.xlsx', index=False)
df_Bob.to_excel(r'files/Threshold_Bob.xlsx', index=False)
df_Charlie.to_excel(r'files/Threshold_Charlie.xlsx', index=False)

print("Files have been saved successfully.")
