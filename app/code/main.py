import argparse
import os
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


def make_confirmed_cases_plots(daily_confirmed_cases_plot, total_confirmed_cases_plot, cases_by_location):
    print('Generating subplots for confirmed cases.')

    # Plot 1: Daily confirmed cases.
    cases_by_location.index = pd.to_datetime(cases_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_confirmed_cases = cases_by_location.diff().fillna(0)

    daily_confirmed_cases_plot.bar(cases_by_location.index, new_daily_confirmed_cases.values, label='Daily Confirmed Cases',color='purple')
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


def make_deaths_plots(daily_deaths_plot, total_deaths_plot, deaths_by_location):
    print('Generating subplots for deaths cases.')
    # Plot 3: Daily deaths.
    deaths_by_location.index = pd.to_datetime(deaths_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_deaths = deaths_by_location.diff().fillna(0)

    daily_deaths_plot.bar(deaths_by_location.index, new_daily_deaths.values, label='Daily Deaths', color='purple')
    daily_deaths_plot.set_ylabel('Daily Deaths')
    daily_deaths_plot.legend()
    daily_deaths_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 4: Total deaths.
    total_deaths_plot.plot(deaths_by_location.index, deaths_by_location.values, label='Total Deaths', color='orange')
    total_deaths_plot.set_xlabel('Date')
    total_deaths_plot.set_ylabel('Total Deaths')
    total_deaths_plot.legend()
    total_deaths_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    daily_deaths_plot.xaxis.set_major_locator(plt.MultipleLocator(180))
    total_deaths_plot.xaxis.set_major_locator(plt.MultipleLocator(180))


def make_recovered_plots(daily_recovered_plot, total_recovered_plot, recovered_by_location):
    print('Generating subplots for recovered cases.')

    # Plot 5: Daily recovered.
    recovered_by_location.index = pd.to_datetime(recovered_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_recoveries = recovered_by_location.diff().fillna(0)

    daily_recovered_plot.bar(recovered_by_location.index, new_daily_recoveries.values, label='Daily Recoveries', color='green')
    daily_recovered_plot.set_xlabel('Date')
    daily_recovered_plot.set_ylabel('Daily Recoveries')
    daily_recovered_plot.legend()
    daily_recovered_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 6: Total recoveries.
    total_recovered_plot.plot(recovered_by_location.index, recovered_by_location.values, label='Total Recoveries', color='cyan')
    total_recovered_plot.set_xlabel('Date')
    total_recovered_plot.set_ylabel('Total Recoveries')
    total_recovered_plot.legend()
    total_recovered_plot.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    daily_recovered_plot.xaxis.set_major_locator(plt.MultipleLocator(180))
    total_recovered_plot.xaxis.set_major_locator(plt.MultipleLocator(180))


def generate_plot(country, confirmed_cases, deaths, recoveries):
    print(f'Generating plot for {country}')

    count_of_plots_needed = sum((confirmed_cases, deaths, recoveries))
    current_plots_row = 0

    fig, axs = plt.subplots(count_of_plots_needed, 2, figsize=(15, 12), sharex=True)

    cases_by_location, deaths_by_location, recovered_by_location = get_data_for_country(country)

    if confirmed_cases:
        make_confirmed_cases_plots(axs[current_plots_row, 0], axs[current_plots_row, 1], cases_by_location)
        current_plots_row += 1

    if deaths:
        make_deaths_plots(axs[current_plots_row, 0], axs[current_plots_row, 1], deaths_by_location)
        current_plots_row += 1

    if recoveries:
        make_recovered_plots(axs[current_plots_row, 0], axs[current_plots_row, 1], recovered_by_location)

    # Change the format of the x-axis labels to display month and year.
    for ax in axs.flat:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.to_datetime(x).strftime('%m/%y')))

    # Add a title reporting the latest number of cases available. todo
    # title = '{}\n{} cases on {}'.format(country, cases_by_location.iloc[-1], cases_by_location.index[-1].strftime('%d %B %Y'))

    plt.suptitle('title')


def store_plot_to_storage(country, confirmed_cases, deaths, recoveries):
    # Create the images directory if it doesn't exist
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

    # if no flag is passed it means that we want all the plots.
    if not args.c and not args.d and not args.r:
        args.c = args.d = args.r = True

    countries = args.countries.split(',')
    for country in countries:
        generate_plot(country, args.c, args.d, args.r)

        store_plot_to_storage(country, args.c, args.d, args.r)
