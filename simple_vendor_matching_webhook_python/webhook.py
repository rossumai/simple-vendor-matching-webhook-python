"""An example Python webhook implemented using Flask."""
import hashlib
import hmac
import re
from functools import wraps
from typing import List

from flask import request, jsonify
from werkzeug.exceptions import abort

from simple_vendor_matching_webhook_python.config import SECRET_KEY


def hmac_signature_required(f):
    @wraps(f)
    def authorize_request(*args, **kwargs):
        """Verify the validity of the request coming from Rossum."""
        digest = hmac.new(SECRET_KEY.encode(), request.data, hashlib.sha1).hexdigest()
        try:
            prefix, signature = request.headers["X-Elis-Signature"].split("=")
        except ValueError:
            abort(401, "Incorrect header format")
        if not (prefix == "sha1" and hmac.compare_digest(signature, digest)):
            abort(401, "Authorization failed.")
        return f(*args, **kwargs)

    return authorize_request


def find_by_schema_id(annotation_tree: List, schema_id: str):
    """ Find a node with a given id (as specified in schema) in the annotation tree. """
    for node in annotation_tree:
        if node["schema_id"] == schema_id:
            return node
        if "children" in node:
            node = find_by_schema_id(node["children"], schema_id)
            if node is not None:
                return node
    return None


def normalize_invoice_id(operations: List, annotation_tree: List):
    """ Remove any non-number characters from invoice id. """
    invoice_id = find_by_schema_id(annotation_tree, "invoice_id")
    invoice_id_norm = re.sub(r"[^0-9]", "", invoice_id["content"]["value"])
    if invoice_id_norm != invoice_id["content"]["value"]:
        operations.append(
            {
                "op": "replace",
                "id": invoice_id["id"],
                "value": {
                    "content": {"value": invoice_id_norm, "validation_sources": ["connector"]}
                },
            }
        )


def validate_order_id(messages: List, annotation_tree: List):
    """ Show a warning in case order id is not in a six digit format. """
    order_id = find_by_schema_id(annotation_tree, "order_id")
    if order_id["content"]["value"] != "" and not re.match(
        r"^[0-9]{6}$", order_id["content"]["value"]
    ):
        messages.append(
            {"id": order_id["id"], "type": "warning", "content": "Invalid order_id format."}
        )


def match_vendor(
    messages: List,
    operations: List,
    annotation_tree: List,
    updated_datapoints: List[int],
    action: str,
):
    """Vendor matching based on vendor name.
    How it works: vendor_name contains the name of the vendor to be matched.
    This pre-populates a vendor enum by (even partially) matching vendors
    in the "database", to let the user make a final pick in case of ambiguity.
    It is possible to match also based on vendor's address or VAT ID. In the
    exported data, the matched value holds the vendor id (not the label).
    In case no vendor is matched, "---" is pre-populated in the enum
    and an error is displayed.
    """

    # Just an example.  Load from file, or look up in an SQL database.
    suppliers = [("Roboyo", 1), ("Rossum", 2), ("Volvo", 3)]

    def normalize_name(name):
        name = re.sub(r"[,.\s]", "", name)
        return name.lower()

    vendor = find_by_schema_id(annotation_tree, "vendor")
    vendor_name = find_by_schema_id(annotation_tree, "vendor_name")
    vendor_name_norm = normalize_name(vendor_name["content"]["value"])

    # Do not update the list unless we have a reason.
    if not (action == "initialize" or vendor_name["id"] in updated_datapoints):
        return

    # Here, you would more typically perform an SQL database lookup.
    # We match by any substring. Other common variations:
    # - match only by prefix
    # - reverse prefix match (e.g. match "Rossum Ltd." to supplier "Rossum")
    matched_vendors = [
        (vendor, id_)
        for vendor, id_ in suppliers
        if vendor_name_norm != "" and vendor_name_norm in normalize_name(vendor)
    ]

    if matched_vendors:
        vendor_options = [{"value": id_, "label": vendor} for vendor, id_ in matched_vendors]
    else:
        vendor_options = [{"value": "---", "label": "---"}]
        messages.append({"id": vendor_name["id"], "type": "error", "content": "Vendor not found."})

    operations.append(
        {
            "op": "replace",
            "id": vendor["id"],
            "value": {
                "content": {"value": vendor_options[0]["value"]},
                "options": vendor_options,
                "validation_sources": ["connector"],
            },
        }
    )


@hmac_signature_required
def vendor_matching():
    annotation_tree = request.json["annotation"]["content"]
    updated_datapoints = request.json["updated_datapoints"]
    action = request.json["action"]
    messages = []
    operations = []

    normalize_invoice_id(operations, annotation_tree)
    validate_order_id(messages, annotation_tree)
    match_vendor(messages, operations, annotation_tree, updated_datapoints, action)

    return jsonify({"messages": messages, "operations": operations})
