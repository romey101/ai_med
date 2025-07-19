import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('covid.csv', header=1)

# Select relevant columns
df = df[['date', 'country', 'total_cases', 'new_cases','total_deaths', 'total_vaccinations', 'positive_rate']]

# Set the date column as index
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Filter for Saudi Arabia up to 2023-12-31
df_saudi = df[df['country'] == 'Saudi Arabia'].loc[:'2023-12-31']

# Drop the country column
df_saudi = df_saudi.drop(columns='country')

# Fill the first few rows with zero for total_cases, new_cases and total_deaths
df_saudi['total_cases'] = df_saudi['total_cases'].fillna(0)
df_saudi['new_cases'] = df_saudi['new_cases'].fillna(0)
df_saudi['total_deaths'] = df_saudi['total_deaths'].fillna(0)

# For total_vaccinations, fill the rows for dates when vaccinations weren't available with zero
df_saudi.loc[:'2021-01-05', 'total_vaccinations'] = df_saudi.loc[:'2021-01-05', 'total_vaccinations'].fillna(0)
df_saudi.loc['2021-01-05':'2022-02-28', 'total_vaccinations'] = df_saudi.loc['2021-01-05':'2022-02-28',\
                                                                             'total_vaccinations'].fillna(method='ffill')
# Handle known anomaly
df_saudi.loc['2023-04-25', 'total_vaccinations'] = np.nan

print(df_saudi)

# Descriptive statistics
df_saudi.describe()

# Cumulative cases for each three month period
total_cases_three_months = df_saudi['total_cases'].resample('3M').last().to_frame()
print(total_cases_three_months)

# Sum of new cases for each three months
new_cases_three_months = df_saudi['new_cases'].resample('3M').sum().to_frame()
print(new_cases_three_months)

# Cumulative cases for each year
cumulative_total_cases_per_year = df_saudi['total_cases'].resample('Y').last().to_frame()
(cumulative_total_cases_per_year)

# Total cases per year
new_cases_per_year = df_saudi['new_cases'].resample('Y').sum().to_frame()
print(new_cases_per_year)

# Average positive rate for each year
avg_yearly_positive_rate = df_saudi['positive_rate'].resample('Y').mean().to_frame()
print(avg_yearly_positive_rate)

# Total cases at the end of 2023
final_total_cases = df_saudi['total_cases'].max()
print(f'Total COVID-19 cases at the end of 2023: {final_total_cases}')

# Total deaths at the end of 2023
final_total_deaths = df_saudi['total_deaths'].max()
print(f'Total COVID-19 related deaths at the end of 2023: {final_total_deaths}')

# Total vaccinations at the end of 2023
final_total_vaccinations = df_saudi['total_vaccinations'].max()
print(f'Total vaccinations at the end of 2023: {final_total_vaccinations}')

# Case fatality rate:
cfr = final_total_deaths / final_total_cases
print(f'COVID-19 death-to-case ratio in Saudi Arabia: {cfr:.1%}')