# Nifty Option Chain Realtime PCR (Put-Call Ratio) Tracker

GitHub Project Description:

**Overview:**
PCR Tracker is a Python-based tool for monitoring the Put-Call Ratio (PCR) in the NIFTY option chain. The project actively scrapes data from the NSE website, processes it, and calculates the PCR in real-time. The tool focuses on providing insights into the options market sentiment by analyzing changes in Open Interest (OI) for both Put and Call options.

**Features:**
- **Real-time Data Scraping:** Utilizes the NSE Website to fetch the latest option chain data for NIFTY.
- **Data Processing:** Extracts relevant information, filtering for Calls and Puts, and organizes the data for analysis.
- **PCR Calculation:** Computes the Put-Call Ratio based on changes in Open Interest for corresponding strike prices.
- **Dynamic Tracking:** Actively tracks and stores changes in Put and Call OI, providing a historical perspective.
- **User-friendly Output:** Prints incremental changes in Put OI, Call OI, and the overall PCR for each iteration.

**Under Development:**
- **Hidden Entries:** Ongoing work to enhance output by suppressing entries with no change (new entries with change = 0).
- **Options Trading Trends:** Future features to approximate whether there is active Put or Call buying/writing and analyze the overall trend.

**Usage:**
1. Clone the repository.
2. Execute the script to initiate real-time tracking.
3. Observe the console output for incremental changes in Put OI, Call OI, and PCR.

**Note:**
The project is actively under development, and additional features are being added regularly. Feel free to contribute or provide feedback to help improve and expand the functionality of the PCR Tracker.

**Disclaimer:**
This tool is for informational purposes only and should not be considered financial advice. Always perform your own research before making any investment decisions.

*Happy tracking!* 📈✨
