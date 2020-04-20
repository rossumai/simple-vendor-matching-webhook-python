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

You can use [elisctl](https://github.com/rossumai/elisctl) tool to configure an Elis queue to use the connector.

Create the connector first:

```
	 elisctl connector create "Python Example Connector" --service-url http://hostname:5000 --auth-token wuNg0OenyaeK4eenOovi7aiF
```
The `--auth-token` will create the secret token that Rossum checks before sending the data to the connector to avoid data leakage.
The value should be stored in the `CONNECTOR_SECRET_KEY` environment variable in the environment where this connector will be running.

In the response, you will receive the ID of the connector. Next, choose an existing queue and deploy the connector to it:

```
	 elisctl queue change 29582 --connector-id 1506
```

Or create a new queue and attach the connector to it:

```
	 elisctl queue create "Python Connector Queue" --connector-id 1506 -s schema.json
```

You can also [configure the connector using our API](https://api.elis.rossum.ai/docs/#create-a-new-connector) directly.

To use this for production, use via HTTPS and enforce the authentication token.
Customize schema.json to taste.

For more information on how to run a connector, check out our [Developer Hub connector guide](https://developers.rossum.ai/docs/your-first-connector).