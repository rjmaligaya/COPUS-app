import pandas as pd

# Define the structure of the COPUS template with appropriate columns
columns = [
    'Minute',
    'Students_Activity1', 'Students_Activity2', 'Students_Activity3',
    'Students_Activity4', 'Students_Activity5', 'Students_Activity6',
    'Students_Activity7', 'Students_Activity8', 'Students_Activity9',
    'Professor_Activity1', 'Professor_Activity2', 'Professor_Activity3',
    'Professor_Activity4', 'Professor_Activity5', 'Professor_Activity6',
    'Professor_Activity7', 'Professor_Activity8',
    'Engagement', 'Comments'
]

# Create an empty DataFrame with these columns
template_df = pd.DataFrame(columns=columns)

# Save this DataFrame to an Excel file
template_df.to_excel('COPUS_template.xlsx', index=False)
