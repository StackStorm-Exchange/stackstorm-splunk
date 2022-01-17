import requests
import json

from st2common.runners.base_action import Action

__all__ = [
    'SendLogAction'
]


class SendLogAction(Action):
    def __init__(self, config):
        super(SendLogAction, self).__init__(config)
        # Validate config is set
        if config is None:
            raise ValueError("No Splunk configuration details found")
        if "splunk_instances" in config:
            if config['splunk_instances'] is None:
                raise ValueError("'splunk_instances' config defined but empty.")
            else:
                pass
        else:
            raise ValueError("No Splunk configuration details found")

    def run(self, instance, index, token, event):
        # Find config details
        if instance:
            splunk_config = self.config['splunk_instances'].get(instance)
        else:
            splunk_config = self.config['splunk_instances'].get('default')

        try:
            host = splunk_config.get('host')
            port = splunk_config.get('hec_port')
            scheme = splunk_config.get('scheme')
            endpoint = splunk_config.get('hec_endpoint')
            self.url = scheme + '://' + host + ':' + str(port) + endpoint
        except BaseException as err:
            raise Exception(
                "Failed to connect to Splunk Instance {} with error {}".format(splunk_config, err)
            )

        event_headers = {'Authorization': 'Splunk ' + token, 'Content-Type': 'application/json'}
        event_payload = json.dumps({"sourcetype": "json", "index": index, "event": event})

        r = requests.post(
            url=self.url,
            headers=event_headers,
            data=event_payload,
            timeout=60,
            verify=False
        )

        if r.status_code == 200:
            return (True, r.status_code)
        else:
            return (False, r.status_code + ' ' + r.reason)
