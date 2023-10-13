# UFC Rankings Data Analysis

## Overview

This Python project focuses on analyzing UFC (Ultimate Fighting Championship) rankings data. The dataset provides insights into fighter rankings, title reigns, and visualizations of UFC fighters' rankings over time. The primary purpose of this project is to showcase the author's proficiency in using the Pandas library to solve data analysis problems encountered during the analysis.

## Data Source

The data used for this analysis was obtained from Kaggle through the Kaggle API. You can download the dataset [here](https://www.kaggle.com/martj42/ufc-rankings).

## Code

The Python code used for this analysis can be found in the Jupyter Notebook provided as [`ufc_rankings_analysis.ipynb`](link to your Jupyter Notebook).

## Project Steps

### Data Retrieval
The project begins with the retrieval of UFC rankings data using the Kaggle API. The dataset is downloaded as a zip file and extracted for analysis.

### Data Exploration
- Obtaining a big picture view of the data by checking its info, shape, and data types.
- Converting column data types, including converting the "weightclass" column to a category for memory optimization.
- Converting the "date" column from a string to a datetime data type.

### Data Manipulation
- Grouping the data by fighter and weight class using the `groupby` function.
- Sorting the data by date within each group using the `apply` function and a lambda function.
- Addressing inaccuracies in the data related to "Pound-for-Pound" rankings and "Men's Pound-for-Pound" rankings.

### Data Visualization
- Creating visualizations of title reigns for four UFC fighters: Islam Makhachev, Alexander Volkanovski, Sean O'Malley, and Israel Adesanya.
- Identifying the longest-reigning champion in the UFC and calculating the duration of their reign.

### P4P Rankings
- Loading Pound-for-Pound (P4P) rankings data from a CSV file.
- Visualizing Jon Jones' P4P rankings over the years.

## Results

The analysis provides insights into UFC fighter rankings, title reigns, and the P4P rankings of Jon Jones. The visualizations help visualize the changes in fighter rankings over time and identify the longest-reigning champion in the UFC.

For detailed code and step-by-step explanations, please refer to the [Jupyter Notebook](https://github.com/tsylanaatadbwen/Portfolio-Projects/blob/main/Python%20Pandas/UFC_Ranking_Project.ipynb) in the project repository.
