import sys
sys.path.append("./src")

import boto3
import os
import logging
import json
import time
import requests
from urllib.request import Request, urlopen

logging.basicConfig(level="INFO")

def lambda_handler(event, context):
    config = {}
    # Q Business Configurations
    config["index_id"] = os.getenv('Q_INDEX_ID')
    config["data_source_id"] = os.getenv('Q_DATASOURCE_ID')
    config["application_Id"] = os.getenv('Q_APPLICATION_ID')

    # Generic oAuth2 Configurations
    config["client_id"] = os.getenv('OAUTH2_CLIENT_ID')
    config["secret"] = os.getenv('OAUTH2_SECRET')
    config['token_url'] = os.getenv('OAUTH2_TOKEN_URL')

    # Generic Data source URL
    config['datasource_url'] = os.getenv('GENERIC_DATASOURCE_URL')

    q_business = boto3.client('qbusiness')

    # Begin: Start a data source sync job

    # End: Start a data source sync job

    logging.info("Start data source sync operation.")

    # Obtain the job execution ID from the result
    job_execution_id = result['executionId']
    logging.info("Job execution ID: "+job_execution_id)
    config['job_execution_id'] = job_execution_id

    genericClient = generic(config, q_business)

    # Start ingesting documents
    try:
        # Part of the workflow will require you to have a list with your documents ready
        # for ingestion
        genericClient.get_docs()

    # Begin: Stop data source sync job
    finally:

    # End: Stop data source sync job

class generic:
    def __init__(self, config, q_business):
        self.config = config
        self.q_business = q_business

    def uploadDocuments(self, documents):
        # Begin: Upload documents to Q Business custom connector data source
       
        # End: Upload documents to Q Business custom connector data source

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

    def get_docs(self):
        documents = []
        documentBatch = []
        tokenResult = self.getAccessToken()
        try:
            # Begin: Getting document list from mock API Server

            # End: Getting document list from mock API Server
        except Exception as e:
            logging.error("Error getting documents from mock API Server.")
            logging.error(e)
            return
 
        for x in documents:
            # Begin: Download document from mock API Server
            
            # End: Download document from mock API Server
            # Begin: Format document content for ingestion
            
            # End: Format document content for ingestion
            # Begin: Add document to batch or upload the document batch
            
            # End: Add document to batch or upload the document batch
            
        if len(documentBatch) > 0:
            self.uploadDocuments(documentBatch)
            documentBatch = []
        
