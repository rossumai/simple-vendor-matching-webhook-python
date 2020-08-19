# Example Python Elis connector

This example connector:
  * Normalizes invoice id to contain only numbers
  * Warns if order id is not in a particular (six digit) format
  * Matches vendor against a vendor list (toy list containing vendors "Roboyo", "Rossum", "Volvo")

![Vendor matching demo](vendordemo.gif)


## Setup
Check out our [Developer Hub connector guide](https://developers.rossum.ai/docs/your-first-connector) to set up
and run the connector for the first time.

After setting up the connector, create `CONNECTOR_SECRET_KEY` environment variable in the environment
where this connector will be running. Its value should be the same as the authentication
token you created following the connector guide.

To use this connector for production, use it via HTTPS and enforce the authentication token.
Customize schema.json to taste before running the connector.
