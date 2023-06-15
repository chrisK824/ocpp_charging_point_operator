## OCPP Central System aka Charging Point Operator

### Supported commands - commands that the CPO will respond to
* Authorize
* BootNotification
* Heartbeat
* MeterValues
* StartTransaction
* StopTransaction


#### Install requirements
`python3.11 -m pip install -r requirements.txt`

#### Usage

##### Start the CPO OCPP server
* Start the CPO OCPP server `python3.11 main.py`
    - port used is `9999`
    - path of server for websocket connections is:  `/ocpp1.6/`
    - View Swagger UI for the available endpoints of the REST API of the CPO at `localhost:9999/docs`

##### Connect a Charging Point client to the CPO OCPP server
* Use a websocket client to connect to the OCPP server e.g chrome extension
    - Select or register a new Charging Point using the Swagger UI
    - Create/view/refresh an ID token for a given Charging Point
    - Extension `chrome-extension://mdmlhchldhfnfnkfmljgeinlffmdgkjo/index.html`
    - Use URL: `ws://127.0.0.1:9999/ocpp1.6/<CHARGING_POINT_ID>`
    - Press connect to connect to the OCPP server
    - Use message section to send messages to the OCPP server
    - Use payloads of `test_cp_requests_payloads.txt` to simulate messages that a charging point would send



