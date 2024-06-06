# Amazon Q for Business connector for Dynamics 365 Business Central

## Prerequisites

* Python 3
* Amazon Q application and custom connector setup. See [AWS documentation](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/custom-connector.html) for details.

## Dynamics 365 Business Central Setup

1) Create Entra ID application. See [documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-develop-connect-apps#set-up-microsoft-entra-id-based-authentication) for more details.

2) Since we are creating an client credentials flow (Service to Service), the API permissions for the application will be different:

* API.ReadWrite.All
* app_access

3) Once you have created an Entra ID application with the proper permissions, you will need to ensure it has admin consent. If you are the administrator of your organization, you can do that in the API Permissions section by clicking on the "Grant admin consent for [organization domain]". If you are not the administrator for your organization, you will need them to perform this step.

4) Ensure you create a client secret and save this value.

5) Note down the following details about your Entra ID application:

* Application (client) ID
* Directory (tenant) ID
* Client secret

6) Now the Entra ID application will need to be authorized in Dynamics 365 Business Central. Go to the Admin Center in Dynamics 365 Business Central and ensure the application you created is listed in Microsoft Entra Apps. You should see the Application (client) ID listed with Admin consent granted. If you do not see the application here, Authorize the application here.

7) In Dynamics 365 Business Central, click on the search box and look for "Microsoft Entra Applications". Click New and enter your Application (client) ID. Ensure the application is Enabled. Under User Permission Sets, ensure it has the proper permissions for the API calls you will be making. You can give it admin permissions with the following set:

* D365 FULL ACCESS

8) See the following resources for more documentation about setting up this flow.

* [Blog about service to service authentication](https://www.kauffmann.nl/2021/07/06/service-to-service-authentication-in-business-central-18-3-how-to-set-up/)
* [Setup Microsoft Entra ID](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-develop-connect-apps#set-up-microsoft-entra-id-based-authentication)

## How to run

1) Install python dependencies

```
pip3 install -r requirements.txt
```

1) Set the following environment variables or create an .env file:

* Q_INDEX_ID - Q index id
* Q_DATASOURCE_ID - Q datasource id
* Q_APPLICATION_ID - Q application id
* DYNAMICS_CLIENT_ID - Entra ID client id
* DYNAMICS_AUTHORITY - Entra ID Authority, i.e. https://login.microsoftonline.com/{tenanid}
* DYNAMICS_SECRET - Entra ID client secret
* DYNAMICS_SCOPE - Entra ID scope, i.e. https://api.businesscentral.dynamics.com/.default
* DYNAMICS_COMPANY_ID - Dynamics Business Central company id

2) Run `examples/dynamics/connector.py` to sync sales invoices between Dynamics 365 and Amazon Q for Business. `python3 connector.py`

## Adding additional capabilities to the connector
Currently the connector only has provisions to sync sales invoices from Dynamics 365 Business Central. If you wish to sync additional objects, you will need to confirm the API calls that will be required to retrieve those objects. You can do that by consulting the following [Open API 1.0 Reference](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/api-reference/v1.0/dynamics-open-api)

1) Once you have determined the API calls, you can add a new class to the examples directory. Use the existing `examples/dynamics/salesinvoices.py` as a template for the new class.

2) The `salesinvoices` class inherits from the `dynamics_connector` and `generic_connector` class in `common.py`. The `dynamics_connector` and `generic_connector` has the following common functions that can be utilized for performing a sync between Dynamics 365 Business Central and Amazon Q for Business:

* uploadDocuments (generic_connector) - Will upload a batch (max 10) of documents to Amazon Q for Business.
* callSourceAPI (generic_connector) - Will call the API and return a response.
* getAccessToken (dynamics_connector) - This function is overriden in the dynamics_connector class. Will get an access token using the msal library (Specific to Dynamics 365).

3) Your new class will need to implement the `get_docs` function which will call the Business Central APIs and upload documents to Amazon Q for Business.

## Scaling Considerations

The current `salesinvoices` class and `get_docs` implementation gets all the sales invoices from Business Central and uploads them to Amazon Q for Business. A way to get only a subset of the sales invoices or any Business Central objects should be implemented for scalability issues. There are several provisions in the Business Central APIs for filtering or deltalinks which should be explored.

* [Filtering documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-connect-apps-filtering)
* [Deltalink documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-connect-apps-delta)