from app import App
import pytz
from datetime import datetime
import random
import json
import sys


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

        self.kafka_producer.produce(topic=self.kafka_topic,
                                    value=json.dumps(output_data).encode('utf-8'))
        self.kafka_producer.flush()

if __name__ == "__main__":
    config = {
        "id": "mock temperature data generator",
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

    try:
        temp_generator = Temperature(config)
        temp_generator.execute()

    except KeyboardInterrupt:
        print('Simulation stopped manually')
        sys.exit(0)

    except Exception as e:
        print(f'Simulation crashed due to {e}')
        sys.exit(1)
