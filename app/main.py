import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import pandas.core.series as series
import pandas as pd

CONFIRMED_CASES_FILE = "time_series_covid19_confirmed_global.csv"
DEATHS_FILE = "time_series_covid19_deaths_global.csv"
RECOVERIES_FILE = "time_series_covid19_recovered_global.csv"
DATE_FORMAT = '%m/%d/%y'


def parse_arguments() -> argparse:
    parser = argparse.ArgumentParser(description='Generate and save COVID-19 plots.')

    # Add optional argument --countries
    parser.add_argument('--countries', type=str, default='Germany',
                        help='Name of the comma-separated countries for which to generate plots. Germany is default if this argument is missing')

    # Add optional flags c/d/r
    parser.add_argument('-c', action='store_true', help='Pass this flag if you want the Confirmed Cases plots.')
    parser.add_argument('-d', action='store_true', help='Pass this flag if you want the Deaths plots.')
    parser.add_argument('-r', action='store_true', help='Pass this flag if you want the Recoveries plots.')

    return parser.parse_args()


def get_data_for_country(country: str) -> tuple:
    print('Getting the data for the subplots.')
    # Read in the data to a pandas DataFrame.
    cases_data = pd.read_csv(CONFIRMED_CASES_FILE)
    deaths_data = pd.read_csv(DEATHS_FILE)
    recoveries_data = pd.read_csv(RECOVERIES_FILE)

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
    recoveries_grouped_by_country = recoveries_data.groupby('Country/Region')
    recoveries_data_frame_by_country = recoveries_grouped_by_country.sum()
    # Extract the Series corresponding to the case numbers for the country.
    recoveries_by_location = recoveries_data_frame_by_country.loc[country, recoveries_data_frame_by_country.columns[3:550]]

    return cases_by_location, deaths_by_location, recoveries_by_location


