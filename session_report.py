from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import PySimpleGUI as sg
import os
import pickle


def runJob(file):

    try:
        with open(file) as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
    except Exception as e:
        print(e)

    try:
        find_table = soup.find_all('table')
        rows = find_table[0].find_all('tr')
    except Exception as e:
        print(e)

    results = []

    session = find_table[0].find_all(class_='sessionDetails')

    job_description = find_table[0].find_all(class_="jobDescription")

    for i in rows:
        table_data = i.find_all('td')
        data = [j.text.strip() for j in table_data]
        results.append(data)


    new_table = pd.DataFrame(results)

    # Strip back to just the required columns
    new_table = new_table.iloc[:,0:9]
    # Name the columns
    new_table.columns = ['Name', 'Status', 'Start Time', 'End Time', 'Size', 'Read', 'Transferred', 'Duration', 'Details']

    # Filter out the everything apart without Success or Error
    new_table = new_table[(new_table['Status'].str.contains('Success')) | (new_table['Status'].str.contains('Error')) | (new_table['Status'].str.contains('Warning'))]

    # drop the nan 
    new_table = new_table.dropna()

    # a bunch of splits
    new_table[['Size', 'Size Metric']] = new_table['Size'].str.split(expand=True)
    new_table[['Read', 'Read Metric']] = new_table['Read'].str.split(expand=True)
    new_table[['Transferred', 'Transfer Metric']] = new_table['Transferred'].str.split(expand=True)
    new_table['Name'] = new_table['Name'].str.split(expand=True)[0]
    new_table['End Time'] = new_table['End Time'].str.split(expand=True)[0]
    new_table['Start Time'] = new_table['Start Time'].str.split(expand=True)[0] # just in case

    # change the types
    new_table['Size'] = new_table['Size'].astype(float)
    new_table['Read'] = new_table['Read'].astype(float)
    new_table['Transferred'] = new_table['Transferred'].astype(float)
    new_table['Start Time'] = pd.to_datetime(new_table['Start Time'])
    new_table['End Time'] = pd.to_datetime(new_table['End Time'])

    # update the capacities to GB
    new_table['Size'] = np.where(new_table['Size Metric'] == 'TB', new_table['Size'] * 1024, new_table['Size']) # assumes source will only be TB or GB
    new_table['Read'] = np.where(new_table['Read Metric'] == 'TB', new_table['Read'] * 1024, new_table['Read'])
    new_table['Read'] = np.where(new_table['Read Metric'] == 'MB', new_table['Read'] / 1024, new_table['Read']) # just in case
    new_table['Transferred'] = np.where(new_table['Transfer Metric'] == 'MB', new_table['Transferred'] / 1024, new_table['Transferred'])
    new_table['Transferred'] = np.where(new_table['Transfer Metric'] == 'TB', new_table['Transferred'] * 1024, new_table['Transferred']) # just in case

    new_table = new_table.drop(['Size Metric', 'Read Metric', 'Transfer Metric'], axis=1)

    global_df = pd.read_pickle('./data.pkl')    

    frames = [global_df, new_table]

    global_df = pd.concat(frames)

    global_df.to_pickle('./data.pkl')


if __name__ == '__main__':
    global_df = pd.DataFrame(columns=['Date','Name', 'Status', 'Start Time', 'End Time', 'Size', 'Read', 'Transferred', 'Duration', 'Details'])

    # delete pickle file if it still exists from a previous run
    if os.path.exists('data.pkl'):
        os.remove('data.pkl')
    
    global_df.to_pickle('./data.pkl')
    
    directory = sg.popup_get_folder('Please select folder')

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            try:
                path = directory + '/' + filename
                print(f"Processing {filename}")
                runJob(path)
            except:
                print(f"file {filename} did not work")
                with open("error_files.txt", "a") as error_files:
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    error_files.write(f"{now_time}: {filename}\n")

    global_df2 = pd.read_pickle('./data.pkl')

    global_df2.reset_index(drop=True, inplace=True)

    now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    global_df2.to_excel(f"results-{now_time}.xlsx")

    if os.path.exists("data.pkl"):
        os.remove('data.pkl')
    else:
        print('No pickle to delete!')