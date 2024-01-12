<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis of the Impact of COVID-19</title>
</head>
<body>

<h1>Analysis of the Impact of COVID-19</h1>

<h2>Project Structure</h2>

<pre>
project-root
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
        ├── time_series_covid19_recovered_global.csv
        └── images
</pre>

<h2>Setup Instructions</h2>

<h3>1. Clone the Repository</h3>

<pre>
git clone https://github.com/KeiKey/covid19-plotting.git
cd covid19-plotting
</pre>

<h3>2.a Local Machine Setup</h3>

<h4>Prerequisites:</h4>
- Python
- Dependencies from requirements.txt

<pre>
pip install -r app/requirements.txt
python app/main.py
</pre>

<h3>2.b Docker Setup</h3>

<h4>Prerequisites:</h4>
- Docker
- Docker Compose

<pre>
cd app
bash run.sh
</pre>

After the above commands finish, you'll be inside the Docker container. Run the script like this:

<pre>
python3 main.py
</pre>

<h2>Usage</h2>

<p>The script <code>main.py</code> allows you to generate and save COVID-19 plots. Here are some usage examples:</p>

<pre>
python3 main.py

python3 main.py -c

python3 main.py --countries France,Italy

python3 main.py --countries Albania -dr
</pre>

<p>- Use <code>--countries</code> to specify a comma-separated list of countries. If it's missing then by default Germany is taken.</p>
<p>- Use <code>-c</code>, <code>-d</code>, or <code>-r</code> flags to include Confirmed Cases, Deaths, or Recoveries plots, respectively.</p>

<p>For more options and details, run:</p>

<pre>
python3 main.py --help
</pre>

<p>Generated plots will be saved in the <code>images</code> folder.</p>

</body>
</html>
