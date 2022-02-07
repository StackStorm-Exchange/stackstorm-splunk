import json
import requests
import urllib3

from st2common.runners.base_action import Action


class SplunkBaseAction(Action):
    """Base function for calling other api actions."""
    def __init__(self, config):
        super(SplunkBaseAction, self).__init__(config)
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

    def instance_details(self, instance):
        """Collect instance details from config."""
        # requests.packages.urllib3.disable_warnings()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Build the base splunk url
        splunk_config = self.config['splunk_instances'].get(instance)

        host = splunk_config.get('host')
        port = splunk_config.get('port')
        scheme = splunk_config.get('scheme')
        verify = splunk_config.get('verify')

        try:
            if splunk_config.get('splunkToken'):
                splunk_token = splunk_config.get('splunkToken')
            else:
                username = splunk_config.get('username')
                password = splunk_config.get('password')
                splunk_token = None
        except BaseException as err:
            raise Exception(
                "Failed to connect to Splunk"
                "Instance {} with error {}".format(splunk_config, err))

        base_url = "{}://{}:{}/".format(scheme, host, port)

        if splunk_token:
            headers = self.get_header(base_url,
                                      verify,
                                      splunk_token=splunk_token)
        else:
            headers = self.get_header(base_url,
                                      verify,
                                      username=username,
                                      password=password)

        conn_info = {
            "base_url": base_url,
            "verify": verify,
            "headers": headers
        }

        return conn_info

    @staticmethod
    def get_header(base_url, verify, splunk_token=None, username=None, password=None):
        """Format and build header for splunk auth."""
        # get token from splunk
        if not splunk_token:
            token = requests.get(base_url +
                                 "/servicesNS/admin/search/auth/login",
                                 data={'username': username,
                                       'password': password,
                                       'output_mode': 'json'}, verify=verify)
            json_token = json.loads(token.text)
            session_key = str(json_token['sessionKey'])

            headers = {'Accept-Language': 'application/json',
                       'Authorization': f'Splunk {session_key}'}
        else:
            headers = {'Accept-Language': 'application/json',
                       'Authorization': f'Bearer {splunk_token}'}

        return headers
