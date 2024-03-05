import requests 

headers = {'User-Agent': 'Anita Bui (adb2221@columbia.edu)'}

# Fetch company_ticker info
company_tickers = requests.get("https://www.sec.gov/files/company_tickers_exchange.json", headers=headers)
tickers_dict = company_tickers.json()

companies = tickers_dict['data']
# print(companies) # check companies 

# Filters to Nasdaq companies and gets first 10 
nasdaq_companies = [company for company in companies if company[3] == 'Nasdaq'][:10]
# print(nasdaq_companies) # check nasdaq companies

# Use Edgar endpoint to group companies by state
states = {'No State Present': 0}

for nasdaq_company in nasdaq_companies:
    # Extract CIK and 0-fill
    cik = str(nasdaq_company[0]).zfill(10)

    # Get Information from Edgar Endpoint
    edgar_endpoint = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=headers)

    # Get State Info
    state = edgar_endpoint.json().get('stateOfIncorporation', 'No State Present')

    if not state: 
        state = 'No State Present'

    # Count States 
    if state in states:
        states[state] += 1
    else:
        states[state] = 1

for curr_state, count in states.items():
    print(f"{curr_state}: {count}")