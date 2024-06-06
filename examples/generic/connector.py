import boto3
import os
import logging
import sys
from dotenv import load_dotenv
from generic import generic

load_dotenv()

logging.basicConfig(level="INFO")

if __name__=="__main__": 
    config = {}
    # Q Business Configurations
    config["index_id"] = os.getenv('Q_INDEX_ID')
    config["data_source_id"] = os.getenv('Q_DATASOURCE_ID')
    config["application_Id"] = os.getenv('Q_APPLICATION_ID')

    # Generic oAuth2 Configurations
    config["client_id"] = os.getenv('OAUTH2_CLIENT_ID')
    config["secret"] = os.getenv('OAUTH2_SECRET')
    config['token_url'] = os.getenv('OAUTH2_TOKEN_URL')

    q_business = boto3.client('qbusiness')

    #Start a data source sync job
    result = q_business.start_data_source_sync_job(
            applicationId=config["application_Id"],
            dataSourceId=config["data_source_id"],
            indexId=config["index_id"]
    )

    logging.info("Start data source sync operation.")

    #Obtain the job execution ID from the result
    job_execution_id = result['executionId']
    logging.info("Job execution ID: "+job_execution_id)
    config['job_execution_id'] = job_execution_id

    genericClient = generic(config, q_business)

    #Start ingesting documents
    try:
        #Part of the workflow will require you to have a list with your documents ready
        #for ingestion
        genericClient.get_docs()

    #Stop data source sync job
    finally:
        # Stop data source sync
        result = q_business.stop_data_source_sync_job(
            applicationId=config["application_Id"],
            dataSourceId=config["data_source_id"],
            indexId=config["index_id"]        
        )
        logging.info("Stop data source sync operation.")
        logging.debug(result)