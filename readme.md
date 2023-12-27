# Azure Cloud Challenge Backend Function App

Python HTTP Trigger for an Azure Function App. This code is part of the Azure Cloud Challenge and pulls a value from an Azure Cosmos DB, which represents a counter. The counter is incremented and returned. The output of this function is handled by JavaScript on the frontend site to display a visitor counter. 

To replicate this, you will need AzureCosmosDBConnectionString in the application settings of the function app which holds the connection string to your Cosmos DB instance.