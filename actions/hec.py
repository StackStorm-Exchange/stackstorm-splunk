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
    """First try to generate a token, if not, get existing token"""

    def run(self, instance):
        """get hec token"""
        """Collect instance details from config."""

        if not instance:
            instance = "default"

        # Get insstance details
        instance_details = self.instance_details(instance)
        # Cannot be headers from self.instance
        headers = {'Accept-Language': 'application/json'}

        data = {
          'name': 'stackstorm',
          'index': 'main',
          'indexes': 'main,summary'
        }

        response = requests.post(instance_details['base_url'] +
                                 '/servicesNS/nobody/search/data/inputs/http',
                                 headers=instance_details['headers'],
                                 data=data,
                                 verify=instance_details['verify'])

        if response.status_code != 201:
            response = requests.get(instance_details['base_url'] +
                                    '/servicesNS/nobody/search/data/inputs/http',
                                    headers=instance_details['headers'],
                                    data=data,
                                    verify=instance_details['verify'])

        dom=xml.dom.minidom.parseString(response.text)

        keys=dom.getElementsByTagName('s:key')

        for n in keys:
            if n.getAttribute('name') == 'token':
                myToken = n.childNodes[0].nodeValue

        return (myToken)
