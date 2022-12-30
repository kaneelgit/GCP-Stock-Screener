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
    csv_bucket = storage_client.get_bucket('screener_csv_bucket') #add csv bucket name here
    pdf_bucket = storage_client.get_bucket('screener_pdf_bucket') #add the pdf bucket name here

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
    if request.method == 'POST':

        run_process()
        
        return ("", 204)

    else:

        return ("", 400)





