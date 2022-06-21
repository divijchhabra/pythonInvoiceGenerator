import pandas as pd
from dateutil import parser
import datetime
import numpy as np
from jinja2 import Environment , FileSystemLoader
import pdfkit


print('Hi, This is an HTML to PDF converter\n')

#Taking all the required inputs
inputcsv=input('Please input the Customer CSV file path.').strip("'").strip('"')
htmlSavePath=input('Please input the path of the Folder to save HTML files in.').strip("'").strip('"')
pdfSavePath=input('Please input the path of the Folder to save PDF files in.').strip("'").strip('"')

#Reading the csv with customer data
df=pd.read_csv(inputcsv,sep=';')
#Cleaning the data
df.replace('"', '', inplace=True, regex=True)


class DictToClass(object):
    '''
        Convert Dictionary to class for easier parameter access (using '.' operator)
    '''
    def __init__(self, my_dict):  
        for key in my_dict:
            setattr(self, key, my_dict[key])


print(df.head())
print(str(len(df))+' records found in CSV data\n')


print('\nConverting...\n')


def datetime_format(value, format="%Y-%m-%d %H:%M:%S"):
    '''
    Format date and time using the date string from csv
    '''
    datetime_obj = parser.parse(value.strip('"'))
    return datetime_obj.strftime("%Y-%m-%d")


#Convert html to pdf using pdfkit 
def html2pdf(html, pdf):
    
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html) as f:
        pdfkit.from_file(f, pdf, options=options)



#Renders HTML file filled with data and saves it as customer_first_name.html
def renderHtml(path,data):
    fileLoader=FileSystemLoader('templates')
    env=Environment(loader=fileLoader)

    env.filters["datetime_format"] = datetime_format
    rendered=env.get_template('template.html').render(invoice_id=data.invoice_id,data=data,invoice_type=data.invoice_type,service_data=data)
    with open(f"{htmlSavePath}/{data.first_name}.html","w") as f:
        f.write(rendered)

try:
    for i in range(len(df)):
        d1=df.iloc[i].to_dict()
        data=DictToClass(d1)          

        ind=data.invoice_id
        print(ind)
        html_path = f'{htmlSavePath}/{data.first_name}.html'
        renderHtml(html_path,data)
        if(str(data.invoice_type).lower()=='invoice'):
            pdf_path = f'{pdfSavePath}/Inv.{ind}_{data.product_name}_{datetime_format(data.created_at)}.pdf'
        else:
            pdf_path = f'{pdfSavePath}/CrInv.{ind}_{data.product_name}_{datetime_format(data.refunded_at)}.pdf'
        html2pdf(html_path,pdf_path)
    print('\nALL DONE! The pdf files have now been saved.')

except Exception as e:
    print('\nOh no! An error occured!\n')
    print(e)
