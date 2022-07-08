# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""File for all Azure-related functionality"""
import sys
from datetime import datetime, timedelta

from time import sleep
try:
    from azure.storage.blob import (BlobServiceClient, 
                                    AccountSasPermissions, 
                                    generate_blob_sas, 
                                    generate_container_sas)
except ImportError:
    print("You need to install"
           " the 'Azure Storage Blobs client library for Python' library."
           " Try: pip install azure-storage-blob")
    sys.exit(1)
    
def create_blob_sas_token(
        azure_storage_account_name,
        azure_storage_account_key,
        container_name,
        blob_name,
        sas_token_hours):
    """Creates a read only sas token to a blob"""
    max_retries = 3
    retry_count = 0
    while True:
        try:
            today = datetime.utcnow()
            expiration_date = (today + timedelta(hours=sas_token_hours)).replace(microsecond=0)

            # Read access only to this particular blob
            sas_token = generate_blob_sas(
                account_name= azure_storage_account_name,
                container_name= container_name,
                blob_name= blob_name,
                account_key= azure_storage_account_key,
                expiry= expiration_date,
                permissions=AccountSasPermissions(read=True)            )

            return sas_token
        except Exception as exc:
            retry_count += 1
            if retry_count > max_retries:
                print("Azure storage error: " + str(exc))
                sys.exit(200)
            message = str(exc)
            print(message)
            sleep(1)

def create_container_sas_token(
        azure_storage_account_name,
        azure_storage_account_key,
        container_name,
        sas_token_hours,
        write_access=False,
        list_access=True):
    """ Creates an Azure SAS token from the given name + key """
    max_retries = 3
    retry_count = 0
    while True:
        try:
            service = BlobServiceClient.from_connection_string(
                "DefaultEndpointsProtocol=https;AccountName={azure_storage_account_name};AccountKey={azure_storage_account_key}")

            expiration_date = (datetime.utcnow() + timedelta(hours=sas_token_hours)).replace(microsecond=0)

            service.create_container(container_name)
            

            sas_token = generate_container_sas(
                account_name= azure_storage_account_name,
                container_name= container_name,
                account_key= azure_storage_account_key,
                expiry= expiration_date,
                permissions= AccountSasPermissions(read=True,
                                                   list=list_access,
                                                   delete=write_access,
                                                   write=write_access))
            return sas_token
        except Exception as exc:
            retry_count += 1
            if retry_count > max_retries:
                print("Azure storage error: " + str(exc))
                sys.exit(200)
            message = str(exc)
            print(message)
            sleep(1)
