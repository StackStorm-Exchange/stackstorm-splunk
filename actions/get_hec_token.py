import json
import requests
import urllib3
urllib3.disable_warnings()
import xml.dom.minidom

from lib.base import SplunkBaseAction

__all__ = [
    'GetHecToken'
]

#
class GetHecToken(SplunkBaseAction):
    """Action to get HEC token"""
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

    def run(self, instance):
        """get hec token"""
        """Collect instance details from config."""
        # requests.packages.urllib3.disable_warnings()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Build the base splunk url
        splunk_config = self.config['splunk_instances'].get(instance)

        host = splunk_config.get('host')
        port = splunk_config.get('port')
        scheme = splunk_config.get('scheme')
        verify = splunk_config.get('verify')
        username = splunk_config.get('username')
        password = splunk_config.get('password')

        base_url = "{}://{}:{}/".format(scheme, host, port)

        if not instance:
            instance = "default"

        headers = {'Accept-Language': 'application/json'}

        data = {
          'name': 'test-py',
          'index': 'main',
          'indexes': 'main,summary'
        }

        response = requests.post(base_url + '/servicesNS/nobody/search/data/inputs/http',
                                    headers=headers,
                                    data=data,
                                    verify=False,
                                    auth=(username, password))

        dom=xml.dom.minidom.parseString(response.text)

        keys=dom.getElementsByTagName('s:key')

        for n in keys:
            if n.getAttribute('name') == 'token':
                myToken = n.childNodes[0].nodeValue
        return (myToken)
