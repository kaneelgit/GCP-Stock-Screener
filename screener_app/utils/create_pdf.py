"""
Author - Kaneel Senevirathne
Date - 12/27/2022
"""

from utils.yf_utils import stock_info
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class create_pdf:
    def __init__(self, stock_list, stock_senti):
        
        #get stock list
        self.stock_list = stock_list
        self.stock_senti = stock_senti

        #date today
        td = datetime.today()
        td_str = f'{td.month}_{td.day}_{td.year}'

        #initialize PDF
        self.pdf = FPDF()

        #create data for each stock
        for i, stock in enumerate(stock_list):
            self.create_page(stock, stock_senti[i])

        self.pdf.output(f'results/watchlist_{td_str}.pdf', 'F')

    def create_page(self, stock, sentiment):
        """
        Creates pdf
        """
        #get stock details from yfinance
        stock_details = stock_info(stock)
        #create stock history
        fig_dir = self.create_history_img(stock, stock_details['price_history'])
        rec_dir = self.create_rec_img(stock, stock_details['recommendations'])
        pc_dir = self.create_pc_img(stock, stock_details['p2c_ratio'])

        #start creating the page
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 18)
        self.pdf.cell(40, 10, stock, 0, 1)
        
        #Number of reddit mentions
        self.pdf.set_font('Arial', '', 14)
        self.pdf.cell(40, 10, f"Mentions: {10}")
        
        #sentiment score
        sentiment_score = np.round(sentiment, 2)
        r, g, b = self.get_color(sentiment_score)
        self.pdf.cell(130, 10, "Sentiment score:", align = 'R')
        self.pdf.set_text_color(r = r, g = g, b = b)
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.cell(140, 10, f"{sentiment_score}", align = "L")

        #change font back
        self.pdf.set_font('Arial', '', 14)
    
        #create the image in the pdf
        self.pdf.image(fig_dir, x = 10, y = 40, w = 170, h = 90, type = '', link = '')

        #create price predictions
        for i in range(12):
            self.pdf.cell(140, 10, "", 0, 1)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(140, 10, "Price Targets", 0, 1)
        self.pdf.set_font('Arial', '', 14)
        self.pdf.cell(140, 10, "", 0, 1)
        #add the pie chart
        self.pdf.image(rec_dir, x = 90, y = 135, w = 115, h = 85, type = '', link = '')
        
        #print out the target prices
        df_target = stock_details['price_targets']

        for i in range(len(df_target)):
            self.pdf.cell(140, 10, f"{df_target.index[i]}: {df_target.values[i][0]}", 0, 1)

        #put to call ratio
        self.pdf.cell(140, 10, "", 0, 1)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(140, 10, "Put to Call Ratio", 0, 0)
        self.pdf.set_font('Arial', '', 14)
        
        #create p2c ratio image
        self.pdf.image(pc_dir, x = 10, y = 230, w = 170, h = 63, type = '', link = '')


    def get_color(self, score):
        
        if score < 0:
            r = 255 - 255 * score/4
            g, b = 0, 0
        if score > 0:
            g = 255 - 255 * score/4
            r, b = 0, 0
        if score == 0:
            r, g, b = 50.2, 50.2, 50.2

        return r, g, b

    def create_history_img(self, stock, history):
        """
        Create image with history
        """
        plt.figure(figsize = (10, 4))
        plt.plot(history.index, history['Close'])
        plt.ylabel('Stock Price')
        plt.xticks(rotation = 45)
        fig_dir = f"results/{stock}_history.png"
        plt.savefig(fig_dir, bbox_inches = "tight")

        return fig_dir

    def create_rec_img(self, stock, df_rec):
        """
        Create recommendations pie chart
        """
        
        pec = df_rec.max() * 0.025
        df_rec = df_rec[df_rec > pec]
        plt.figure()
        df_rec.plot.pie(autopct="%1.1f%%", figsize = (6, 6))
        fig_dir = f"results/{stock}_rec.png"
        plt.savefig(fig_dir, bbox_inches = "tight")

        return fig_dir

    def create_pc_img(self, stock, pc_ratios):
        """
        Create put to call ratio plot
        """
        
        dates = [v[0] for v in pc_ratios]
        pc_ratios = [v[1] for v in pc_ratios]

        plt.figure(figsize = (10, 4))
        plt.plot(dates, pc_ratios)
        plt.ylabel('Put/Call')
        plt.xticks(rotation = 45)
        fig_dir = f"results/{stock}_pc.png"
        plt.savefig(fig_dir, bbox_inches = "tight")

        return fig_dir


