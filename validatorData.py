import os
import subprocess
import pandas as pd
from datetime import datetime
import streamlit as st
import time

# File paths
output_file = "/Users/hkarri/Desktop/repositories/gitlab/block-monitoring/results.csv"
log_file = "/Users/hkarri/Desktop/repositories/gitlab/block-monitoring/collect_results.log"
script_dir = os.path.dirname(os.path.abspath(__file__))

def log_message(message):
    """ Append messages to the log file. """
    with open(log_file, "a") as log:
        log.write(f"{message}\n")

def run_command(command):
    """ Execute a shell command and return its output. """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def collect_data():
    """ Collect data and write it to the CSV file. """
    log_message(f"Starting data collection at {datetime.now()}")

    # Change to the script's directory
    os.chdir(script_dir)

    # Write the header to the CSV file
    header_command = "btcli subnet metagraph --netuid 1"
    header_output = run_command(header_command)
    header_lines = header_output.splitlines()
    
    header_line = ""
    for line in header_lines:
        if "UID" in line:
            header_line = line
            break
    
    if header_line:
        header_file = ','.join(header_line.split()).strip(',')
        with open(output_file, "w") as f:
            f.write(f"Subnet ID,{header_file}\n")
    
    # Loop through values 1 to 5
    for netuid in range(1, 6):
        result_command = f"btcli subnet metagraph --netuid {netuid}"
        result_output = run_command(result_command)
        result_lines = result_output.splitlines()
        
        result_line = ""
        for line in result_lines:
            if "5HEo565WAy" in line:
                result_line = line
                break
        
        if result_line:
            result = ','.join(result_line.split()).strip(',')
            with open(output_file, "a") as f:
                f.write(f"{netuid},{result}\n")
    
    log_message(f"Data collection completed at {datetime.now()}")

def load_data():
    """ Load data from the CSV file into a DataFrame. """
    return pd.read_csv(output_file)

def main():
    """ Main function to run the Streamlit app. """
    # Title of the app
    st.title('Subnet Data Viewer')

    while True:
        with st.spinner('Validator results are being fetched from Bittensor CLI...'):
            # Collect data
            collect_data()

        # Display the dataframe
        st.write("Data Preview:")
        try:
            df = load_data()
            st.dataframe(df, use_container_width=True)

            # Optionally: display a chart for visual representation
            st.write("Last updated time was ", datetime.now())

            if 'UPDATED' in df.columns:
                st.bar_chart(df['UPDATED'], use_container_width=True)
            
            # New section: Display subnet IDs and UPDATED values where UPDATED > 1000
            st.write("Subnet IDs with UPDATED > 1000:")
            if 'UPDATED' in df.columns:
                filtered_df = df[df['UPDATED'] > 1000][['Subnet ID', 'UPDATED']]
                st.dataframe(filtered_df, use_container_width=True)

        except FileNotFoundError:
            st.error("The file `results.csv` was not found.")
        
        # Refresh every 5 minutes
        st.write("Refreshing every 5 minutes...")
        time.sleep(300)  # Sleep for 5 minutes
        st.rerun()  # Force Streamlit to rerun the script

if __name__ == "__main__":
    main()
