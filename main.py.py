import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

class PCRScrapper:
    def __init__(self):
        self.OI_change_dict = {}
        self.previous_timestamp = ""

    def fetch_data(self):
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"                               #pulling nifty option chain data from NSe website
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["records"]["data"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def process_data(self, data):
        oc_data = []                                                                                        #There is a lot of data, We only want rows for Calls and Puts
        for i in data:
            for j, k in i.items():
                if j == "CE" or j == "PE":
                    info = k
                    info["instrumentType"] = j
                    oc_data.append(info)
        df = pd.DataFrame(oc_data)
        return df

    def filter_data(self, df):
        expiry = 1                                                                                          #1 means current expiry, 2 means next expiry and so on...
        dates_np_array = pd.DataFrame(df["expiryDate"].unique())
        dates_np_array.columns = ["OG_DATES"]
        dates_np_array["CONVERTED_DATES"] = pd.to_datetime(dates_np_array["OG_DATES"])
        todays_date = pd.Timestamp.today()
        mask = dates_np_array["CONVERTED_DATES"] >= todays_date
        expiry_series_selection = dates_np_array[mask].sort_values(by="CONVERTED_DATES").reset_index().loc[
            expiry, "OG_DATES"]
        df = df[df["expiryDate"] == expiry_series_selection]

        underlying_value = df["underlyingValue"].unique()[0]
        upper_range = underlying_value + 350                                                                #We want all data for strikes +-350 of the current strike price
        lower_range = underlying_value - 350

        strike_price_mask = (df["strikePrice"] >= lower_range) & (df["strikePrice"] <= upper_range)
        df = df[strike_price_mask]

        pe_mask = df["instrumentType"] == 'PE'
        pe_df = df[pe_mask]                                                                                 #sepearting the Calls and Puts dataframe and bringing it in same line, originally its aligned one below other
        ce_df = df[~pe_mask]

        return pe_df, ce_df

    def calculate_pcr(self, pe_df, ce_df):                                                                  #This is our main piece of code, Inserts data into dictionary if it does not already exists and shows comparisions incrementally if items exist in dictionary
        final_df = pe_df.merge(ce_df, on="strikePrice")
        final_df["PCR_OI"] = final_df["changeinOpenInterest_x"] / final_df["changeinOpenInterest_y"]
        current_timestamp = datetime.now().strftime("%H - %M- %S")

        if not self.OI_change_dict:
            self.OI_change_dict[current_timestamp] = {"initial_change_in_put_OI": final_df["openInterest_x"].sum(),
                                                       "initial_Change_in_call_OI": final_df["openInterest_y"].sum(),
                                                       "initial_sum_of_PCR": final_df["PCR_OI"].sum()}
        else:
            self.OI_change_dict[current_timestamp] = {"initial_change_in_put_OI": self.OI_change_dict.get(self.previous_timestamp, {}).get(
                "initial_change_in_put_OI", 0) - final_df["openInterest_x"].sum(),
                                                       "initial_Change_in_call_OI": self.OI_change_dict.get(self.previous_timestamp, {}).get(
                                                           "initial_Change_in_call_OI", 0) - final_df["openInterest_y"].sum(),
                                                       "initial_sum_of_PCR": self.OI_change_dict.get(self.previous_timestamp, {}).get(
                                                           "initial_sum_of_PCR", 0) - final_df["PCR_OI"].sum()}

        print(self.OI_change_dict[current_timestamp])
        self.previous_timestamp = str(current_timestamp)

    def run(self):
        while True:                                                                                         #Never ending loop until stopped
            try:
                data = self.fetch_data()
                if data:
                    df = self.process_data(data)
                    pe_df, ce_df = self.filter_data(df)
                    self.calculate_pcr(pe_df, ce_df)
            except Exception as e:
                print(f"Error in main loop: {e}")

            time.sleep(30)                                                                                  #30 means refresh data every 30 seconds, adjust this paramter as per requirements (in seconds)

if __name__ == "__main__":
    pcr_scrapper = PCRScrapper()                                                                            #Inititlizing the class and running the function
    pcr_scrapper.run()
