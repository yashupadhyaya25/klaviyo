from azure.storage.blob import BlobServiceClient

class AZURE:
    def __init__(self, account_name, account_key, container_name):
        self.container_name = container_name
        self.account_name = account_name
        self.account_key = account_key

    def get_blob_client(self) :
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        return blob_service_client
    
    def upload_to_blob(self,blob_client_obj,local_file_path,blob_name,sub_folder_name) :
        blob_client = blob_client_obj.get_blob_client(container=self.container_name, blob=f"{sub_folder_name}/{blob_name}")
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)