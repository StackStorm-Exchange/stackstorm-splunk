import requests
import json
import pprint

from st2common.runners.base_action import Action

__all__ = [
    'FindUserAction'
]


class FindUserAction(Action):

    def __init__(self, config):
        super(FindUserAction, self).__init__(config)
        # Validate config is set
        if config is None:
            raise ValueError("No Splunk configuration details found")
        if "splunk_instances" in config:
            if config['splunk_instances'] is None:
                raise ValueError("'splunk_instances' config empty.")
            else:
                pass
        else:
            raise ValueError("No Splunk configuration details found")

    def run(self, instance, userName):
        # requests.packages.urllib3.disable_warnings()

        # Find config details
        if instance:
            splunk_config = self.config['splunk_instances'].get(instance)
        else:
            splunk_config = self.config['splunk_instances'].get('default')

        try:
            if splunk_config.get('splunkToken'):
                host = splunk_config.get('host')
                port = splunk_config.get('port')
                splunkToken = splunk_config.get('splunkToken')
                scheme = splunk_config.get('scheme')
                verify = splunk_config.get('verify')
            else:
                host = splunk_config.get('host')
                port = splunk_config.get('port')
                username = splunk_config.get('username')
                password = splunk_config.get('password')
                scheme = splunk_config.get('scheme')
                verify = splunk_config.get('verify')
                splunkToken = None

        except BaseException as err:
            raise Exception(
                "Failed to connect to Splunk"
                "Instance {} with error {}".format(splunk_config, err))

        base_url = scheme + '://' + host + ':' + str(port)

        if not splunkToken:
            token = requests.get(base_url +
                                 "/servicesNS/admin/search/auth/login",
                                 data={'username': username,
                                       'password': password,
                                       'output_mode': 'json'}, verify=verify)
            json_token = json.loads(token.text)
            session_key = str(json_token['sessionKey'])

            headers = {'Accept-Language': 'application/json',
                       'Authorization': 'Splunk {}'.format(session_key)}
        else:
            headers = {'Accept-Language': 'application/json',
                       'Authorization': 'Bearer {}'.format(splunkToken)}

        print(headers)
        data = {'output_mode': 'json'}
        r = requests.get(base_url +
                         '/services/authentication/users/{}'.format(userName),
                         data=data,
                         headers=headers,
                         verify=verify)

        return pprint.pprint(json.loads(r.text))
