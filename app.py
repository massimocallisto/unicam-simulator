import json
import time
import random
import string
import uuid

from functions import *


class App:
    def __init__(self, config=None):
        self.id = str(uuid.uuid4())
        self.params = None
        self.data_model = None
        self.output_keys = []
        self.config = config
        self.configured = False
        self.interval = 1
        self.max_iterations = -1
        self.iteration = -1

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

            if "id" in self.config:
                self.id = self.config['id']

            if "T" in self.params:
                self.interval = self.params['T']
            if "max_iterations" in self.params:
                self.max_iterations = self.params['max_iterations']

            self.configured = True

    def execute(self):
        if not self.configured:
            self.configure()

        try:
            self.iteration = 1
            while True:
                self.run()

                time.sleep(self.interval)

                self.iteration = self.get_iteration(self.iteration + 1)
                if self.iteration is None:
                    return

        except KeyboardInterrupt:
            print("Simulation stopped.")

    def run(self):
        random_text = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))

        output_data = self.set_output(locals(), )

        # Print the output JSON
        print(json.dumps(output_data))

    def get_iteration(self, iteration):
        if self.max_iterations != -1 and iteration > self.max_iterations:
            return None
        return iteration

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
        "id": "optional id generator",
        "params": {
            "T": 2,
            "max_iterations": 3
        },
        "data_model": {
            "simple_message": "${random_text}",
            "iteration": "${iteration}",
            "ref": "${id}"
        }
    }

    app = App(config)
    app.execute()
