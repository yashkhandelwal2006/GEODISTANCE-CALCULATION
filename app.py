import requests

#String Input
address = input('Enter address: ')
url = 'http://localhost:5000/api/v1/getGeoDistance/distance'
payload = {'address': address}
#Service invoked to get distance
response = requests.post(url, json=payload)
#checking status code of response and further processing based on it
if response.status_code == 200:
    output = '\n'
    json = response.json()
    if 'msg' in json:
        output += json['msg']
    elif 'output' in json:
        output += json['output']
    #writing output to .log file
    with open("test.log", "a") as myfile:
        myfile.write(output)