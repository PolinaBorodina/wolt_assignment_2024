# Test Assignment for Wolt Summer 2024 Engineering Internships, Backend, Python

## Made by Polina Borodina

### Short description
This project was made as a test assignment for Wolt Summer 2024 Engineering Internships

Assignment specification (Python, backend) can be found [here.](https://github.com/woltapp/engineering-internship-2024)

### Prerequisites
The project was made using **Python version 3.12.1**. Compatibility with earlier versions is not guaranteed.

### How to run the project:
**Step 1. Create venv**

Check how to create and activate venv in your environment [here.](https://docs.python.org/3/library/venv.html)

Example:
```
python -m venv new_environment
```

_For Linux/Mac change python to python3_

**Step 2. Activate venv**

Check how to activate venv in your environment [here.](https://docs.python.org/3/tutorial/venv.html)

For example, if you want to activate virtual environment on Windows in a PowerShell console, use the next command:
```
C:\path_to_new_environment\new_environment\Scripts\activate.ps1
```

*In venv directory you can also find 'deactivate.bat' script, use it if you want to deactivate active virtual environment*

**Step 3. Install requirements**

*Make sure that the virtual environment from the previous steps is active*

*Don't forget to switch to the project directory or specify full path to app.py*

Example:
```
pip install -r requirements.txt
```

**Step 4. Run app.py**

*Don't forget to switch to the project directory or specify full path to app.py*

Windows:
```
python app.py
```
An example with a path:
```
python C:\path_to_project\app.py
```
For Linux/Mac change python to _python3_

*Note! Flask server will be run and its address will be displayed in the output.
Default address is http://127.0.0.1:5000*

### How to send a request:
1. Make sure that the project is running
2. Make a POST request to http://127.0.0.1:5000/calc_fee
*(check server address from the last step of "How to run the project" paragraph)*

To make a request you can use, for example, Postman. 
Create a new POST request, change Content-Type to application/json and add your JSON into body of the request.
When you will send request, response will appear.

Request body (json) example:
```json
{"cart_value": 7920, "delivery_distance": 1335, "number_of_items": 4, "time": "2024-01-26T16:00:00Z"}
```

The same request can be made with curl.
Check how to use curl  [here.](https://curl.se/docs/tutorial.html)

Example for **Windows**, cmd (character " must be escaped if you use cmd):
```
curl -i -X POST -H "Content-Type:application/json" -d "{\"cart_value\": 7920,  \"delivery_distance\" : 1335,  \"number_of_items\" : 4, \"time\" : \"2024-01-26T16:00:00Z\" }" http://127.0.0.1:5000/calc_fee
```

Example for Linux/Mac:
```
curl -i -X POST -H 'Content-Type:application/json' -d '{"cart_value":7920,"delivery_distance":1335,"number_of_items":4,"time":"2024-01-26T16:00:00Z"}' http://127.0.0.1:5000/calc_fee
```

Response example:
```
HTTP/1.1 200 OK
Server: Werkzeug/3.0.1 Python/3.12.1
Date: Tue, 30 Jan 2024 13:15:14 GMT
Content-Type: application/json
Content-Length: 21
Connection: close

{"delivery_fee":360}
```
If you use curl with only -H and -d parameters, you get short answer:
```
curl -H 'Content-Type:application/json' -d '{"cart_value":7920,"delivery_distance":1335,"number_of_items":4,"time":"2024-01-26T16:00:00Z"}' http://127.0.0.1:5000/calc_fee
```
Responce:
```
{"delivery_fee":360}
```
____
Request parameters description:

| Field             | Type    | Description                                                                | Example value                            |
|:------------------|:--------|:---------------------------------------------------------------------------|:-----------------------------------------|
| cart_value        | Integer | Value of the shopping cart __in cents__.                                   | __790__ (790 cents = 7.90€)              |
| delivery_distance | Integer | The distance between the store and customer’s location __in meters__.      | __2235__ (2235 meters = 2.235 km)        |
| number_of_items   | Integer | The __number of items__ in the customer's shopping cart.                   | __4__ (customer has 4 items in the cart) |
| time              | String  | Order time in UTC in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). | __2024-01-15T13:00:00Z__                 |

Response example:
```json
{"delivery_fee":360}
```
Response parameter description:

| Field        | Type    | Description                           | Example value               |
|:-------------|:--------|:--------------------------------------|:----------------------------|
| delivery_fee | Integer | Calculated delivery fee __in cents__. | __710__ (710 cents = 7.10€) |
____
### About tests
* End time of Friday rush (7 PM UTC) is **included** into the rush interval.
* Tests can be found in the project directory
  * test_app.py contains a test for functionality from app.py
  * test_calculations.py contains a test for functionality from calculations.py
* No negative tests were added. The behavior in negative scenarios is not defined, so there is no point in testing such behavior.
* Some supposed max values for testing purposes were added: MAX_CART_VALUE, MAX_DISTANCE, MAX_ITEMS_NUM.
  * They were necessary because I needed some upper limits of values.
  * MAX_DISTANCE and MAX_ITEMS_NUM were counted as a theoretically max numbers that can change calculations result before the delivery fee limit will be reached 

**To run tests:**
* make sure that virtual environment is activated
* make sure that you are in the project directory
* choose what file you want to execute test_app.py or test_calculations.py
* use following commands:

For Windows:
```
python -m pytest tests\test_calculations.py
```
```
python -m pytest tests\test_app.py
```

For Linux/Mac use forward slash:
```
python -m pytest tests/test_calculations.py
```
```
python -m pytest tests/test_app.py
```