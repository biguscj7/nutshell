import os

import pytest

from dotenv import load_dotenv

from nutshell import NutshellAPI
from nutshell.entities import CreateActivity, Activity
from nutshell.methods import NewActivity, GetActivity, DeleteActivity, EditActivity

load_dotenv()


@pytest.mark.live_api
@pytest.fixture()
def api() -> NutshellAPI:
    return NutshellAPI(os.getenv("NUTSHELL_USERNAME"), password=os.getenv("NUTSHELL_KEY"))


@pytest.mark.live_api
@pytest.fixture
def create_new_activity(api) -> Activity:
    created_activity = CreateActivity(name="New testing activity",
                                      description="Creating test activity for integration testing", activity_type_id=1,
                                      start_time="2024-03-30T18:00:00+00:00", end_time="2024-03-30T18:00:00+00:00")

    new_activity = NewActivity(activity=created_activity)
    api.api_calls = new_activity
    api_response = api.call_api()
    yield api_response.result

    api.api_calls = GetActivity(activity_id=api_response.result.id)
    single_activity = api.call_api().result

    api.api_calls = DeleteActivity(activity_id=single_activity.id, rev=single_activity.rev)
    delete_result = api.call_api().result

    assert delete_result  # result should be boolean of True


@pytest.mark.live_api
def test_new_activity(api, create_new_activity):
    assert isinstance(create_new_activity, Activity)
    assert create_new_activity.name == "New testing activity"
    assert create_new_activity.description == "Creating test activity for integration testing"


def test_get_activity(api, create_new_activity):
    activity_id = create_new_activity.id
    get_activity = GetActivity(activity_id=activity_id)
    api.api_calls = get_activity
    call_result = api.call_api().result
    assert call_result.id == activity_id
    assert call_result.name == "New testing activity"
    assert call_result.description == "Creating test activity for integration testing"


def test_edit_activity(api, create_new_activity):
    activity_id = create_new_activity.id

    edit_activity = EditActivity(activity_id=activity_id, rev=create_new_activity.rev,
                                 activity={"name": "Edited testing activity"})
    api.api_calls = edit_activity
    edited_activity = api.call_api().result
    assert edited_activity.name == "Edited testing activity"
    assert edited_activity.description == "Creating test activity for integration testing"
    assert edited_activity.id == activity_id
    assert edited_activity.rev != create_new_activity.rev
