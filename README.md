# Creating a Stock Screener on Google Cloud Platform

This repository has code to deploy a stock screening app to Google Cloud Platform. The stock screener scrapes through reddit to find the three most mentioned stocks on reddit forums "investing", "wallstreetbets" and "stocks", calculate the sentiment on reddit and create a summary for each stock. The stock screener is programmed to run everyday at 10.30 pm in Google Cloud. The code is deployed to Google Cloud Run using Terraform. 

## Google Cloud Workflow Diagram

The diagram below shows the GCP infrastructure created by the code. We use the Gcloud scheduler api to run the code deployed to Google Cloud Run everyday at 10.30pm. The results are then daily saved in storage buckets. 

![Stock Screener Flowchart](https://user-images.githubusercontent.com/85404022/210032756-842df8c5-57eb-41d7-a5a3-736ca7247e49.png)

## Resulting Summary

Below is an example page from the PDF created by the infrastructure. The resulting PDF contains the top 3 mentioned stocks in reddit and shows the sentiment, analyst recommendations, put/call ratio etc.

![Capture](https://user-images.githubusercontent.com/85404022/210092435-cc15b69a-94c1-4e21-abb7-e410128de49d.PNG)
