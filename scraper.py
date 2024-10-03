from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'

# Get HTML text from url
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html.parser")

# print(soup)

# Find tables from webpage
soup.find('table', class_ = "wikitable sortable sticky-header-multi sort-under jquery-tablesorter")

# Store first table from webpage
table = soup.find_all('table')[0]

# Store table headers and format
world_titles = table.find_all('th')
world_table_titles = [title.text.strip() for title in world_titles[:7]]
world_table_titles[6] = world_table_titles[6].removesuffix("[note 1]")


# put headers into dataframe columns
df = pd.DataFrame(columns= world_table_titles)
# print(df)

# Get html column data (rows) from table
column_data = table.find_all('tr')

# Get rank values from table header rows 
rank_data = table.find_all('th')[10:]
rank_values = []
for row in rank_data:
    rank_val = [data.text.strip() for data in row]
    rank_values.append(rank_val)
  

data = []
for row in column_data[2:]:    # 2: - omit first two lists/rows since empty (no td tags in first two rows)
    # get table data for each row in column data
    row_data = row.findAll('td') 

    # format and store data from each row
    individual_row_data = [data.text.strip() for data in row_data[:6]]
    data.append(individual_row_data)

# Add rank values to first column of each row of data
i = 0
while i < len(data):
    data[i].insert(0,rank_values[i][0])
    # print(data[i])
    i += 1

# Add each row of fomatted data in dataframe
for row in data:
    length = len(df)
    df.loc[length] = row

file_path = r'C:\Users\BenRo\OneDrive\Documents\Data Engineering\Projects\WebScraper\Output\CompaniesData.csv'
# Export dataframe to csv file without index
df.to_csv(file_path, index = False)