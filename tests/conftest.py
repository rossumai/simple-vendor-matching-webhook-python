import hashlib
import hmac
import pytest

from typing import List
from simple_vendor_matching_webhook_python import create_app
from tests import WEBHOOK_ID, GENERATED_SECRET_KEY

API_URL = "httpmock://api.elis.rossum.ai"
HOOKS_URL = f"{API_URL}/v1/hooks"
WEBHOOK_URL = f"{HOOKS_URL}/{WEBHOOK_ID}"


@pytest.fixture
def app():
    app = create_app()
    return app


def create_annotation_tree(
    invoice_id="", order_id="", vendor="", amount_due="", vendor_name="---"
) -> List[dict]:
    return [
        {
            "id": "190000",
            "schema_id": "vendor_section",
            "children": [
                {"id": "190001", "schema_id": "invoice_id", "content": {"value": invoice_id}},
                {"id": "190002", "schema_id": "order_id", "content": {"value": order_id}},
                {"id": "190003", "schema_id": "vendor_name", "content": {"value": vendor_name}},
                {"id": "190004", "schema_id": "vendor", "content": {"value": vendor}},
                {"id": "190005", "schema_id": "amount_due", "content": {"value": amount_due}},
            ],
        }
    ]


def create_hashed_signature(request_body: bytes) -> str:
    signature = hmac.new(GENERATED_SECRET_KEY.encode(), request_body, hashlib.sha1).hexdigest()
    return signature
