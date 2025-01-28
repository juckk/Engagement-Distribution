import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = "/Users/juck/Downloads/Zocial Metric Business - Calculate Sheet 2024 (RapidMiner).xlsx"

# Read the Excel file
data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets

sheet_lists = list(data.keys())
# Print the contents of the Excel file
print("\nAvailable Sheets:", sheet_lists)

sheet1 = data['facebook_stat']
sheet2 = data['twitter_stat']

sheet1 = pd.DataFrame(sheet1)
sheet2 = pd.DataFrame(sheet2)

# Merging with suffixes to differentiate columns from both DataFrames
if 'id' in sheet1.columns and 'id' in sheet2.columns:
    merged_data = pd.merge(sheet1, sheet2, on='id', how='inner')
    print("\nMerged Data:")
    print(merged_data)
    merged_data['Engagement'] = merged_data['Engagement Count_x'] + merged_data['Engagement Count_y']
else:
    print("One or both sheets do not contain the 'id' column.")


# Group by 'id' and sum 'Engagement'
if 'id' in merged_data.columns and 'Engagement' in merged_data.columns:
    group_brand = merged_data.groupby('id', as_index=False).agg({
        'Engagement': 'sum',
        'Account Name_x': 'first'
    })
    print("Grouped data by 'id':")
    print(group_brand)
else:
    print("The necessary columns for grouping ('id' and 'Engagement') are missing in the sheet.")
    print(merged_data.columns)

# Applying Freedman-Diaconis Rule to determine bin width and bins
def freedman_diaconis_bins(data):
    q75, q25 = np.percentile(data, [75 ,25])  # Find 75th and 25th percentiles
    iqr = q75 - q25  # Interquartile Range (IQR)
    bin_width = 2 * iqr / len(data) ** (1/3)  # Freedman-Diaconis bin width
    range_of_data = data.max() - data.min()
    n_bins = int(np.ceil(range_of_data / bin_width))  # Number of bins
    return n_bins

# Get the number of bins using Freedman-Diaconis rule
n_bins_fd = freedman_diaconis_bins(group_brand['Engagement'])
print("Recommended number of bins based on Freedman-Diaconis rule:", n_bins_fd)

# Create a frequency table based on bins
bins_fd = np.histogram_bin_edges(group_brand['Engagement'], bins=n_bins_fd)
print("Bins based on Freedman-Diaconis rule:", bins_fd)

# Plotting the Histogram of Engagement using the optimal bins from Freedman-Diaconis Rule
plt.figure(figsize=(10, 6))  # Set the size of the figure
sns.histplot(group_brand['Engagement'], kde=True, color='blue', bins=bins_fd)  # Plot with optimal bins

plt.title('Engagement Distribution (Freedman-Diaconis Bins)')  # Title for the chart
plt.xlabel('Engagement')             # X-axis label
plt.ylabel('Frequency')              # Y-axis label
# plt.ylim(0, 70)                      # Adjust y-axis limits

# Show the plot
plt.show()