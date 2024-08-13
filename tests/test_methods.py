import pydantic
import pytest

from pytest import mark

from nutshell.entities import FindLeadsQueryFilter, FindLeadsQueryStatus, Team, User, AnalyticsReportType, \
    ActivityStatus, CreateActivity
from nutshell.methods import FindUsers, GetUser, GetAnalyticsReport, FindTeams, FindActivityTypes, \
    FindStagesets, FindMilestones, FindLeads, FindLeadsQuery, FindActivities, FindActivitiesQuery, EditActivity, \
    NewActivity, GetActivity


def test_find_users_query():
    find_users = FindUsers(query={"email": "test@test.com"})

    assert find_users.params == {"query": {"email": "test@test.com"}, "orderBy": "last_name", "orderDirection": "ASC",
                                 "limit": 50, "page": 1}


def test_find_users_no_query():
    find_users = FindUsers()

    assert find_users.params == {"orderBy": "last_name", "orderDirection": "ASC",
                                 "limit": 50, "page": 1}


def test_find_users_100_limit():
    find_users = FindUsers(limit=100)

    assert find_users.params == {"orderBy": "last_name", "orderDirection": "ASC", "page": 1, "limit": 100}


def test_get_user():
    get_user = GetUser(user_id=1)

    assert get_user.params == {"userId": 1}


def test_get_user_no_id():
    GetUser()
    assert GetUser().params == {}


def test_get_user_with_rev():
    get_user = GetUser(user_id=1, rev="1")

    assert get_user.params == {"userId": 1, "rev": "1"}


def test_find_teams():
    find_teams = FindTeams()

    assert find_teams.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 50, "page": 1}


def test_find_activity_types():
    find_activity_types = FindActivityTypes()

    assert find_activity_types.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 50, "page": 1}


def test_get_analytics_report():
    user_one = User(id=1, name="John Doe", rev="1", entityType="Users", emails=["mail@test.com"], isEnabled=True,
                    stub=True,
                    isAdministrator=True, modifiedTime="2021-01-01T00:00:00Z", createdTime="2021-01-01T00:00:00Z")
    report = GetAnalyticsReport(report_type=AnalyticsReportType.EFFORT, period="-d30", filters=[user_one])

    assert report.params == {"reportType": "Effort", "filter": [{"entityId": 1, "entityName": "Users"}],
                             "period": "-d30"}


def test_get_analytics_report_missing_period():
    user_one = User(id=1, name="John Doe", rev="1", entityType="Users", emails=["mail@test.com"], isEnabled=True,
                    stub=True,
                    isAdministrator=True, modifiedTime="2021-01-01T00:00:00Z", createdTime="2021-01-01T00:00:00Z")
    with pytest.raises(pydantic.ValidationError):
        GetAnalyticsReport(report_type=AnalyticsReportType.EFFORT, filters=[user_one])


def test_find_stagesets():
    find_stagesets = FindStagesets(order_by="name", order_direction="ASC", limit=5, page=1)

    assert find_stagesets.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 5, "page": 1}


def test_findstagesets_empty():
    find_stagesets = FindStagesets()

    assert find_stagesets.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 50, "page": 1}


def test_find_milestones():
    find_milestones = FindMilestones(order_by="name", order_direction="ASC", limit=100, page=1)

    assert find_milestones.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 100, "page": 1}


def test_find_milestones_bare():
    find_milestones = FindMilestones()

    assert find_milestones.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 50, "page": 1}


def test_find_leads_bare():
    find_leads = FindLeads()

    assert find_leads.params == {"orderBy": "id", "orderDirection": "ASC", "limit": 50, "page": 1,
                                 "stubResponses": True, "query": {}}


def test_find_leads_full():
    find_leads = FindLeads(order_by="name", order_direction="DESC", limit=100, page=2, stub_responses=False)

    assert find_leads.params == {"orderBy": "name", "orderDirection": "DESC", "limit": 100, "page": 2,
                                 "stubResponses": False, "query": {}}


