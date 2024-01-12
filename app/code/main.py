import argparse
import matplotlib.pyplot as plt
import pandas as pd

CONFIRMED_CASES_FILE = "time_series_covid19_confirmed_global.csv"
DEATH_CASES_FILE = "time_series_covid19_deaths_global.csv"
RECOVERED_CASES_FILE = "time_series_covid19_recovered_global.csv"
DATE_FORMAT = '%m/%d/%y'


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate and save COVID-19 plots.')

    # Add optional argument --countries
    parser.add_argument('--countries', type=str, default='Germany',
                        help='Name of the comma-separated countries for which to generate plots. Germany is default if this argument is missing')

    # Add optional flags c/d/r
    parser.add_argument('-c', action='store_true', help='Pass this flag if you want the Confirmed Cases plots.')
    parser.add_argument('-d', action='store_true', help='Pass this flag if you want the Deaths plots.')
    parser.add_argument('-r', action='store_true', help='Pass this flag if you want the Recoveries plots.')

    return parser.parse_args()


def get_data_for_country(country):
    # Read in the data to a pandas DataFrame.
    cases_data = pd.read_csv(CONFIRMED_CASES_FILE)
    deaths_data = pd.read_csv(DEATH_CASES_FILE)
    recovered_data = pd.read_csv(RECOVERED_CASES_FILE)

    # Group by country and sum over the different states/regions of each country.
    cases_grouped_by_country = cases_data.groupby('Country/Region')
    cases_data_frame_by_country = cases_grouped_by_country.sum()

    # Extract the Series corresponding to the case numbers for the country.
    cases_by_location = cases_data_frame_by_country.loc[country, cases_data_frame_by_country.columns[3:]]

    # Group by country and sum over the different states/regions of each country.
    deaths_grouped_by_country = deaths_data.groupby('Country/Region')
    deaths_data_frame_by_country = deaths_grouped_by_country.sum()

    # Extract the Series corresponding to the case numbers for the country.
    deaths_by_location = deaths_data_frame_by_country.loc[country, deaths_data_frame_by_country.columns[3:]]

    # Group by country and sum over the different states/regions of each country.
    recovered_grouped_by_country = recovered_data.groupby('Country/Region')
    recovered_data_frame_by_country = recovered_grouped_by_country.sum()

    # Extract the Series corresponding to the case numbers for the country.
    recovered_by_location = recovered_data_frame_by_country.loc[country, recovered_data_frame_by_country.columns[3:]]

    return cases_by_location, deaths_by_location, recovered_by_location


def make_confirmed_cases_plots(axs, cases_by_location):
    # Plot 1: Daily confirmed cases.
    cases_by_location.index = pd.to_datetime(cases_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_confirmed_cases = cases_by_location.diff().fillna(0)

    axs[0, 0].bar(cases_by_location.index, new_daily_confirmed_cases.values, label='Daily Confirmed Cases',color='purple')
    axs[0, 0].set_ylabel('Daily Confirmed Cases')
    axs[0, 0].legend()
    axs[0, 0].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 2: Total confirmed cases.
    axs[0, 1].plot(cases_by_location.index, cases_by_location.values, label='Total Confirmed Cases', color='blue')
    axs[0, 1].set_ylabel('Confirmed cases, $N$')
    axs[0, 1].legend()
    axs[0, 1].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    axs[0, 0].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[0, 1].xaxis.set_major_locator(plt.MultipleLocator(180))


def make_deaths_plots(axs, deaths_by_location):
    # Plot 3: Daily deaths.
    deaths_by_location.index = pd.to_datetime(deaths_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_deaths = deaths_by_location.diff().fillna(0)

    axs[1, 0].bar(deaths_by_location.index, new_daily_deaths.values, label='Daily Deaths', color='purple')
    axs[1, 0].set_ylabel('Daily Deaths')
    axs[1, 0].legend()
    axs[1, 0].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 4: Total deaths.
    axs[1, 1].plot(deaths_by_location.index, deaths_by_location.values, label='Total Deaths', color='orange')
    axs[1, 1].set_xlabel('Date')
    axs[1, 1].set_ylabel('Total Deaths')
    axs[1, 1].legend()
    axs[1, 1].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    axs[1, 0].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[1, 1].xaxis.set_major_locator(plt.MultipleLocator(180))


def make_recovered_plots(axs, recovered_by_location):
    # Plot 5: Daily recovered.
    recovered_by_location.index = pd.to_datetime(recovered_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_recoveries = recovered_by_location.diff().fillna(0)

    axs[2, 0].bar(recovered_by_location.index, new_daily_recoveries.values, label='Daily Recoveries', color='green')
    axs[2, 0].set_xlabel('Date')
    axs[2, 0].set_ylabel('Daily Recoveries')
    axs[2, 0].legend()
    axs[2, 0].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 6: Total recoveries.
    axs[2, 1].plot(recovered_by_location.index, recovered_by_location.values, label='Total Recoveries', color='cyan')
    axs[2, 1].set_xlabel('Date')
    axs[2, 1].set_ylabel('Total Recoveries')
    axs[2, 1].legend()
    axs[2, 1].ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    axs[2, 0].xaxis.set_major_locator(plt.MultipleLocator(180))
    axs[2, 1].xaxis.set_major_locator(plt.MultipleLocator(180))


def make_plots(country, confirmed_cases, deaths, recoveries):
    fig, axs = plt.subplots(3, 2, figsize=(15, 12), sharex=True)

    cases_by_location, deaths_by_location, recovered_by_location = get_data_for_country(country)

    if confirmed_cases:
        make_confirmed_cases_plots(axs, cases_by_location)

    if deaths:
        make_deaths_plots(axs, deaths_by_location)

    if recoveries:
        make_recovered_plots(axs, recovered_by_location)

    # Change the format of the x-axis labels to display month and year.
    for ax in axs.flat:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.to_datetime(x).strftime('%m/%y')))

    # Add a title reporting the latest number of cases available. todo
    # title = '{}\n{} cases on {}'.format(country, cases_by_location.iloc[-1], cases_by_location.index[-1].strftime('%d %B %Y'))

    plt.suptitle('title')

    # Save the plot as an image file.
    image_path = '/app/plot.png'
    plt.savefig(image_path)

    # Print the path to the saved image.
    print(f"Plot saved to: {image_path}")


if __name__ == "__main__":
    args = parse_arguments()

    # if no flag is passed it means that we want all the plots.
    if not args.c and not args.d and not args.r:
        args.c = args.d = args.r = True

    countries = args.countries.split(',')
    for country in countries:
        print(f'Generating plots for {country}')
        make_plots(country, args.c, args.d, args.r)
