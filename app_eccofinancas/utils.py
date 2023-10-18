import requests

def getBanks():
    urlApi = "https://brasilapi.com.br/api/banks/v1/"
    response = requests.get(urlApi)

    if response.ok:
        banks = response.json()
        return banks
    else:
        raise Exception(requests.status_codes)
    
def getBankByCode(code):
    urlApi = f"https://brasilapi.com.br/api/banks/v1/{code}"
    response = requests.get(urlApi)

    if response.ok:
        bank = response.json()
        return bank
    else:
        raise Exception(requests.status_codes)

def getCodeBankByFullName(fullName):
    banks = getBanks()
    for bank in banks:
        if 'fullName' in bank and bank['fullName'] == fullName:
            return bank['code']