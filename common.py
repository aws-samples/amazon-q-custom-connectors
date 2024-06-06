import msal
import logging
import requests
from urllib.request import Request, urlopen

class generic_connector:
    def __init__(self, config, q_business):
        self.config = config
        self.q_business = q_business

    def uploadDocuments(self, documents):
        logging.info("---------------")
        #batchput docs
        batch_put_document_result = self.q_business.batch_put_document(
                applicationId= self.config['application_Id'],
                dataSourceSyncId= self.config['job_execution_id'],
                indexId= self.config['index_id'],
                documents = documents
        )
        logging.info("Calling batch_put_document for batch.")
        logging.debug(batch_put_document_result)

    def callSourceAPI(self, access_token, url, addHeaders):
        req = Request(url)
        req.add_header("Authorization", "Bearer "+access_token)
        for k,v in addHeaders.items():
            req.add_header(k, v)
        content = urlopen(req).read()
        return content

    def getAccessToken(self):
        token_data = {
            "grant_type": "client_credentials",
            "client_id": self.config['client_id'], 
            "client_secret": self.config['secret']
        }
        token_response = requests.post(self.config['token_url'], data=token_data)
        access_token_result = token_response.json()
        return access_token_result


class dynamics_connector(generic_connector):
    def getAccessToken(self):
        result = None
        try:
            app = msal.ConfidentialClientApplication(
                self.config["client_id"], authority=self.config["authority"],
                client_credential=self.config["secret"])

            result = app.acquire_token_silent(self.config["scope"], account=None)

            if not result:
                logging.info("No suitable token exists in cache. Let's get a new one from Azure AD.")
                result = app.acquire_token_for_client(scopes=self.config["scope"])
        except Exception as e:
            logging.error("Error getting access token.")
            logging.error(e)
        return result