def test_find_lead_query_min():
    find_lead_query = FindLeadsQuery(status=FindLeadsQueryStatus.OPEN, filter=FindLeadsQueryFilter.ALL_LEADS)

    assert find_lead_query.query == {"status": 0, "filter": 2}


def test_find_lead_query_assignee():
    team_one = Team(stub=True, id=1, name="Team One", rev="1", entityType="Teams",
                    modifiedTime="2021-01-01T00:00:00Z",
                    createdTime="2021-01-01T00:00:00Z")
    user_one = User(id=1, name="John Doe", rev="1", entityType="Users", emails=["test@mail.com"], isEnabled=True,
                    stub=True,
                    isAdministrator=True, modifiedTime="2021-01-01T00:00:00Z", createdTime="2021-01-01T00:00:00Z")

    find_lead_query = FindLeadsQuery(status=FindLeadsQueryStatus.OPEN, filter=FindLeadsQueryFilter.ALL_LEADS,
                                     assignee=[team_one, user_one])

    assert find_lead_query.query == {"status": 0, "filter": 2,
                                     "assignee": [{"entityType": "Teams", "id": 1}, {"entityType": "Users", "id": 1}]}


def test_find_lead_with_query():
    team_one = Team(stub=True, id=1, name="Team One", rev="1", entityType="Teams",
                    modifiedTime="2021-01-01T00:00:00Z",
                    createdTime="2021-01-01T00:00:00Z")
    user_one = User(id=1, name="John Doe", rev="1", entityType="Users", emails=["test@mail.com"], isEnabled=True,
                    stub=True,
                    isAdministrator=True, modifiedTime="2021-01-01T00:00:00Z", createdTime="2021-01-01T00:00:00Z")

    find_lead_query = FindLeadsQuery(status=FindLeadsQueryStatus.OPEN, filter=FindLeadsQueryFilter.ALL_LEADS,
                                     assignee=[team_one, user_one])

    find_leads = FindLeads(query=find_lead_query)

    assert find_leads.params == {"orderBy": "id", "orderDirection": "ASC", "limit": 50, "page": 1,
                                 "stubResponses": True, "query": {"status": 0, "filter": 2,
                                                                  "assignee": [{"entityType": "Teams", "id": 1},
                                                                               {"entityType": "Users", "id": 1}]}}


def test_find_activities_min():
    find_activities = FindActivities()

    assert find_activities.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 50, "page": 1,
                                      "stubResponses": True, "query": {}}


@mark.parametrize("status, expected", [(ActivityStatus.SCHEDULED, 0), (ActivityStatus.LOGGED, 1)])
def test_find_activities_with_query(status, expected):
    query = FindActivitiesQuery(status=status)

    find_activities = FindActivities(query=query)

    assert find_activities.params == {"orderBy": "name", "orderDirection": "ASC", "limit": 50, "page": 1,
                                      "stubResponses": True, "query": {"status": expected}}


def test_edit_activity_minimal():
    edit_activity = EditActivity(activity_id=1, rev="1", activity={"name": "New Name"})

    assert edit_activity.params == {"activityId": 1, "rev": "1", "activity": {"name": "New Name"}}


def test_new_activity():
    created_activity = CreateActivity(name="New activity", description="New description", activity_type_id=1,
                                      start_time="2024-02-13T14:53:27+01:00", end_time="2024-02-13T14:53:27+01:00")

    new_activity = NewActivity(activity=created_activity)

    assert new_activity.params == {
        "activity": {"name": "New activity", "description": "New description", "activityTypeId": 1,
                     "startTime": "2024-02-13T14:53:27+01:00", "endTime": "2024-02-13T14:53:27+01:00"}}


def test_get_activity():
    get_activity = GetActivity(activity_id=1)

    assert get_activity.params == {"activityId": 1}
