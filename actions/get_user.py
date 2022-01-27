import requests
import json
import pprint

from lib.base import SplunkBaseAction

__all__ = [
    'FindUserAction'
]


class FindUserAction(SplunkBaseAction):

    def run(self, instance, userName):

        if not instance:
            instance = "default"
        
        instance_details = self.instance_details(instance)

        print(instance_details)
        data = {'output_mode': 'json'}
        r = requests.get(instance_details['base_url'] +
                         '/services/authentication/users/{}'.format(userName),
                         data=data,
                         headers=instance_details['headers'],
                         verify=instance_details['verify'])

        return pprint.pprint(json.loads(r.text))
