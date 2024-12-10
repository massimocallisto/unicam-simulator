from app import App
import pytz
from datetime import datetime
import random
import json


class Temperature(App):

    def run(self):
        # Parse the input JSON configuration
        params = self.get_config("params")
        data_model = self.get_config('data_model')

        # Extract parameters
        tz = pytz.timezone(params['TZ'])
        interval = params['T']
        min_temp = params['MIN']
        max_temp = params['MAX']

        # Initialize the start time
        current_time = datetime.now(tz)

        # Generate a random temperature
        temperature = random.uniform(min_temp, max_temp)

        # Create a copy of the data_model to modify
        output_data = self.set_output(locals())

        # Print the output JSON
        print(json.dumps(output_data))


if __name__ == "__main__":
    config = {
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

    temp_generator = Temperature(config)
    temp_generator.execute()
