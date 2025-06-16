# Data Preparation and Cleaning - Part 3

## Overview
This script performs data loading, cleaning, feature engineering, and imputation tasks on pharmaceutical sales and matching datasets. The goal is to prepare a refined and comprehensive dataset for further analysis or modeling.

## What the script does:
1. **Loads two datasets** (`full_match3` and `sales6`) from pickle files.
2. **Renames columns** for consistency.
3. **Sorts and removes duplicates** based on a unique identifier.
4. **Applies conditional logic** to categorize records into 'split' groups based on sales figures and invoice data.
5. **Cleans outliers** in specific numeric columns.
6. **Selects and reorders columns** for clarity and usability.
7. **Creates missing value indicators** for numeric variables.
8. **Calculates group-wise means** for numerical features by 'split' category.
9. **Imputes missing values** using these group means.
10. **Removes duplicate rows** and recalculates statistics.
11. **Merges datasets** and ensures a clean, sorted output ready for downstream analysis.

## Requirements
- Python 3.x
- pandas
- numpy

## Usage
1. Adjust file paths to your local environment.
2. Run the script to generate a cleaned and enriched DataFrame.
3. Use the output for further analysis or modeling steps.

---

**Note:**  
This code is designed for data preprocessing in a pharmaceutical sales context and emphasizes handling missing data and outliers effectively.
