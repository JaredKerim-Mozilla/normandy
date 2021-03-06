import json
import jsonschema
import pytest

from datetime import datetime

from normandy.recipes import signing


def canonical_json(data):
    return json.dumps(data, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode()


def check_action_schema_format(action):
    """Given an action, make sure its argument schema is a valid json schema"""
    # This avoids downloading the schema by asserting that it is using json schema draft v4, and
    # checking against a local copy of it.
    assert action["arguments_schema"]["$schema"] == "http://json-schema.org/draft-04/schema#"
    with open("contract-tests/data/json-schema-draft-4-schema.json") as f:
        schema = json.load(f)
        assert jsonschema.validate(action["arguments_schema"], schema) is None


@pytest.mark.skip(
    # NOTE(peterbe): Let's fix or delete this test once the dust has settled
    # for how to reason about known-in-advance actions.
    reason=(
        "The list of possible actions is no longer hard coded and known. "
        "With remote actions we might have them being added as more recipes "
        "are actually added to mozilla-central. "
    )
)
def test_expected_action_types(conf, requests_session):
    r = requests_session.get(conf.getoption("server") + "/api/v1/action/")
    r.raise_for_status()
    response = r.json()

    # Verify we have at least one response and then grab the first record
    assert len(response) >= 1

    # Make sure we only have expected action types
    expected_records = ["console-log", "show-heartbeat", "preference-experiment", "opt-out-study"]

    for record in response:
        assert record["name"] in expected_records


def test_console_log(conf, requests_session):
    r = requests_session.get(conf.getoption("server") + "/api/v1/action/")
    r.raise_for_status()
    response = r.json()

    # Verify we have at least one response and then grab the first record
    assert len(response) >= 1

    # Look for any console-log actions
    cl_records = [record for record in response if record["name"] == "console-log"]

    if len(cl_records) == 0:
        pytest.skip("No console-log actions found")
        return

    record = cl_records[0]
    # Does an 'action' have all the required fields?
    expected_action_fields = ["name", "implementation_url", "arguments_schema"]
    for field in record:
        assert field in expected_action_fields

    check_action_schema_format(record)


def test_show_heartbeat(conf, requests_session):
    r = requests_session.get(conf.getoption("server") + "/api/v1/action/")
    r.raise_for_status()
    response = r.json()

    # Verify we have at least one response and then grab the first record
    assert len(response) >= 1

    # Let's find at least one record that is a 'show-heartbeat'
    sh_records = [record for record in response if record["name"] == "show-heartbeat"]

    if len(sh_records) == 0:
        pytest.skip("No show-heartbeat actions found")
        return

    record = sh_records[0]
    expected_action_fields = ["name", "implementation_url", "arguments_schema"]
    for field in record:
        assert field in expected_action_fields

    check_action_schema_format(record)


def test_recipe_signatures(conf, requests_session):
    r = requests_session.get(conf.getoption("server") + "/api/v1/recipe/signed/")
    r.raise_for_status()
    data = r.json()

    if len(data) == 0:
        pytest.skip("No signed recipes")

    for item in data:
        canonical_recipe = canonical_json(item["recipe"])
        signature = item["signature"]["signature"]
        x5u = item["signature"]["x5u"]
        assert signing.verify_signature_x5u(canonical_recipe, signature, x5u)


def test_action_signatures(conf, requests_session):
    r = requests_session.get(conf.getoption("server") + "/api/v1/action/signed/")
    r.raise_for_status()
    data = r.json()

    if len(data) == 0:
        pytest.skip("No signed actions")

    for item in data:
        canonical_action = canonical_json(item["action"])
        signature = item["signature"]["signature"]
        x5u = item["signature"]["x5u"]
        assert signing.verify_signature_x5u(canonical_action, signature, x5u)


def test_recipe_api_is_json(conf, requests_session):
    r = requests_session.get(conf.getoption("server") + "/api/v1/recipe/?enabled=1")
    r.raise_for_status()
    data = r.json()
    assert isinstance(data, list)


def test_recipe_history(conf, requests_session):
    r = requests_session.get(conf.getoption("server") + "/api/v1/recipe/")
    r.raise_for_status()
    data = r.json()

    if len(data) == 0:
        pytest.skip("No recipes found.")

    for item in data:
        endpoint = f'/api/v1/recipe/{item["id"]}/history/'
        r = requests_session.get(conf.getoption("server") + endpoint)
        r.raise_for_status()
        history = r.json()

        last_date = datetime.now()
        for revision in history:
            created = datetime.strptime(revision["date_created"], "%Y-%m-%dT%H:%M:%S.%fZ")
            assert created < last_date
            last_date = created
