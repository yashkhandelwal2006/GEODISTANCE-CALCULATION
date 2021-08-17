from flask import Blueprint, jsonify, request
import requests
#haversine is used for calculating distance between given geo locations/coordinates.
from haversine import haversine
getGeoDistance = Blueprint(name="blueprint_geo", import_name=__name__)

def get_coordinates(in_val, is_ring_road = False, bbox = False):
  '''
    Description : Takes in address as the input and returns it's latitudes and longitudes or it's bounding box of the area based on the flags
    inputs :
      in_val(String) : Address String
      is_ring_road(Boolean) : Only for Moscow ring road which only needs (long, lat)
      bbox(Boolean) : Only for MKAD to get it's bounding region coordinates
    outputs :
      Scenario 1:
        Tuple (True/False, Longitude, Latitude)
      Scenario 2:
        Tuple (Longitude, Latitude)
      Scenario 3:
        List Bounding box of the region
  '''
  response = requests.get(API_URL + '+'.join(in_val.split()))
  data = response.json()
  found = int(data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'])
  if found > 0:
    if bbox:
      llongi, llat = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']['lowerCorner'].split()
      ulongi, ulat = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']['upperCorner'].split()
      return [float(llongi), float(llat), float(ulongi), float(ulat)]
    longi, lat = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
    lat = float(lat)
    longi = float(longi) 
    if is_ring_road:
      return longi, lat
    return True, longi, lat
  return (False,)

API_KEY = '1d421467-249f-4246-8ad2-889297a728f8'
API_URL = f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&format=json&lang=en_RU&geocode='
ring_road_coordinates = get_coordinates('Moscow ring road', is_ring_road = True)
mkad_bbox = get_coordinates('MKAD', bbox = True)

@getGeoDistance.route('/test', methods=['GET'])
def test():
    """
    ---
    get:
      description: test endpoint
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - testing
    """
    output = {"msg": "I'm the test endpoint from getGeoDistance."}
    return jsonify(output)


@getGeoDistance.route('/distance', methods=['POST'])
def plus_x():
    """
    ---
    post:
      description: calculates the distance from Moscow Ring Road
      requestBody:
        required: true
        content:
            application/json:
                schema: InputSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - calculation
    """
    # retrieve body data from input JSON
    data = request.get_json()
    if 'address' not in data:
      return {"msg": "Invalid data found"}
    in_val = data['address']
    if not isinstance(in_val,str):
      return {"msg": "Invalid data found"}
    if not in_val.strip():
      return {"msg": "No address passed"}
    # compute result and return as JSON
    coordinates = get_coordinates(in_val)
    distance = ''
    if coordinates[0]:
      if coordinates[1] >= mkad_bbox[0] and coordinates[1] <= mkad_bbox[2] and coordinates[2] >= mkad_bbox[1] and coordinates[2] <= mkad_bbox[3]:
        return {"msg": "Address Inside MKAD"}
      longi, lat = coordinates[1:]
      distance = haversine(ring_road_coordinates[::-1], (lat, longi))
    else:
      return {"msg": "Address not found"} 
    output = {"output": str(distance) + " kms"}
    return jsonify(output)