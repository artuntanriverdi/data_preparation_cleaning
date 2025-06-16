import pandas as pd
import os

input_path_full_match3='C:\\Users\\gremotti\\Gmr S.r.L\\GMR-Progetti - Documenti\\2211-11 ClonazioneFarmacie\\PerPython\\savedtable\\full_match3.pkl'
input_path_sales6='C:\\Users\\gremotti\\Gmr S.r.L\\GMR-Progetti - Documenti\\2211-11 ClonazioneFarmacie\\sales6.pkl'

# Load the DataFrame
full_match3 = pd.read_pickle(input_path_full_match3)  # Use .read_csv() or .read_excel() if needed
print("DataFrame loaded successfully.")

# Load the DataFrame
sales6 = pd.read_pickle(input_path_sales6)  # Use .read_csv() or .read_excel() if needed
print("DataFrame loaded successfully.")

sales6.rename(columns={
    'pdf_phy_id': 'minsal_phy_id',

}, inplace=True)

df=full_match3
# Ensure the data is sorted by 'phy_id'
df = df.sort_values(by='minsal_phy_id')

# Drop duplicate rows keeping the first occurrence for each 'phy_id'
df = df.drop_duplicates(subset='minsal_phy_id', keep='first')

df['split'] = df['nfatturato']

# Apply split logic
def apply_split(row):
    if pd.isna(row['split']) or row['split'] in [4]:
        if pd.isna(row['mmas_fatt']):
            return 42
        elif row['mmas_fatt'] < 860000:
            return 41
        elif row['mmas_fatt'] < 1370000:
            return 42
        elif row['mmas_fatt'] < 2000000:
            return 43
        else:
            return 44
    return row['split']

df['split'] = df.apply(apply_split, axis=1)

# Outlier cleaning for 'ssn_qta'
df.loc[df['ssn_qta'] > 300000, 'ssn_qta'] = np.nan

# Keep only specified columns
# Replace &varnum and &varch with actual column names if needed

# Define the new order of columns
new_order = [
    "minsal_phy_id","ssn_qta", "mmas_fatt", "COMUNE_x", "PROVINCIA", "REGIONE", "nfatturato", "Addetti",
    "Mq", "Mq_Magazzino", "Vetrine", "Laureati", "Catena", "Zona_altimetrica", "Altitudine_centro",
    "Comune_litoraneo", "Comune_Montano", "Superficie", "Urbanizzazione", "first_mese", "split"
]

# Reorder the columns of the filtered DataFrame
prepare_1 = df[new_order]

# Count the occurrences of each unique value in the 'split' column
split_counts = prepare_1['split'].value_counts()

# Define the numeric columns
varnum = [
    "Addetti", "Mq", "Mq_Magazzino", "Laureati",
    "Vetrine", "Zona_altimetrica", "Altitudine_centro",
    "Comune_litoraneo", "Superficie", "Urbanizzazione",
    "nfatturato", "mmas_fatt"
]

# Create a copy of prepare_1 for prepare_2
prepare_2 = prepare_1.copy()

# Create new columns to indicate missing values
for col in varnum:
    prepare_2[f'{col}_missing'] = prepare_2[col].isna().astype(int)

# Calculate means by 'split'
means_by_split = prepare_2.groupby('split')[varnum].mean().reset_index()

# Replace NaN values in prepare_2 with the mean values from means_by_split
for col in varnum:
    prepare_2[col] = prepare_2.apply(
        lambda row: means_by_split.loc[means_by_split['split'] == row['split'], col].values[0]
        if pd.isna(row[col]) else row[col], axis=1
    )

# Add mean columns to the DataFrame
for col in varnum:
    prepare_2[f'{col}_mean'] = prepare_2.groupby('split')[col].transform('mean')

# Recalculate missing value indicators after replacing NaNs
for col in varnum:
    prepare_2[f'{col}_missing'] = prepare_2[col].isna().astype(int)

# Ensure that the DataFrame is sorted by 'minsal_phy_id'
prepare_2 = prepare_2.sort_values(by='minsal_phy_id')


# Group by 'split'
grouped = prepare_2.groupby('split')

# Identify numeric columns
numeric_columns = prepare_2.select_dtypes(include=np.number).columns.tolist()

# Create a copy of the DataFrame to store the result
prepare_3 = prepare_2.copy()

# Fill missing values in numeric columns with the mean of their respective groups
for col in numeric_columns:
    # Calculate the means by group for the column
    means = grouped[col].transform('mean')

    # Fill missing values with the means
    prepare_3[col] = prepare_3[col].fillna(means)

means_by_group = grouped[numeric_columns].mean()

# Number of rows before removing duplicates
num_rows_before = len(prepare_3)

# Identify and remove duplicate rows
prepare_3_no_duplicates = prepare_3.drop_duplicates()

# Number of rows after removing duplicates
num_rows_after = len(prepare_3_no_duplicates)

# Recalculate the mean values after removing duplicates
mean_values = {}
for column in numeric_columns:
    if column in prepare_3_no_duplicates.columns:
        # Count all entries, including NaNs
        total_count = len(prepare_3_no_duplicates[column])

        # Sum the values, treating NaNs as 0
        total_sum = prepare_3_no_duplicates[column].sum()

        # Calculate the mean value by dividing the sum by the total count
        mean_value = total_sum / total_count if total_count != 0 else np.nan

        # Store the mean value in the dictionary
        mean_values[column] = mean_value



# Impute missing values with the recalculated mean for each numeric column
for column in numeric_columns:
    if column in prepare_3_no_duplicates.columns:
        prepare_3_no_duplicates[column].fillna(mean_values[column], inplace=True)

# Sort the DataFrame by the 'split' column
prepare_3= prepare_3_no_duplicates.sort_values(by='split').reset_index(drop=True)

# Merge prepare_2 and prepare_3 on 'split'
merged_df = pd.merge(prepare_2, prepare_3, on='split', how='left')

# Sort the resulting DataFrame by 'minsal_phy_id'
prepare_3 = merged_df.sort_values(by='minsal_phy_id')


