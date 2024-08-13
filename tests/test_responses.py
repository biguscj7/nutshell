import pytest
from pydantic import ValidationError

from rich import print

from nutshell.responses import FindUsersResult, FindTeamsResult, FindActivityTypesResult, GetAnalyticsReportResult, \
    FindStagesetsResult, FindMilestonesResult, FindLeadsResult, FindActivitiesResult

from nutshell.entities import User, Team, Lead, TimeSeriesData, SummaryData, ActivityType, Stageset, Milestone, Activity


@pytest.fixture()
def testing_user():
    return User(stub=True, id=1, entityType="Users", rev="1", name="John Doe", isEnabled=True, isAdministrator=True,
                emails=["test@mail.com"], modifiedTime="2021-01-01T00:00:00Z", createdTime="2021-01-01T00:00:00Z")


@pytest.fixture()
def testing_team():
    return Team(stub=True, id=1, name="Team One", rev="1", entityType="Teams", modifiedTime="2021-01-01T00:00:00Z",
                createdTime="2021-01-01T00:00:00Z")


@pytest.fixture()
def testing_milestone():
    return Milestone(id=1, name="Milestone One", rev="1", entityType="Milestones", position=1,
                     stagesetId=1)


@pytest.fixture()
def test_stageset():
    return Stageset(id=1, entityType="Stagesets", name="Stageset One", default=1, position=1)


def test_user():
    user_dict = {
        "stub": True,
        "id": 1,
        "entityType": "Users",
        "rev": "1",
        "name": "John Doe",
        "isEnabled": True,
        "isAdministrator": True,
        "emails": ["test@test.com"],
        "modifiedTime": "2024-01-17T19:12:05+0000",
        "createdTime": "2021-11-15T16:42:22+0000",
    }
    user = User(**user_dict)
    assert user.stub is True
    assert user.id == 1
    assert user.entity_type == "Users"
    assert user.rev == "1"
    assert user.name == "John Doe"
    assert user.first_name is None
    assert user.last_name is None
    assert user.is_enabled is True
    assert user.is_administrator is True
    assert user.emails == ["test@test.com"]
    assert user.modified_time == "2024-01-17T19:12:05+0000"
    assert user.created_time == "2021-11-15T16:42:22+0000"


def test_non_user():
    user_dict = {
        "stub": True,
        "id": 1,
        "entityType": "Teams",
        "rev": "1",
        "name": "John Doe",
        "isEnabled": True,
        "modifiedTime": "2024-01-17T19:12:05+0000",
        "createdTime": "2021-11-15T16:42:22+0000",
    }
    with pytest.raises(ValidationError):
        User(**user_dict)


def test_userresponse():
    with open("findUsers.json") as f:
        user_response = FindUsersResult.model_validate_json(f.read())
    for user in user_response.result:
        assert isinstance(user, User)


def test_team():
    team_dict = {
        "stub": True,
        "id": 1,
        "name": "Team A",
        "rev": "1",
        "entityType": "Teams",
        "isEnabled": True,
        "modifiedTime": "2024-01-17T19:12:05+0000",
        "createdTime": "2021-11-15T16:42:22+0000",
    }
    team = Team(**team_dict)
    assert team.stub is True
    assert team.id == 1
    assert team.entity_type == "Teams"
    assert team.rev == "1"
    assert team.name == "Team A"
    assert team.modified_time == "2024-01-17T19:12:05+0000"
    assert team.created_time == "2021-11-15T16:42:22+0000"


def test_bad_team():
    team_dict = {
        "stub": True,
        "id": 1,
        "name": "Team A",
        "rev": "1",
        "entityType": "Users",
        "isEnabled": True,
        "modifiedTime": "2024-01-17T19:12:05+0000",
        "createdTime": "2021-11-15T16:42:22+0000",
    }
    with pytest.raises(ValidationError):
        Team(**team_dict)


def test_teamresponse():
    with open("findTeams.json") as f:
        team_response = FindTeamsResult.model_validate_json(f.read())
    for team in team_response.result:
        assert isinstance(team, Team)


