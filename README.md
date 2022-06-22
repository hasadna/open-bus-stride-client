# open-bus-stride-client

Python client library and CLI to interact with the [Stride REST API](https://open-bus-stride-api.hasadna.org.il/docs)

* Please report issues and feature requests [here](https://github.com/hasadna/open-bus/issues/new)
* To get updates about the system status and for general help join Hasadna's Slack #open-bus channel ([Hasadna Slack signup link](https://join.slack.com/t/hasadna/shared_invite/zt-167h764cg-J18ZcY1odoitq978IyMMig))

## Using the interactive Jupyter notebooks

This project contains several Jupyter notebooks to demonstrate usage.

For a very quickstart without any installation, you can open the notebooks online:

* [Load route rides to dataframe](https://mybinder.org/v2/gh/hasadna/open-bus-stride-client/HEAD?labpath=notebooks%2FLoad%20route%20rides%20to%20dataframe.ipynb)
* [getting all arrivals to all stops of a given line on a given day](https://mybinder.org/v2/gh/hasadna/open-bus-stride-client/HEAD?labpath=notebooks%2Fgetting%20all%20arrivals%20to%20all%20stops%20of%20a%20given%20line%20in%20a%20given%20day.ipynb)
* [load siri vehicle locations to pandas dataframe](https://mybinder.org/v2/gh/hasadna/open-bus-stride-client/main?labpath=notebooks%2Fload%20siri%20vehicle%20locations%20to%20pandas%20dataframe.ipynb)
* [load gtfs timetable to pandas dataframe](https://mybinder.org/v2/gh/hasadna/open-bus-stride-client/HEAD?labpath=notebooks%2Fload%20gtfs%20timetable%20to%20pandas%20dataframe.ipynb)

## Local Usage

Install the library

```
pip install --upgrade open-bus-stride-client
```

### API Access

The client provides the following methods for generic API access:

* `stride.get(path, params=None)`: Make a GET request to the given path with optional params dict
* `stride.iterate(path, params=None, limit=1000)`: For list operations - iterate over all items up to the given limit.

Refer to the [API Docs](https://open-bus-stride-api.hasadna.org.il/docs) for the available paths, parameter types and general usage.

### CLI Support

Most methods are available via CLI, to install CLI support:

```
pip install --upgrade open-bus-stride-client[cli]
```

See the CLI help message for details:

```
stride --help
```

