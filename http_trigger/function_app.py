import os
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
from azure.identity import ManagedIdentityCredential
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

COSMOS_DB_ENDPOINT = os.environ['AzureCosmosDBEndpoint']
MANAGED_IDENTITY_CLIENT_ID = os.environ['MANAGED_IDENTITY_CLIENT_ID']
CREDENTIAL = ManagedIdentityCredential(client_id=MANAGED_IDENTITY_CLIENT_ID)
COSMOS_CLIENT = CosmosClient(COSMOS_DB_ENDPOINT, CREDENTIAL)
DATABASE = COSMOS_CLIENT.get_database_client("heyitsadam")
CONTAINER = DATABASE.get_container_client("counter")

@app.function_name(name="http_trigger")
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    count = 0
    query = f"SELECT * FROM c WHERE c.id = '1'"
    try:
        for item in CONTAINER.query_items(query=query, enable_cross_partition_query=True):
            updated_item = item
            count = int(item['count'])
            count += 1
            updated_item['count'] = str(count)
            CONTAINER.upsert_item(item, updated_item)
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"An error occurred: {e.status_code} - {e.message}")
        count = e.message

    return func.HttpResponse(body=str(count), status_code=200)