def test_activitytypes():
    activity_dict = {
        "stub": True,
        "id": 1,
        "name": "Activity A",
        "entityType": "Activity_Types",
        "rev": "1",
    }
    activity = ActivityType(**activity_dict)
    assert activity.stub is True
    assert activity.id == 1
    assert activity.entity_type == "Activity_Types"
    assert activity.rev == "1"
    assert activity.name == "Activity A"


def test_activity_type_response():
    with open("findActivityTypes.json") as f:
        activity_response = FindActivityTypesResult.model_validate_json(f.read())
    for activity in activity_response.result:
        assert isinstance(activity, ActivityType)


def test_series_data():
    series_data = {
        "total_effort": [[1, 2], [3, 4]],
        "successful_effort": [[5, 6], [7, 8]],
    }
    series = TimeSeriesData(**series_data)
    assert series.total_effort == [[1, 2], [3, 4]]
    assert series.successful_effort == [[5, 6], [7, 8]]


def test_summary_data():
    summary_data = {"sum": 1.0, "avg": 2.0, "min": 3.0, "max": 4.0, "sum_delta": 5.0,
                    "avg_delta": 6.0, "min_delta": 7.0, "max_delta": 8.0, }

    summary = SummaryData(**summary_data)
    assert summary.sum == 1.0
    assert summary.avg == 2.0
    assert summary.min == 3.0
    assert summary.max == 4.0
    assert summary.sum_delta == 5.0
    assert summary.avg_delta == 6.0
    assert summary.min_delta == 7.0
    assert summary.max_delta == 8.0


def test_analytics_report():
    with open("analyticsReportQuotes.json") as f:
        report = GetAnalyticsReportResult.model_validate_json(f.read())
    result = report.result
    assert isinstance(result.series_data, TimeSeriesData)
    assert isinstance(result.summary_data["total_effort"], SummaryData)
    assert isinstance(result.summary_data["successful_effort"], SummaryData)


def test_stageset_response():
    with open("findStagesets.json") as f:
        stageset_response = FindStagesetsResult.model_validate_json(f.read())
    for stageset in stageset_response.result:
        assert isinstance(stageset, Stageset)


def test_milestones_response():
    with open("findMilestones.json") as f:
        milestones_response = FindMilestonesResult.model_validate_json(f.read())
    for milestone in milestones_response.result:
        assert isinstance(milestone, Milestone)


# revisit this test; not sure what it's here for
def test_lead_entity(testing_user, testing_milestone, test_stageset):
    test_lead = Lead(id=1, entityType="Leads", rev="1", name="Lead A", htmlUrl="http://example.com", tags=["tag1"],
                     description="This is a test lead", createdTime="2021-11-15T16:42:22+0000", creator=testing_user,
                     milestone=testing_milestone,
                     stageset=test_stageset, status=0, confidence=50, assignee=testing_user,
                     dueTime="2024-01-17T19:12:05+0000", value={"currency": "USD", "amount": 26365},
                     normalizedValue={"currency": "USD",
                                      "amount": 26365}, stub=True)


def test_lead_stub():
    with open("findLeadsStub.json") as f:
        leads = FindLeadsResult.model_validate_json(f.read())
    for lead in leads.result:
        assert isinstance(lead, Lead)


def test_lead_non_stub():
    with open("findLeadsNonStub.json") as f:
        leads = FindLeadsResult.model_validate_json(f.read())
    for lead in leads.result:
        assert isinstance(lead, Lead)


def test_activities_non_stub():
    with open("findActivitiesNonStub.json") as f:
        activities = FindActivitiesResult.model_validate_json(f.read())
    for activity in activities.result:
        assert isinstance(activity, Activity)


def test_activities_stub():
    with open("findActivitiesStub.json") as f:
        activities = FindActivitiesResult.model_validate_json(f.read())
    for activity in activities.result:
        assert isinstance(activity, Activity)
