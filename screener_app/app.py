"""
Author - Kaneel Senevirathne
Date - 12/28/2022
"""
import base64
import json
import os

from flask import Flask, request
from utils import yf_utils, create_pdf, reddit_utils, credentials

import pandas as pd
from datetime import datetime

from google.cloud import storage

storage_client = storage.Client()

#helper functions
def run_process():

    #first scrape data from reddit
    reddit_utils.scrape_data(credentials.client_id, credentials.secret, credentials.user_id)

    #load the file
    td = datetime.today()
    td_str = f'{td.month}_{td.day}_{td.year}'

    #load dataframe
    df_reddit = pd.read_csv(f'results/results_{td_str}.csv')
    df_reddit = df_reddit.sort_values(by = [f'count_{td_str}'], ascending = False)
    
    #top 3 mentioned stocks
    top_stocks = df_reddit[:3]['index'].to_list()
    stock_senti = df_reddit[:3][f'sentiment_{td_str}'].to_list()

    #create pdf
    create_pdf.create_pdf(top_stocks, stock_senti)

    #upload csv and pdf names
    upload_csv = f'results_{td_str}.csv'
    upload_pdf = f'watchlist_{td_str}.pdf'

    #upload files
    csv_bucket = storage_client.get_bucket('csv_output_bucket') #add csv bucket name here
    pdf_bucket = storage_client.get_bucket('pdf_output_bucket') #add the pdf bucket name here

    #upload csv file
    csv_blob = csv_bucket.blob(upload_csv)
    with open(f"results/{upload_csv}", "rb") as output_csv:
        csv_blob.upload_from_file(output_csv)

    #upload the pdf
    pdf_blob = pdf_bucket.blob(upload_pdf)
    with open(f"results/{upload_pdf}", "rb") as output_pdf:
        pdf_blob.upload_from_file(output_pdf)
        

#create flask app
app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    # Decode the Pub/Sub message.
    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        try:
            data = json.loads(base64.b64decode(pubsub_message["data"]).decode())

        except Exception as e:
            msg = (
                "Invalid Pub/Sub message: "
                "data property is not valid base64 encoded JSON"
            )
            print(f"error: {e}")
            return f"Bad Request: {msg}", 400

        # Validate the message is a Cloud Storage event.
        if not data["name"] or not data["bucket"]:
            msg = (
                "Invalid Cloud Storage notification: "
                "expected name and bucket properties"
            )
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        try:
            print('worked up to here')
            run_process()
            return ("", 204)

        except Exception as e:
            print(f"error: {e}")
            return ("", 500)

    return ("", 500)

