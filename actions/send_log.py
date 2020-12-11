import requests
import json

from st2common.runners.base_action import Action

__all__ = [
    'SendLogAction'
]


class SendLogAction(Action):
    def __init__(self, config):
        super(SendLogAction, self).__init__(config)

        host = self.config.get('host')
        port = self.config.get('hec_port')
        scheme = self.config.get('scheme')
        endpoint = self.config.get('hec_endpoint')
        self.url = scheme + '://' + host + ':' + port + endpoint

    def run(self, index, token, event):
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
