import requests

headersPanelSms = {
    'X-API-KEY': 'test'
}


def send(phone, code):
    if phone.startswith('0'):
        phone = phone[1:]
    json = {
        "mobile": "{}".format(phone),
        "templateId": 653542,
        "parameters": [
            {
                "name": "CODE",
                "value": "{}".format(code)
            }
        ]
    }
    url = 'https://api.sms.ir/v1/send/verify'
    response = requests.post(url=url, json=json, headers=headersPanelSms)
    print('status_code == ', response.status_code)
    return response.status_code
