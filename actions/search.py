import splunklib.client as client
import splunklib.results as results

from st2common.runners.base_action import Action

__all__ = [
    'OneShotSearch'
]


class OneShotSearch(Action):

    def __init__(self, config):
        super(OneShotSearch, self).__init__(config)
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

    def run(self, instance, query):
        """stackstork run method"""
        # Find config details
        if instance:
            splunk_config = self.config['splunk_instances'].get(instance)
        else:
            splunk_config = self.config['splunk_instances'].get('default')

        try:
            if splunk_config.get('splunkToken'):
                self.service = client.connect(
                    host=splunk_config.get('host'),
                    port=splunk_config.get('port'),
                    splunkToken=splunk_config.get('splunkToken'),
                    scheme=splunk_config.get('scheme'),
                    verify=splunk_config.get('verify'))
            else:
                self.service = client.connect(
                    host=splunk_config.get('host'),
                    port=splunk_config.get('port'),
                    username=splunk_config.get('username'),
                    password=splunk_config.get('password'),
                    scheme=splunk_config.get('scheme'),
                    verify=splunk_config.get('verify'))
        except BaseException as err:
            raise Exception(
                "Failed to connect to Splunk Instance {} with error {}".format(splunk_config, err)
            )

        result = self.service.jobs.oneshot(query, params={"output_mode": "json"})
        reader = results.ResultsReader(result)
        search_results = []

        for item in reader:
            if isinstance(item, results.Message):
                # Diagnostic messages may be returned in the results
                # print '%s: %s' % (item.type, item.message)
                self.logger.info('%s: %s' % (item.type, item.message))
            elif isinstance(item, dict):
                # Normal events are returned as dicts
                search_results.append(item)

        return search_results
