import json
from tests.conftest import create_annotation_tree, WEBHOOK_URL
from tests.conftest import create_hashed_signature


class TestValidate:
    def test_success(self, client):
        annotation_tree = create_annotation_tree(vendor_name="Roboyo")
        webhook_schema = {
            "action": "initialize",
            "updated_datapoints": [],
            "hook": WEBHOOK_URL,
            "annotation": {"content": annotation_tree},
        }
        request_body = json.dumps(webhook_schema).encode("utf-8")

        annot_tree = client.post(
            data=request_body,
            path="/vendor_matching",
            headers={
                "Content-Type": "application/json",
                "X-Elis-Signature": f"sha1={create_hashed_signature(request_body)}",
            },
        )

        assert annot_tree.status_code == 200
        assert annot_tree.json == {
            "messages": [],
            "operations": [
                {
                    "id": "190004",
                    "op": "replace",
                    "value": {
                        "content": {"value": 1},
                        "options": [{"label": "Roboyo", "value": 1}],
                        "validation_sources": ["connector"],
                    },
                }
            ],
        }

    def test_vendor_not_found(self, client):
        webhook_schema = {
            "action": "initialize",
            "updated_datapoints": [],
            "hook": WEBHOOK_URL,
            "annotation": {"content": create_annotation_tree(vendor_name="Sony")},
        }
        request_body = json.dumps(webhook_schema).encode("utf-8")

        annot_tree = client.post(
            data=request_body,
            path="/vendor_matching",
            headers={
                "Content-Type": "application/json",
                "X-Elis-Signature": f"sha1={create_hashed_signature(request_body)}",
            },
        )

        assert annot_tree.status_code == 200
        assert annot_tree.json == {
            "messages": [{"content": "Vendor not found.", "id": "190003", "type": "error"}],
            "operations": [
                {
                    "id": "190004",
                    "op": "replace",
                    "value": {
                        "content": {"value": "---"},
                        "options": [{"label": "---", "value": "---"}],
                        "validation_sources": ["connector"],
                    },
                }
            ],
        }
