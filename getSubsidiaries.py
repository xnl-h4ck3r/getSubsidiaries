import requests
import argparse
from sec_api import SubsidiaryApi

API_KEY = 'PUT YOUR API CODE HERE'

# ANSI color codes
BLUE = '\033[94m'
RED = '\033[91m'
PURPLE = '\033[95m'
GREEN = '\033[92m'
RESET = '\033[0m'

def main():
    parser = argparse.ArgumentParser(description='Search for a company ticker on Yahoo Finance')
    parser.add_argument('company_name', type=str, help='Name of the company to search for')
    args = parser.parse_args()

    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": args.company_name, "quotes_count": 0, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    # Filter out results that either have no longname or contain '.'
    valid_results = [(q['longname'], q['symbol']) for q in data['quotes']
                     if q.get('longname') is not None and '.' not in q['symbol']]

    chosen_name, chosen_symbol = None, None

    if len(valid_results) == 1:
        # If there's only one choice, just pick it
        chosen_name, chosen_symbol = valid_results[0]
        print(f"{BLUE}You chose this company:{RESET} {PURPLE}{chosen_name} ({chosen_symbol}){RESET}\n")
    elif len(valid_results) > 1:
        # Multiple choices: prompt user
        print(f"{BLUE}Multiple companies found:{RESET}")
        for i, (name, symbol) in enumerate(valid_results, start=1):
            print(f"{i}. {name} ({symbol})")

        choice = None
        while choice is None:
            try:
                user_input = input(f"{BLUE}Please choose a company: {RESET}")
                idx = int(user_input)
                if 1 <= idx <= len(valid_results):
                    choice = idx
                else:
                    print(f"{RED}Invalid choice. Please try again.{RESET}")
            except ValueError:
                print(f"{RED}Invalid input. Please enter a number.{RESET}")

        chosen_name, chosen_symbol = valid_results[choice - 1]
        print(f"{BLUE}You chose this company:{RESET} {PURPLE}{chosen_name} ({chosen_symbol}){RESET}\n")
    else:
        # No valid results
        print(f"{RED}No matching companies found.{RESET}")
        return

    # If we have chosen a company, run the subsidiary query
    if chosen_symbol:
        subsidiary_api = SubsidiaryApi(API_KEY)
        subs_query = {
            "query": f"ticker:{chosen_symbol}",
            "from": "0",
            "size": "50",
            "sort": [ { "filedAt": { "order": "desc" } } ]
        }
        subsidiaries = subsidiary_api.get_data(subs_query)

        # Check if we have data and subsidiaries
        if 'data' in subsidiaries and len(subsidiaries['data']) > 0:
            data_entry = subsidiaries['data'][0]
            if 'subsidiaries' in data_entry and len(data_entry['subsidiaries']) > 0:
                print(f"{GREEN}The following subsidiaries were found:{RESET}")
                for sub in data_entry['subsidiaries']:
                    print(sub.get('name', 'No subsidiary name found'))
            else:
                print(f"{RED}No subsidiaries found{RESET}")
        else:
            print(f"{RED}No subsidiaries found{RESET}")

if __name__ == '__main__':
    main()
