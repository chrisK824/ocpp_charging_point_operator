#### Install requirements
`python3.9 -m pip install -r requirements.txt`

#### Usage
* Start the OCPP server `python3.9 main.py`
    - port used is `9999`
    - path of server is `/ocpp1.6/`

* Use a websocket client to connect to the OCPP server e.g chrome extension 
    - Extension `chrome-extension://mdmlhchldhfnfnkfmljgeinlffmdgkjo/index.html`
    - Use URL (`virta_sub001` is already existing charging point in the db): `ws://127.0.0.1:9999/ocpp1.6/virta_sub001`
    - Press connect to connect to the ocpp server
    - Use message section to send messages to the OCPP server
    - Use payloads of `test_cp_requests_payloads.txt` to simulate messages that a charging point would send


