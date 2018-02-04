import json
import os
from typing import Mapping

import math

from demo import settings


class IntentionModel:
    def __init__(self, model_file='query-intention-model-v0.json'):
        self.file_path = os.path.join(settings.STATIC_DIR, 'datafiles', model_file)

        # load the query-intention model
        with open(self.file_path, 'r') as f:
            self.model_json = json.load(f)
            self.models = dict()
            for model in self.model_json['models']:
                coefficient_dict = dict()
                for coefficient in model['coefficients']:
                    coefficient_dict[coefficient['name']] = coefficient['value']
                self.models[model['intention']] = coefficient_dict

    def predict(self, feature_dict: Mapping[str, float], intent='PEOPLE'):
        """

        :param intent: str from ['PEOPLE', 'PROVIDERS', 'COMPANY', 'POSTS', 'SCHOOL', 'GROUP', 'JOB']
        :type feature_dict: Mapping[str, float]
        """
        model = self.models[intent]
        logit = 0.0
        logit_dict = dict()
        for coefficient_name, coefficient_value in model.items():
            feature_value = feature_dict.get(coefficient_name)
            if feature_value:
                logit_dict[coefficient_name] = feature_value * coefficient_value
                logit += logit_dict[coefficient_name]
        logit_dict['(INTERCEPT)'] = model.get('(INTERCEPT)', 0.0)
        logit += logit_dict['(INTERCEPT)']

        return 1.0 - (1.0 / (1.0 + math.exp(logit))), logit_dict

    def get_intention_lables(self):
        return self.models.keys()
