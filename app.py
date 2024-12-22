import json
import time
import random
import string
import uuid
import os
import sys

from confluent_kafka import Producer

from functions import *

class App:
    def __init__(self, config=None):
        self.id = str(uuid.uuid4())
        self.params = None
        self.data_model = None
        # integration of kafka producer, kafka topic and kafka bootstrap servers
        self.kafka_producer = None
        self.kafka_topic = None
        self.kafka_bootstrap_servers = None
        self.output_keys = []
        self.config = config
        self.configured = False
        self.interval = 1

        if config:
            self.configure()

    def configure(self):
        """
        Initialize internal parameters from the given config.
        """
        if self.config:
            self.params = self.config['params']
            self.data_model = self.config['data_model']
            self.output_keys = collect_output_keys(self.data_model)

            # load environment variables necessary for Kafka accessability
            self.kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
            self.kafka_topic = os.getenv("KAFKA_TOPIC")
            # initialize Kafka Producer if environment variables loaded successfully
            if self.kafka_bootstrap_servers and self.kafka_topic:
                self.kafka_producer = Producer({'bootstrap.servers': self.kafka_bootstrap_servers})

            if "id" in self.config:
                self.id = self.config['id']

            if "T" in self.params:
                self.interval = self.params['T']

            self.configured = True

    def execute(self):
        if not self.configured:
            self.configure()
        while True:
            self.run()
            time.sleep(self.interval)

    def run(self):
        random_text = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))

        output_data = self.set_output(locals(), )

        self.kafka_producer.produce(topic=self.kafka_topic,
                                    value=json.dumps(output_data).encode('utf-8'))
        self.kafka_producer.flush()

    def set_output(self, local_vars=None):
        # Prepare output data
        output_data = json.loads(json.dumps(self.data_model))

        # Replace placeholders in the data_model
        for key in self.output_keys:
            current_value = get_variable_value(key, local_vars, vars(self))
            if current_value is None:
                continue
            output_data = replace_placeholder(output_data, f"${{{key}}}", current_value)

        return output_data

    def get_param(self, param_name):
        return self._get_value(param_name, self.params)

    def get_config(self, param_name):
        return self._get_value(param_name, self.config)

    @staticmethod
    def _get_value(val_name, config_map=None):
        if config_map:
            value = config_map[val_name] if val_name in config_map else None
            return value
        else:
            return None

if __name__ == "__main__":
    config = {
        "id": "mock data generator",
        "params": {
            "T": 2
        },
        "data_model": {
            "simple_message": "${random_text}",
            "ref": "${id}"
        }
    }
    try:
        app = App(config)
        app.execute()

    except KeyboardInterrupt:
        print('Simulation stopped manually')
        sys.exit(0)

    except Exception as e:
        print(f'Simulation crashed due to {e}')
        sys.exit
