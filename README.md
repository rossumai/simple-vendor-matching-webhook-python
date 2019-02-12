# Example Python Elis connector

This example connector:
  * Normalizes invoice id to contain only numbers
  * Warns if order id is not in a particular (six digit) format
  * Matches vendor against a vendor list (toy list containing vendors "Roboyo", "Rossum", "Volvo")

![Vendor matching demo](vendordemo.gif)

To run it:
```
	python3 connector.py
```

To configure an elis queue to use it:
```
	curl -u demo-default@elis.rossum.ai:... -H 'Content-Type: application/json'   -d '{"name": "Python Example Connector", "service_url": "http://hostname:5000", "authorization_token":"wuNg0OenyaeK4eenOovi7aiF"}'   'https://api.elis.rossum.ai/v1/connectors
		{"id":1506, ...}
	elisctl queue create 'Python example' --connector-id 1506 -s schema.json
```

To use this for production, use via HTTPS and enforce the authentication token.
Customize schema.json to taste.
