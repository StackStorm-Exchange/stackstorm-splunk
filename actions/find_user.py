import splunklib.client as client
import json 

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

    def run(self, instance, user):
        # Find config details
        if instance:
            splunk_config = self.config['splunk_instances'].get(instance)
        else:
            splunk_config = self.config['splunk_instances'].get('default')

        try:
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

        kwargs = {"sort_key":"realname", "sort_dir":"asc", "search":user}
        results = self.service.users.list(count=-1,**kwargs)

        user_results = []
        for item in results:
            #del item.service
            user_results.append(json.dumps(item._state))

        return user_results
