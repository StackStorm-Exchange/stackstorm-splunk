# Change Log

## 2.1.1

- Refactor to modularize token retrieval

## 2.1.0

- Feature authenticate via bear token vs username and password
- Feature added action get_user

## 2.0.0

- Fixed bug in entry point for send_log.
- Added support for multiple Splunk instances.

## 1.0.0

* Drop Python 2.7 support

## 0.6.2

- Added feature to send logs to Splunk via Hec (Http Event Collector)

## 0.6.1

- Add explicit support for Python 2 and 3

## 0.6.0

- Added the ability to disable SSL validation using `verify: false` in `splunk.yaml`

## 0.5.1

- Removed unused `version` string from `config.schema.yaml
 
## 0.5.0

- Update splunk.search to use splunklib.results.ResultsReader to return formatted results,
  instead of raw data

## 0.4.0

- Updated action `runner_type` from `run-python` to `python-script`

## 0.3.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
