# Unicam App Simulation Project

This project is a Python-based simulation application designed to generate data in JSON format. The application takes as input a structured data model with placeholders, replaced at runtime according to the application logic.

## System Requirements
* Python 3.8 or higher
* Docker (for containerized deployment)
* Pip (Python package installer)

## Docker Usage
The image is available on Docker hub. You can use the following docker run command to execute the simple App demo:

    docker run massimocallisto/unicam-data-simulator:0.0.1

You can override the command to start the temperature simulator as follows:

    docker run massimocallisto/unicam-data-simulator:0.0.1 python -u temperature.py


## Docker Usage (build locally)

Build the Docker image:

    docker-compose build .
    docker-composen up

## Configuration logic

The application takes as input a configuration as below:

```
{
  "id": "device-001",
  "params": {
    "T": 5,
    "max_iterations": 10
  },
  "data_model": {
    "message": "${random_text}",
    "iteration": "${iteration}",
    "timestamp": "${current_time}"
  }
}
```

Where:
* `id` identify the simulated object. Can be any string. If missing, the application generates a random UUID string `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
* `params` is a mandatory JSON object to pass input params according to the application logic. Two parameter can be passed as special meaning: `T` is the time interval in seconds between two iterations (default `1` second), `max_iterations` is the number of iterations to execute (default `1` time). 
* `data_model` represent the JSON output created by the application. All the string literals defined as variables `${...}` will be replaced by the application logic using the variables defined with the same name. For instance, if the application define a variable `temperature = random.uniform(10, 20)`, the corresponding `${temperature}` will get the random value assigned to the `temperature` variable.

## Temperature application

The project contains an example temperature data generation that extends the original app using the following configuration:

```
{
    "id": "jzp://edv.0001",
    "params": {
        "TZ": "UTC",
        "T": 5,
        "MIN": -10,
        "MAX": 40
    },
    "data_model": {
        "ref": "${id}",
        "tz": "${current_time}",
        "temperature": "${temperature}",
        "unit": "°"
    }
}
```
The application logic is defined in the temperature.py file. To execute the simulation build the Docker image:

    docker-compose -f docker-compose-temperature.yml build .
    docker-composen -f docker-compose-temperature.yml up



