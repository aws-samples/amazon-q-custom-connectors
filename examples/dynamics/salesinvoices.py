
import sys
import logging
import json
import time
sys.path.append("../../")
from common import dynamics_connector

class salesinvoices(dynamics_connector):
    def get_docs(self):
        documents = []
        salesInvoices = []

        tokenResult = self.getAccessToken()

        salesInvoiceResult = None
        try:
            logging.info("Getting sales invoices from Dynamics 365 Business Central.")
            salesInvoicesURL = f"https://api.businesscentral.dynamics.com/v2.0/production/api/v2.0/companies({self.config['companyid']})/salesInvoices?$expand=pdfDocument"
            content = self.callSourceAPI(tokenResult["access_token"], salesInvoicesURL, {})
            salesInvoiceResult = json.loads(content)
            salesInvoices = salesInvoiceResult['value']
            logging.info(f"Found {len(salesInvoices)} sales invoices.")
        except Exception as e:
            logging.error("Error getting sales invoices from Dynamics 365 Business Central.")
            logging.error(e)
            return

        for x in salesInvoices:
            getPDFFileLink = x['pdfDocument']['pdfDocumentContent@odata.mediaReadLink']
            content = self.callSourceAPI(tokenResult["access_token"], getPDFFileLink, {})
            filename = x['number'] + ".pdf"
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
                            "stringValue":"Sales Invoices"
                        }
                    }
                ],
            }
            if len(documents) >= 10:
                self.uploadDocuments(documents)
                documents = []
            documents.append(doc)
            time.sleep(1)

        if len(documents) > 0:
            self.uploadDocuments(documents)
            documents = []