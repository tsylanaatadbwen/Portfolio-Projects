# Top Rated Movies Data Analysis

## Overview

This project involves the exploratory data analysis of a dataset containing information about top-rated movies. The analysis focuses on data cleaning, visualizations, and findings derived from the dataset to gain insights into the movies' popularity, ratings, and temporal trends.

## Data Cleaning

In the data cleaning process, the following steps were taken:

- Removed duplicates from the dataset.
- Eliminated the first column without a header (index/serial).
- Ensured consistency and data integrity by converting numerical columns to numeric data types and date columns to date data types.
- Handled missing values in the "overview" column by replacing blank cells with "N/A."
- Improved consistency in string values in the "title" and "overview" columns using TRIM() and PROPER() functions.

## Visualizations

The project includes various visualizations to better understand the dataset.

1. **Popularity Histogram**: A histogram displaying the distribution of popularity scores in the dataset. It reveals a notable concentration of movies with high popularity scores.

2. **Popularity TimeSeries**: A time series line graph showing the trend of movie popularity over time. It indicates a recent surge in popularity and intermittent spikes.

3. **Vote_Average Box Plot**: A box plot illustrating the distribution of movie ratings, including central tendency, spread, and variability.

4. **Ratings & Votes Scatterplot**: A scatter plot analyzing the correlation between vote counts and movie ratings. It reveals a positive but relatively weak relationship between the two variables.

## Findings

The data analysis led to the following key findings:

**Popularity Histogram**:
- The majority of movies in the dataset have popularity scores ranging from 7 to 20.
- A notable concentration of approximately 150 movies has a popularity score around 200.
- The distribution of movie popularity is right-skewed, with the mean popularity score greater than the median.

**Popularity TimeSeries**:
- Recent movies experienced a substantial and prolonged surge in popularity.
- Intermittent spikes in popularity correspond to specific movie release dates.
- Recent movies dominate the dataset, suggesting higher popularity for recent releases.

**Vote_Average Box Plot**:
- Most movies receive ratings clustered around 6.7 to 6.8.
- Movie ratings in the dataset range from 5.7 to 8.7, demonstrating diversity in ratings.
- The interquartile range (IQR) is relatively narrow, emphasizing consistency in ratings.

**Ratings & Votes Scatterplot**:
- There is a positive correlation between vote counts and movie ratings (0.2592).
- The correlation is relatively weak, indicating a mild positive relationship.
- Low vote counts are concentrated in the dataset, while higher vote counts exhibit a wider range of ratings.

These insights offer a better understanding of movie popularity, ratings, and the relationship between votes and ratings within the dataset.

## Project Directory

The project directory includes images of the visualizations. To check the project in Excel in detail, download it from [here](https://github.com/tsylanaatadbwen/Portfolio-Projects/blob/main/Excel/MoviesTopRated.xlsx)

## Acknowledgments

- Dataset source: [Top Rated Movies](https://www.kaggle.com/datasets/khalidalam980/top-rated-movies-data-set)
