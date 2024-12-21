# getSubsidiaries

Get list of subsidiaries for a selected company. This is useful for recon of wide scope bug bounty targets.

## Requirements

Run `pip install -r requirements.txt` to install required libraries.

Go to https://sec-api.io/signup and get your free API key. Then put your API key in the top of the code, i.e. replace `PUT YOUR API KEY HERE`.

## Running

Examples:
```sh
python getSubsidiairies.py "tesla"
python getSubsidiairies.py "tesla inc"
```

If more than one company is found, then select the company you want to search.

