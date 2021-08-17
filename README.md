# Distance calculation from the Moscow Ring Road to the specified address

The following features are included in the application:

* Usage of endpoint blueprints
* Automated endpoint tests via pytest

## Setup

To set up the application, you need Python 3.8. After cloning the repository change to the project directory and install the dependencies via:

```
python3 -m pip install -r requirements.txt
```

## Development

To start the app in development mode, execute

```
./run_app_dev.sh
```

The application will then be available at `localhost:5000`. You can test the functionality manually using `curl`, e.g. via

```
curl localhost:5000/api/v1/getGeoDistance/test
```

The commands should output

```
{
  "msg": "I'm the test endpoint from getGeoDistance."
}
```

For automated testing run the following command:

```
pytest
```

The commands should output

```
test/test_endpoints.py ....
============= 8 passed in 2.58s ==============
```

Automated test scenarios can be found inside test/test_endpoints.py and it covers the following cases:

```
1) Normal address is passed and gets correct output
2) No address is passed i.e. empty string
3) Wrong address is sent
4) Address passed is inside MKAD region
5) Wrong input structure cases
```

For testing on Custom input run the following python script which reads from stdin and saves the output to test.log file.

```
python3 app.py
```

To view the API documentation through the Swagger user interface, navivate your browser to `localhost:5000/api/docs`. 