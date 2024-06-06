# Generic Connector with mock OAuth2 API Server
A generic connector is included and can be utilized to evaluate the connector workflow locally. A local API Server which implements the oauth2 client credentials flow is also included.

## Prerequisites

* Python 3
* Amazon Q application and custom connector setup. See [AWS documentation](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/custom-connector.html) for details.

## How to run

1) Install python dependencies

```
pip3 install -r requirements.txt
```

2) Start the local API Server. Go to `examples/generic` and run the server.py: `python3 server.py`

3) Download and store pdf files into `examples/generic/documents`. The local API server will serve these files to the generic connector.

4) The generic connector utilizes the `generic_connector` class. You can view this in the `common.py` file.

5) Set the following environment variables:

* Q_INDEX_ID - Q index id
* Q_DATASOURCE_ID - Q datasource id
* Q_APPLICATION_ID - Q application id
* OAUTH2_CLIENT_ID - can be any value as the mock API server will take any value.
* OAUTH2_SECRET - can be any value as the mock API server will take any value.
* OAUTH2_TOKEN_URL - must be http://localhost:5000/oauth/token

6) A end to end connector is implemented in `examples/generic/connector.py`. You can run this connector to sync files from `examples/generic/documents` to Amazon Q for Business: `python3 connector.py`
