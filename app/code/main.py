import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

# If you have saved a local copy of the CSV file as LOCAL_CSV_FILE,
# set READ_FROM_URL to True
READ_FROM_URL = True
LOCAL_CSV_FILE = 'covid-19-cases.csv'

# Start the plot on the day when the number of confirmed cases reaches MIN_CASES.
MIN_CASES = 100

# The country to plot the data for.
country = 'Germany'

# This is the GitHub URL for the Johns Hopkins data in CSV format
data_loc = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'
            'csse_covid_19_data/csse_covid_19_time_series'
            '/time_series_covid19_confirmed_global.csv')

# Read in the data to a pandas DataFrame.
if not READ_FROM_URL:
    data_loc = LOCAL_CSV_FILE
df = pd.read_csv(data_loc)

# Group by country and sum over the different states/regions of each country.
grouped = df.groupby('Country/Region')
df2 = grouped.sum()

def make_plot(country):
    """Make different plots for case numbers, cumulative cases, and mortality rate."""

    # Extract the Series corresponding to the case numbers for the country.
    c_df = df2.loc[country, df2.columns[3:]]
    print(c_df)
    # Discard any columns with fewer than MIN_CASES.
    c_df = c_df[c_df >= MIN_CASES].astype(int)
    # Convert the index to a proper datetime object.
    c_df.index = pd.to_datetime(c_df.index)
    n = len(c_df)
    if n == 0:
        print('Too few data to plot: minimum number of cases is {}'
              .format(MIN_CASES))
        sys.exit(1)

    # Merge deaths and cumulative cases dataframes based on the common date index.
    deaths_df = df.groupby('Country/Region').sum().loc[country, df.columns[3:]]
    combined_df = pd.merge(c_df, deaths_df, left_index=True, right_index=True, suffixes=('_confirmed', '_deaths'))

    # Print column names for debugging.
    print("Column names in combined_df:", combined_df.columns)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Plot 1: Total confirmed cases.
    axs[0].plot(c_df.index, c_df.values, label='Total Confirmed Cases', color='blue')
    axs[0].set_ylabel('Confirmed cases, $N$')
    axs[0].legend()

    # Plot 2: Cumulative cases.
    cumulative_cases = c_df.cumsum()
    axs[1].plot(c_df.index, cumulative_cases.values, label='Cumulative Cases', color='green')
    axs[1].set_ylabel('Cumulative Cases, $N$')
    axs[1].legend()

    # Plot 3: Mortality rate.
    mortality_rate = np.zeros_like(c_df, dtype=float)
    non_zero_cumulative_cases = cumulative_cases[cumulative_cases > 0]
    if not non_zero_cumulative_cases.empty:
        mortality_rate[cumulative_cases > 0] = (
                combined_df[country + '_deaths'] / non_zero_cumulative_cases * 100
        )  # Calculate mortality rate (%)

    # Replace NaN values (resulting from dividing by zero) with zero.
    mortality_rate = np.nan_to_num(mortality_rate)

    axs[2].plot(c_df.index, mortality_rate, label='Mortality Rate', color='red')
    axs[2].set_xlabel('Date')
    axs[2].set_ylabel('Mortality Rate (%)')
    axs[2].legend()

    # Add a title reporting the latest number of cases available.
    title = '{}\n{} cases on {}'.format(country, c_df[-1],
                                        c_df.index[-1].strftime('%d %B %Y'))
    plt.suptitle(title)

    # Save the plot as an image file.
    image_path = '/app/plot.png'
    plt.savefig(image_path)

    # Print the path to the saved image.
    print(f"Plot saved to: {image_path}")


# Call the function to generate the plot.
make_plot(country)
