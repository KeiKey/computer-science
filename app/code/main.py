import sys
import pandas as pd
import matplotlib.pyplot as plt

CONFIRMED_CASES_FILE = "time_series_covid19_confirmed_global.csv"
DEATH_CASES_FILE = "time_series_covid19_deaths_global.csv"
RECOVERED_CASES_FILE = "time_series_covid19_recovered_global.csv"

# The country to plot the data for.
country = 'Germany'

# Read in the data to a pandas DataFrame.
cases_data = pd.read_csv(CONFIRMED_CASES_FILE)
deaths_data = pd.read_csv(DEATH_CASES_FILE)
recoveries_data = pd.read_csv(RECOVERED_CASES_FILE)

# Group by country and sum over the different states/regions of each country.
grouped_by_country = cases_data.groupby('Country/Region')
data_frame_by_country = grouped_by_country.sum()


def make_plot(country):
    """Make different plots for case numbers, cumulative cases, and mortality rate."""

    # Extract the Series corresponding to the case numbers for the country.
    cases_by_location = data_frame_by_country.loc[country, data_frame_by_country.columns[3:]]
    # Convert the index to a proper datetime object with a flexible format.
    cases_by_location.index = pd.to_datetime(cases_by_location.index, errors='coerce')
    n = len(cases_by_location)
    if n == 0:
        print('Too few data to plot.')
        sys.exit(1)

    # Merge deaths and cumulative cases dataframes based on the common date index.
    deaths_by_location = deaths_data.groupby('Country/Region').sum().loc[country, deaths_data.columns[3:]]
    deaths_by_location.index = pd.to_datetime(deaths_by_location.index, errors='coerce')  # Updated line
    combined_df = pd.merge(cases_by_location, deaths_by_location, left_index=True, right_index=True,
                           suffixes=('_confirmed', '_deaths'))

    # Print column names for debugging.
    print("Column names in combined_df:", combined_df.columns)

    fig, axs = plt.subplots(3, 2, figsize=(15, 12), sharex=True)

    # Plot 1: Daily confirmed cases.
    axs[0, 0].bar(cases_by_location.index, cases_by_location.diff().fillna(0).values, label='Daily Confirmed Cases', color='purple')
    axs[0, 0].set_ylabel('Daily Confirmed Cases')
    axs[0, 0].legend()

    # Plot 2: Total confirmed cases.
    axs[0, 1].plot(cases_by_location.index, cases_by_location.values, label='Total Confirmed Cases', color='blue')
    axs[0, 1].set_ylabel('Confirmed cases, $N$')
    axs[0, 1].legend()
    axs[0, 1].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 3: Daily deaths.
    new_daily_deaths = deaths_by_location.diff().fillna(0)
    axs[1, 0].bar(deaths_by_location.index, new_daily_deaths.values, label='Daily Deaths', color='purple')
    axs[1, 0].set_ylabel('Daily Deaths')
    axs[1, 0].legend()

    # Plot 4: Total deaths.
    axs[1, 1].plot(deaths_by_location.index, deaths_by_location.values, label='Total Deaths', color='orange')
    axs[1, 1].set_xlabel('Date')
    axs[1, 1].set_ylabel('Total Deaths')
    axs[1, 1].legend()
    axs[1, 1].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 5: Daily recoveries.
    recovered_by_location = recoveries_data.groupby('Country/Region').sum().loc[country, recoveries_data.columns[3:]]
    recovered_by_location.index = pd.to_datetime(recovered_by_location.index, errors='coerce')  # Updated line
    new_daily_recoveries = recovered_by_location.diff().fillna(0)
    axs[2, 0].bar(recovered_by_location.index, new_daily_recoveries.values, label='Daily Recoveries', color='green')
    axs[2, 0].set_xlabel('Date')
    axs[2, 0].set_ylabel('Daily Recoveries')
    axs[2, 0].legend()

    # Plot 6: Total recoveries.
    axs[2, 1].plot(recovered_by_location.index, recovered_by_location.values, label='Total Recoveries', color='cyan')
    axs[2, 1].set_xlabel('Date')
    axs[2, 1].set_ylabel('Total Recoveries')
    axs[2, 1].legend()
    axs[2, 1].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    axs[0, 0].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[0, 1].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[1, 0].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[1, 1].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[2, 0].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[2, 1].xaxis.set_major_locator(plt.MultipleLocator(180))

    # Change the format of the x-axis labels to display month and year.
    for ax in axs.flat:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.to_datetime(x).strftime('%m/%y')))

    # Add a title reporting the latest number of cases available.
    title = '{}\n{} cases on {}'.format(country, cases_by_location[-1],
                                        cases_by_location.index[-1].strftime('%d %B %Y'))
    plt.suptitle(title)

    # Save the plot as an image file.
    image_path = '/app/plot.png'
    plt.savefig(image_path)

    # Print the path to the saved image.
    print(f"Plot saved to: {image_path}")


# Call the function to generate the plot.
make_plot(country)
