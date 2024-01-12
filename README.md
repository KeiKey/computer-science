# Analysis of the Impact of COVID-19

## Project Structure

<pre>
    project-root
    │
    └── app
        ├── main.py
        ├── time_series_covid19_confirmed_global.csv
        ├── time_series_covid19_deaths_global.csv
        ├── time_series_covid19_recovered_global.csv
        └── images
    ├── .gitignore
    ├── README.md
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    └── run.sh
</pre>

## Setup Instructions

### 1\. Clone the Repository

<pre>
    git clone https://github.com/KeiKey/covid19-plotting.git
    cd covid19-plotting
</pre>

### 2.a Local Machine Setup

#### Prerequisites:

- Python 
- Dependencies from requirements.txt

<pre>
    pip install -r requirements.txt
    python3 main.py
</pre>

### 2.b Docker Setup

#### Prerequisites:

- Docker 
- Docker Compose

<pre>
    bash run.sh
</pre>

After the above commands finish, you'll be inside the Docker container. Run the script like this:

<pre>
    python3 main.py
</pre>

## Usage

The script `main.py` allows you to generate and save COVID-19 plots. Here are some usage examples:

<pre>python3 main.py

python3 main.py -c

python3 main.py --countries France,Italy

python3 main.py --countries Albania -dr
</pre>

- Use `--countries` to specify a comma-separated list of countries. If it's missing then by default Germany is taken.
- Use `-c`, `-d`, or `-r` flags to include Confirmed Cases, Deaths, or Recoveries plots, respectively.

For more options and details, run:

<pre>
    python3 main.py --help
</pre>

Generated plots will be saved in the `images` folder.