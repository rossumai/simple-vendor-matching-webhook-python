# Example Python Rossum connector

This example connector:
  * Normalizes invoice id to contain only numbers
  * Warns if order id is not in a particular (six digit) format
  * Matches vendor against a vendor list (toy list containing vendors "Roboyo", "Rossum", "Volvo")

![Vendor matching demo](vendordemo.gif)

## Instructions

Check out the [basic Rossum connector guide](https://developers.rossum.ai/docs/your-first-connector).

This example connector is designed to work with a particular schema - use `schema.json` that is part of this project.
Of course, customize schema.json to taste.

To use this connector for production, use via HTTPS and enforce the authentication token verification.
