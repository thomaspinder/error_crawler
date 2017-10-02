import os
import pandas as pd
import mammoth 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

root_path = "C:/DROPBOX/Dropbox (Novi.Digital)/SEO 247 - Root Folder/CLIENT MANAGEMENT/ACTIVE Clients"
text_dir = "C:/DROPBOX/Dropbox (Novi.Digital)/SEO 247 - Root Folder/CLIENT MANAGEMENT/ACTIVE Clients/CheapCoffeeSupplIes/Strategic Implementation/Webmaster Tools Reports/2017- 08 Aug/CheapCoffeeSupplies Webmasters Tools Report 08 Aug 17.docx"

clients = os.listdir(root_path)

def dir_finder(client):
    file_dir = root_path+"/"+client+"/Strategic Implementation/"
    for file in os.listdir(file_dir):
        if file.endswith("Error Log.xlsx"):\
        final_dir = file_dir+file
    return final_dir


def docx_to_html(docx_dir):
    with open(docx_dir, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value
        messages = result.messages
        if len(messages) == 0:
            print("No Errors Encountered")
        return html
    
    
def result_gen(df):
    increases = {}
    for column in ref_data.tail(2):
        if column.startswith("Unnamed"):
            pass
        else:
            try:
                x = ((ref_data[column][1]-ref_data[column][0])/ref_data[column][1])
                if x > 0:
                    increases[column] = ((ref_data[column][1]-ref_data[column][0])/ref_data[column][1])
                else:
                    pass
            except:
                print("0 Present, division not possible")
    for key, value in increases.items():
        print("A " + str(round(value*100, 2)) + "% increase in " + str(key) + " errors.")


#Melt the frame and plot
def point_plot(df):
    ref_melt = pd.melt(df, id_vars = "Unnamed: 0", value_vars = list(df.select_dtypes([np.number])))
    ax = sns.pointplot(data = ref_melt, x = "Unnamed: 0", y = "value", hue = "variable", dodge = True)
    ax.set(xlabel = "Date Range", ylabel = "Unit Change")
    plt.show()

for client in clients:
    if client == 'CheapCoffeeSupplIes':
        file_dir = root_path+"/"+client+"/Strategic Implementation/"
        for file in os.listdir(file_dir):
            if file.endswith("Error Log.xlsx"):\
            final_dir = file_dir+file


data = pd.read_excel(final_dir, skiprows=4, sheetname = "Google Webmaster Tools Errors").fillna(0)
ref_data = data.loc[:, (data != 0).any(axis = 0)]
ref_data['Unnamed: 0'] = ref_data['Unnamed: 0'].dt.strftime("%Y-%m-%d")

#Calculate Changes
result_gen(ref_data)

#Plot Changes
point_plot(ref_data)