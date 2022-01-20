# Splunk Integration Pack

Basic integration with Splunk Enterprise, Splunk Cloud, or Splunk Light: http://www.splunk.com/en_us/products.html

## Configuration

Copy the example configuration in [splunk.yaml.example](./splunk.yaml.example)
to `/opt/stackstorm/configs/splunk.yaml` and edit as required.

It should contain:

* ``instance`` - Friendly instance name
* ``host`` - Splunk server
* ``port`` - Splunk API port (default: 8089)
* ``username`` - Splunk username
* ``password`` - Splunk password
* ``splunkToken`` - Bear token from splunk for authentication
* ``scheme`` - Protocol for contacting Splunk API (default: https)
* ``verify`` - Should vertificate validation be performed (default: true)
* ``hec_endpoint`` - The Splunk's HEC URL (default: /services/collector)
* ``hec_port`` - The port HEC is listening on (default: 8088)

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Actions

### search

Runs a synchronous search to get Splunk data. E.g., `st2 run splunk.search query='search * | head 10`. Refer to [Splunk documentation](http://docs.splunk.com/Documentation/Splunk/5.0/Search/Aboutthesearchlanguage) for search query syntax.

As of version 0.5.0, this returns formatted results, rather than raw data, e.g.:

```bash
lhill@st2:~$ st2 run splunk.search query='search * | head 1'
.
id: 597439dec3540c7fd6b84da2
status: succeeded
parameters:
  query: search * | head 1
result:
  exit_code: 0
  result:
  - _bkt: main~3~DD5C5A84-8334-433E-89BC-7AD42FFE7E6F
    _cd: 3:237
    _indextime: '1500593568'
    _raw: 'Jul 20 16:32:48 10.25.101.2 Jul 20 16:32:33 mlx16-1 Security: ssh terminated by lhill from src IP 10.125.101.160 from USER EXEC mode using RSA as Server Host Key. Reason Code: 11, Description:disconnected by user. '
    _serial: '0'
    _si:
    - Splunk
    - main
    _sourcetype: syslog
    _time: '2017-07-20T16:32:48.000-07:00'
    host: 10.25.101.2
    index: main
    linecount: '1'
    source: udp:514
    sourcetype: syslog
    splunk_server: Splunk
  stderr: ''
  stdout: ''
lhill@st2:~$
```

### get_user

Retrieves user info by name. E.g., `st2 run splunk.get_user user=admin`.

## Sensors

No sensors yet...but pull requests welcome!

See https://stackstorm.com/2016/10/21/auto-remediation-stackstorm-splunk/ for an example of how to submit events from Splunk
into StackStorm

## Maintainers

Active pack maintainers with review & write repository access and expertise with Splunk:

* Sean Elliott ([@satellite-no](https://github.com/satellite-no)), <satellite-no@users.noreply.github.com> deepwatch
