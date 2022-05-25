import os
import pandas as pd
import PyPDF2

# assign PDF directory
DIR = '../data/pdfs/'

# list intake categories
INTAKES = [
    'Stray', 'Owner Surrender', 'Confiscate', 'Wildlife', 
    'Disposal Request', 'Euthanasia Request', 'Returns',
    'Quarantine'
]

MONTHS = {
    'jan':'January','feb':'February','mar':'March','apr':'April',
    'aug':'August','sept':'September','oct':'October','nov':'November',
    'dec':'December','jul':'July','jun':'June','sep':'September'
}

def pdf_to_df(filename, month, year, intake=INTAKES):
    file = open(filename, 'rb')
    reader = PyPDF2.PdfFileReader(file)
    
    # extract page text
    pageObj = reader.getPage(0)
    page = pageObj.extractText()
    
    # strip away page header
    page = page[45:]

    # insert breaks to separate variables and then remove excess strings
    page_cln = page.replace(
        '\n','|'
    ).replace(
        'Outcomes|',''
    ).replace(
        'Intakes','Outcomes'
    )
    
    # add intake for consistency
    page_cln = 'Intakes|' + page_cln
    
    # convert string to list
    page_splt = page_cln.split('|')
    
    # split string into list of lists
    frame = []
    i=0

    for n in range(1,(len(page_splt)//5)+1):
        frame.append(page_splt[i:n*5])
        i+=5
    
    # convert to dataframe    
    df = pd.DataFrame(frame, columns=['Category','Dog','Cat','Other','Total'])
    df = df[~df.Category.isin(['Intakes','Outcomes','Total'])]
    df = df.drop(columns=['Total'])

    df['Type'] = ['Intakes' if c in intake else 'Outcomes' for c in df.Category]

    df['Month'] = month
    df['Year'] = year
    df['Date'] = df['Month']+ '-' + df['Year']
    df['Date'] = pd.to_datetime(df['Date'], format=("%B-%Y"))
    df['Date'] = df['Date'].dt.to_period('M')
    
    return df

full_df = pd.DataFrame()
 
# iterate over PDF files
for filename in os.listdir(DIR):
    if filename[-3:] == 'pdf':
        txt = filename[:-4].replace('_stats','').replace('-stats','').split('_')
        month=txt[0]
        year=txt[1]
        
        if month.lower() in MONTHS.keys():
            month = MONTHS[month]
        file = os.path.join(DIR, filename)

        month_df = pdf_to_df(file, month, year)
        full_df = pd.concat([full_df,month_df])

# clean up data types
full_df['Dog'] = full_df['Dog'].astype(int)
full_df['Cat'] = full_df['Cat'].astype(int)
full_df['Other'] = full_df['Other'].str.replace(',','').astype(int)
full_df['Year'] = full_df['Year'].astype(int)
full_df['Month'] = full_df['Month'].str.capitalize()

# save dataframe
full_df.to_csv('../data/cacc_monthly_data.csv')