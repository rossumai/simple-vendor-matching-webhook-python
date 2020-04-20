"""An example Python connector implemented using Flask."""
import hmac
import os
import re
from functools import wraps

import flask
from flask import request, jsonify
from werkzeug.exceptions import Unauthorized

app = flask.Flask(__name__)
# app.config["DEBUG"] = True


def auth_required(f):
    @wraps(f)
    def authorize_request(*args, **kwargs):
        expected_header = f"secret_key {os.environ['CONNECTOR_SECRET_KEY']}"
        authorized = hmac.compare_digest(request.headers.get("Authorization", ""), expected_header)
        if not authorized:
            raise Unauthorized("Invalid authorization header.")
        return f(*args, **kwargs)

    return authorize_request


def find_by_schema_id(annotation_tree, schema_id):
    """ Find a node with a given id (as specified in schema) in the annotation tree. """
    for node in annotation_tree:
        if node['schema_id'] == schema_id:
            return node
        if 'children' in node:
            node = find_by_schema_id(node['children'], schema_id)
            if node is not None:
                return node
    return None


def normalize_invoice_id(messages, updated_datapoints, annotation_tree):
    """ Remove any non-number characters from invoice id. """
    invoice_id = find_by_schema_id(annotation_tree, 'invoice_id')
    invoice_id_norm = re.sub(r'[^0-9]', '', invoice_id['value'])
    if invoice_id_norm != invoice_id['value']:
        updated_datapoints.append({'id': invoice_id['id'], 'value': invoice_id_norm})


def validate_order_id(messages, updated_datapoints, annotation_tree):
    """ Show a warning in case order id is not in a six digit format. """
    order_id = find_by_schema_id(annotation_tree, 'order_id')
    if order_id['value'] != '' and not re.match(r'^[0-9]{6}$', order_id['value']):
        messages.append({'id': order_id['id'], 'type': 'warning', 'content': 'Invalid order_id format.'})


def match_supplier(messages, updated_datapoints, annotation_tree, is_initial, previously_updated):
    """
    Supplier matching based on vendor name.

    How it works: vendor_name contains the name of the supplier to be matched.
    This pre-populates a vendor enum by (even partially) matching suppliers
    in our "database", to let the user make a final pick in case of ambiguity.
    This enum maps the name to a vendor id that is part of the exported data.

    In case no vendor is matched by this name, "---" is pre-populated in the
    enum and an error is displayed.
    """
    # Just an example.  Load from file, or look up in an SQL database.
    SUPPLIERS = [
        ('Roboyo', 1),
        ('Rossum', 2),
        ('Volvo', 3),
    ]
    def normalize_name(name):
        name = re.sub(r'[,.\s]', '', name)
        return name.lower()

    vendor = find_by_schema_id(annotation_tree, 'vendor')
    vendor_name = find_by_schema_id(annotation_tree, 'vendor_name')
    vendor_name_norm = normalize_name(vendor_name['value'])

    # Do not update the list unless we have a reason.
    if not (is_initial or vendor_name['id'] in previously_updated):
        return

    # Here, you would more typically perform an SQL database lookup.
    # We match by any substring. Other common variations:
    # - match only by prefix
    # - reverse prefix match (e.g. match "Rossum Ltd." to supplier "Rossum")
    matched_vendors = [(vendor, id)
                       for vendor, id in SUPPLIERS
                       if vendor_name_norm != '' and vendor_name_norm in normalize_name(vendor)]

    if matched_vendors:
        vendor_options = [{'value': id, 'label': vendor} for vendor, id in matched_vendors]
    else:
        vendor_options = [{'value': '---', 'label': '---'}]
        messages.append({'id': vendor_name['id'], 'type': 'error', 'content': 'Vendor not found.'})

    updated_datapoints.append(
        { 'id': vendor['id'], 'value': vendor_options[0]['value'], 'options': vendor_options}
    )


@app.route('/validate', methods=['POST'])
@auth_required
def api_validate():
    annotation_tree = request.json['content']
    previously_updated = request.json['meta']['updated_datapoint_ids']
    is_initial = request.args.get('initial', 'false').lower() == 'true'
    messages = []
    updated_datapoints = []

    normalize_invoice_id(messages, updated_datapoints, annotation_tree)
    validate_order_id(messages, updated_datapoints, annotation_tree)
    match_supplier(messages, updated_datapoints, annotation_tree, is_initial, previously_updated)

    return jsonify({'messages': messages, 'updated_datapoints': updated_datapoints})


@app.route('/save', methods=['POST'])
def api_save():
    # We do nothing explicit on invoice export.
    return jsonify({})


@app.route('/healthz', methods=['GET'])
def api_healthz():
    # This is not required by Elis, but useful when running the connector
    # in a managed environment (e.g. Kubernetes).
    return ('', 204)


app.run(host='0.0.0.0')
