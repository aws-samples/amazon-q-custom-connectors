import sys
import logging
import json
import time
sys.path.append("../../")
from common import generic_connector

class generic(generic_connector):
    def get_docs(self):
        documentBatch = []
        tokenResult = self.getAccessToken()
        try:
            logging.info("Getting documents from mock API Server.")
            mockAPIServerURL = "http://127.0.0.1:5000/getListDocs"
            content = self.callSourceAPI(tokenResult["access_token"], mockAPIServerURL, {})
            documentsResult = json.loads(content)
            documents = documentsResult['documents']
            logging.info(f"Found {len(documents)} documents.")
        except Exception as e:
            logging.error("Error getting documents from mock API Server.")
            logging.error(e)
            return

        for x in documents:
            getPDFFileLink = f"http://127.0.0.1:5000/getDoc?name={x['name']}"
            content = self.callSourceAPI(tokenResult["access_token"], getPDFFileLink, {})
            filename = x['name']
            logging.info(f"Adding {filename} to upload batch.")
            doc = {
                "id": filename,
                "contentType":"PDF",
                "title": filename,
                "content": {
                    "blob": content
                },
                "attributes": [ 
                    { 
                        "name": "_category",
                        "value": {
                            "stringValue":"Documents"
                        }
                    }
                ],
            }
            if len(documentBatch) >= 10:
                self.uploadDocuments(documentBatch)
                documentBatch = []
            documentBatch.append(doc)
            time.sleep(1)

        if len(documentBatch) > 0:
            self.uploadDocuments(documentBatch)
            documentBatch = []