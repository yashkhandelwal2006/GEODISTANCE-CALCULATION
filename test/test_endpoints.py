import os
import requests
from openapi_spec_validator import validate_spec_url

def test_getGeoDistance_test(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'getGeoDistance', 'test')
    response = requests.get(endpoint)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "I'm the test endpoint from getGeoDistance."

#Basic Case
def test_normal_case(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'getGeoDistance', 'distance')
    payload = {'address': '202 alwar rajasthan'}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'output' in json
    assert round(float(json['output'].split()[0]), 2) == 4407.39

#Empty string passed
def test_no_address_case(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'getGeoDistance', 'distance')
    payload = {'address': ' '}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "No address passed"

#Invalid address case
def test_invalid_address_case(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'getGeoDistance', 'distance')
    payload = {'address': '47fb74fb74h74h74gd7g4d74g7d'}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Address not found"

#Inside MKAD case
def test_inside_MKAD_address_case(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'getGeoDistance', 'distance')
    payload = {'address': 'MKAD'}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Address Inside MKAD"

#Invalid input Case
def test_invalid_input_case(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'getGeoDistance', 'distance')
    payload = {'addres': 'moscow'}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Invalid data found"

#Wrong input datatype
def test_wrong_datatype_case(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'getGeoDistance', 'distance')
    payload = {'address': 6353837}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Invalid data found"

def test_swagger_specification(host):
    endpoint = os.path.join(host, 'api', 'swagger.json')
    validate_spec_url(endpoint)
    # use https://editor.swagger.io/ to fix issues
