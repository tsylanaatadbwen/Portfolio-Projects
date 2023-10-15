# Data Analysis of Weather Dataset

This repository contains the documentation and data analysis of the Weather Dataset from Szeged, Hungary, covering the years 2006-2016. The project aims to showcase statistical analysis, hypothesis testing, and regression analysis skills.

## Sample Size Calculation

In the "Sample Size" section:
- Calculated the sample size required for the population temperature column based on standard deviation, margin of error, and confidence level.
- Performed data cleaning by removing unnecessary columns.
- Extracted a random sample of 35046 rows using Excel's RAND() function.
- Sorted the data based on random numbers for further analysis.

## Statistical Distributions

In the "Statistical Distribution" section:
### Question 1
- Calculated the sample mean and sample standard deviation of the temperature.
- Performed a two-tail test and determined the probability using NORM.DIST().
- Drew a conclusion based on the calculated probability.

### Question 2
- Utilized NORM.INV() to calculate values from the probability density function for Normal Distribution.
- Concluded the results of the analysis.

### Question 3
- Applied BINOM.DIST() to calculate the probability of a specific number of successful events.
- Summarized the findings.

### Question 4
- Utilized POISSON.DIST() to calculate the number of events in a fixed time interval.
- Presented the results of the analysis.

## Confidence Interval

- Calculated a confidence interval for the population sample using the t distribution.
- Determined alpha using NORM.INV() and computed the margin of error.
- Concluded the confidence interval for the sample data.

## Hypothesis Testing

### Population Mean Hypothesis
- Assumed the null hypothesis and calculated the sample mean and sample standard deviation.
- Computed the t-statistic and identified the rejection region using T.INV.
- Concluded whether to reject the null hypothesis or not.

### Difference in Mean Hypothesis
- Assumed that the means are equal and used equal variance in Excel's Data Analysis tools.
- Concluded the results.

## Regression Analysis

- Sampled data for dependent and independent variables.
- Created a scatter plot with a regression line to assess linearity.
- Built a regression model in line with the business application.
- Utilized Excel's Data Analysis tool to generate regression statistics.
- Interpreted the relationship between variables in the inference section.
- Checked the goodness of fit using the Adjusted-R.
- Conducted hypothesis testing for regression variables based on the provided statistics.
- Assessed multicollinearity using Excel's Data Analysis tools.
- Made predictions in line with the provided scenario and calculated prediction intervals.
- Drew conclusions based on the analysis results and ensured sheet formatting for clarity.

For a detailed view of the project and to access the Excel workbook, please download it from the provided link [here](https://github.com/tsylanaatadbwen/Portfolio-Projects/blob/main/Statistics%20%26%20Regression%20Analysis%20Excel/Regression_Proj.xlsx)

## License

- Dataset source: [Weather in Szeged 2006-2016](https://www.kaggle.com/datasets/budincsevity/szeged-weather)
