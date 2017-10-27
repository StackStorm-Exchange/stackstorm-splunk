import splunklib.client as client
import splunklib.results as results

from st2common.runners.base_action import Action

__all__ = [
    'OneShotSearch'
]


class OneShotSearch(Action):

    def __init__(self, config):
        super(OneShotSearch, self).__init__(config)

        self.service = client.connect(
            host=self.config.get('host'),
            port=self.config.get('port'),
            username=self.config.get('username'),
            password=self.config.get('password'),
            scheme=self.config.get('scheme'))

    def run(self, query):
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
