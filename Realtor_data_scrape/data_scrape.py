import google.generativeai as genai
import pandas as pd
import csv
import gspread
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
genai.configure(api_key="insert api key")

#100 developments a day. attach to sheet team in india can qualify.
# start_data = pd.read_csv('/Users/solomonhufford/Downloads/Untitled spreadsheet - Sheet1.csv')
# city = start_data['City']
# state = start_data['State']
defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.5,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},
                      {"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},
                      {"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}
sizeable_counties = pd.read_csv('/Users/solomonhufford/csv_data')
counties = sizeable_counties['county_full']
states = sizeable_counties['state_name']

# Google Sheets API setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('marketingproject-406421-d8620450026a.json', scope)
gc = gspread.authorize(credentials)

def generate_leads(county_name, state_order):
    input = f"Please make a accurate sheet of information from 2023, I would like for it to include the data of the top community developers in {county_name}, the key members of that development, \
      and the amount of homes this developer sold for each of the years, the population of that county, and the county you were prompted with. If you cannot find the information somewhere please list 'unknown', and do not put any data that is not real or \
        you have made up as this is extremely important data. Please follow the exact same format for each response. Do not make any duplicates in any column, and do not include the rank."
    prompt = f"""input: {input}
    output:"""

    response = genai.generate_text(
      **defaults,
      prompt=prompt
    )

    # Open the Google Sheet by title
    spreadsheet_title = 'lead_creator'
    worksheet_title = f"{state_order}"

    # If the spreadsheet and worksheet don't exist, create them
    # Try to get the existing worksheet
    try:
      sh = gc.open(spreadsheet_title)
      worksheet = sh.worksheet(worksheet_title)
      print(f"Found existing worksheet: {worksheet_title}")
    except WorksheetNotFound:
    # If the worksheet doesn't exist, create a new one
      print(f"Creating a new worksheet: {worksheet_title}")
      sh = gc.open(spreadsheet_title)
      sh.add_worksheet(title=worksheet_title, rows=500, cols=10)
      worksheet = sh.worksheet(worksheet_title)
    except gspread.SpreadsheetNotFound:
    # If the spreadsheet doesn't exist, create it and add a new worksheet
      print(f"Creating a new spreadsheet: {spreadsheet_title}")
      sh = gc.create(spreadsheet_title)
      worksheet = sh.worksheet(worksheet_title)

    print(f"Using worksheet: {worksheet.title}")

      
    # Read the text and convert it into arrays
    text = str(response.result)

    # Use the csv module to read the text into arrays
    data = list(csv.reader(text.strip().splitlines(), delimiter='|'))

    # Remove empty strings and whitespace from the arrays
    data = [[cell.strip() for cell in row if cell.strip()] for row in data]

    #Write the data to the Google Sheet
    #worksheet.clear()
    worksheet.insert_rows(data)
    print(f"Data has been successfully imported into the Google Sheet. {county_name} - {state_order}")
    
i = 0
while i is not len(counties):
   generate_leads(counties[i], states[i])
   i+=1
   