def make_confirmed_cases_subplots(daily_confirmed_cases_plot: axes, total_confirmed_cases_plot: axes, cases_by_location: series) -> None:
    print('Generating subplots for confirmed cases.')

    # Plot 1: Daily confirmed cases.
    cases_by_location.index = pd.to_datetime(cases_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_confirmed_cases = cases_by_location.diff().fillna(0).clip(lower=0)  # Set negative values to zero

    daily_confirmed_cases_plot.bar(cases_by_location.index, new_daily_confirmed_cases.values, label='Daily Confirmed Cases', color='purple')
    daily_confirmed_cases_plot.set_ylabel('Daily Confirmed Cases')
    daily_confirmed_cases_plot.legend()
    daily_confirmed_cases_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 2: Total confirmed cases.
    total_confirmed_cases_plot.plot(cases_by_location.index, cases_by_location.values, label='Total Confirmed Cases', color='blue')
    total_confirmed_cases_plot.set_ylabel('Confirmed cases, $N$')
    total_confirmed_cases_plot.legend()
    total_confirmed_cases_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    daily_confirmed_cases_plot.xaxis.set_major_locator(plt.MultipleLocator(180))
    total_confirmed_cases_plot.xaxis.set_major_locator(plt.MultipleLocator(180))


def make_deaths_subplots(daily_deaths_plot: axes, total_deaths_plot: axes, deaths_by_location: series) -> None:
    print('Generating subplots for deaths cases.')

    # Plot 3: Daily deaths.
    deaths_by_location.index = pd.to_datetime(deaths_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_deaths = deaths_by_location.diff().fillna(0).clip(lower=0)  # Set negative values to zero

    daily_deaths_plot.bar(deaths_by_location.index, new_daily_deaths.values, label='Daily Deaths', color='purple')
    daily_deaths_plot.set_ylabel('Daily Deaths')
    daily_deaths_plot.legend()
    daily_deaths_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 4: Total deaths.
    total_deaths_plot.plot(deaths_by_location.index, deaths_by_location.values, label='Total Deaths', color='orange')
    total_deaths_plot.set_ylabel('Total Deaths')
    total_deaths_plot.legend()
    total_deaths_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    daily_deaths_plot.xaxis.set_major_locator(plt.MultipleLocator(180))
    total_deaths_plot.xaxis.set_major_locator(plt.MultipleLocator(180))


def make_recoveries_subplots(daily_recoveries_plot: axes, total_recoveries_plot: axes, recoveries_by_location: series) -> None:
    print('Generating subplots for recoveries cases.')

    # Plot 5: Daily recoveries.
    recoveries_by_location.index = pd.to_datetime(recoveries_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_recoveries = recoveries_by_location.diff().fillna(0).clip(lower=0)  # Set negative values to zero

    daily_recoveries_plot.bar(recoveries_by_location.index, new_daily_recoveries.values, label='Daily Recoveries', color='green')
    daily_recoveries_plot.set_ylabel('Daily Recoveries')
    daily_recoveries_plot.legend()
    daily_recoveries_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 6: Total recoveries.
    total_recoveries_plot.plot(recoveries_by_location.index, recoveries_by_location.values, label='Total Recoveries', color='cyan')
    total_recoveries_plot.set_ylabel('Total Recoveries')
    total_recoveries_plot.legend()
    total_recoveries_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    daily_recoveries_plot.xaxis.set_major_locator(plt.MultipleLocator(180))
    total_recoveries_plot.xaxis.set_major_locator(plt.MultipleLocator(180))


def generate_plot(country: str, confirmed_cases: bool, deaths: bool, recoveries: bool) -> None:
    print(f'Generating plot for {country}')

    count_of_subplots_needed = sum((confirmed_cases, deaths, recoveries))
    current_subplots_row = 0

    fig, axs = plt.subplots(count_of_subplots_needed, 2, figsize=(15, 12), sharex=True)

    cases_by_location, deaths_by_location, recoveries_by_location = get_data_for_country(country)

    if confirmed_cases:
        daily_cases_subplot = axs[0] if count_of_subplots_needed == 1 else axs[current_subplots_row, 0]
        total_cases_subplot = axs[1] if count_of_subplots_needed == 1 else axs[current_subplots_row, 1]

        make_confirmed_cases_subplots(daily_cases_subplot, total_cases_subplot, cases_by_location)
        current_subplots_row += 1

    if deaths:
        daily_deaths_subplot = axs[0] if count_of_subplots_needed == 1 else axs[current_subplots_row, 0]
        total_deaths_subplot = axs[1] if count_of_subplots_needed == 1 else axs[current_subplots_row, 1]

        make_deaths_subplots(daily_deaths_subplot, total_deaths_subplot, deaths_by_location)
        current_subplots_row += 1

    if recoveries:
        daily_recoveries_subplot = axs[0] if count_of_subplots_needed == 1 else axs[current_subplots_row, 0]
        total_recoveries_subplot = axs[1] if count_of_subplots_needed == 1 else axs[current_subplots_row, 1]

        make_recoveries_subplots(daily_recoveries_subplot, total_recoveries_subplot, recoveries_by_location)

    # Rotate x-axis labels for better visibility.
    for ax in axs.flat:
        ax.tick_params(axis='x', rotation=45)

    # Add a title reporting the latest number of cases available.
    title = f"Analysis of the Impact of COVID-19 in {country}"

    plt.suptitle(title)


def store_plot_to_storage(country: str, confirmed_cases: bool, deaths: bool, recoveries: bool) -> None:
    # Create the image's directory if it doesn't exist
    images_dir = '/app/images'
    os.makedirs(images_dir, exist_ok=True)

    # Construct the image name based on the flags
    image_name = f"{country}_"
    if confirmed_cases:
        image_name += "c"
    if deaths:
        image_name += "d"
    if recoveries:
        image_name += "r"

    # Add the plot suffix
    image_name += "_plot.png"

    # Save the plot as an image file.
    image_path = os.path.join(images_dir, image_name)
    plt.savefig(image_path)

    # Print the path to the saved image.
    print(f"Plot saved to: {image_path}")


if __name__ == "__main__":
    args = parse_arguments()

    # if no flag is passed it means that we want all the subplots.
    if not args.c and not args.d and not args.r:
        args.c = args.d = args.r = True

    countries = args.countries.split(',')
    for country in countries:
        generate_plot(country, args.c, args.d, args.r)

        store_plot_to_storage(country, args.c, args.d, args.r)
