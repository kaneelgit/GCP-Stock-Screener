# Creating a Stock Screener on Google Cloud Platform

This repository has code to deploy a stock screening app to Google Cloud Platform. The stock screener scrapes through reddit to find the three most mentioned stocks on reddit forums "investing", "wallstreetbets" and "stocks", calculate the sentiment on reddit and create a summary for each stock. The stock screener is programmed to run everyday at 10.30 pm in Google Cloud. The code is deployed to Google Cloud Run using Terraform. 

## Google Cloud Workflow Diagram

The diagram below shows the GCP infrastructure created by the code. We use the Gcloud scheduler api to run the code deployed to Google Cloud Run everyday at 10.30pm. The results are then daily saved in storage buckets. 

![Stock Screener Flowchart](https://user-images.githubusercontent.com/85404022/210032756-842df8c5-57eb-41d7-a5a3-736ca7247e49.png)

<a href="https://cloud.google.com/run">Google Cloud Run</a>, <a href="https://cloud.google.com/scheduler">Google Cloud Scheduler</a>, <a href = "https://cloud.google.com/container-registry">Google Cloud Container Registry</a>, <a href = "https://cloud.google.com/storage">Google Cloud Storage</a> are the billable resources used in this project. 

## Output

Below is an example page from the PDF created by the infrastructure. The resulting PDF contains the top 3 mentioned stocks in reddit and shows the sentiment, analyst recommendations, put/call ratio etc.

![Capture](https://user-images.githubusercontent.com/85404022/210092435-cc15b69a-94c1-4e21-abb7-e410128de49d.PNG)

## Setup & Requirements

In order to setup and run the code, you will need a billing enabled Google Cloud Platform (GCP) account. You will also need to have GCP command line interface (CLI) properly, terraform and docker properly setup in your local environment. The following are some useful resources on how to setup a Google Cloud account and install the above mentioned software locally. Additionally, you will also need a Reddit API key to access reddit.

1. <a href = "#">Google Cloud Platform</a>
2. <a href = "https://cloud.google.com/sdk/docs/install">Gcloud CLI</a>
3. <a href = "https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli">Terraform</a>
4. <a href = "https://docs.docker.com/get-docker/">Docker</a>
5. <a href = "https://www.reddit.com/wiki/api/">Reddit API</a>





## Run Code


## Destroy Infrastructure



## Other details
