# Project Name

## Project Structure

<pre>project-root
│
├── .gitignore
├── README.md
└── app
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── run.sh
    └── code
        ├── main.py
        ├── time_series_covid19_confirmed_global.csv
        ├── time_series_covid19_deaths_global.csv
        └── time_series_covid19_recovered_global.csv
</pre>

## Setup Instructions

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)
*   Python 3.9

### Steps

1.  Clone the repository:

<pre>
git clone repository-url
cd repository-directory/app
</pre>

1.  Run the setup script to build the Docker image and start the container:

<pre>
bash run.sh
</pre>

This script does the following:

*   Removes any existing containers.
*   Builds the Docker image using the Dockerfile.
*   Runs the Docker container in detached mode.
*   Starts an interactive session inside the container.

1.  Once the container is running, execute the main Python script:

<pre>python3 main.py
</pre>

This script generates and saves plots based on the COVID-19 data for a specified country.

1.  Find the generated plot at `/app/plot.png`.

## Additional Information

*   The `docker-compose.yml` file sets up the Docker service for running the Python application with X11 support.
*   The `Dockerfile` installs necessary dependencies and copies the Python code and data into the container.
*   The `requirements.txt` file lists the Python packages required for the project.
*   The `run.sh` script automates the setup process by handling Docker container creation and image building.
*   The `code` directory contains the main Python script (`main.py`) and COVID-19 data files.

Feel free to modify the code and adapt the instructions based on your specific needs.