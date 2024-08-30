import os

import pytest
from dotenv import load_dotenv

from nutshell.nutshell_api import NutshellAPI
from nutshell.methods import FindUsers, GetUser, FindTeams, FindActivityTypes, GetAnalyticsReport, FindStagesets, \
    FindMilestones, \
    FindLeads, FindActivities, GetLead
from nutshell.entities import Lead, User, Team, ActivityType, AnalyticsReport, TimeSeriesData, Stageset, Milestone, \
    AnalyticsReportType, Activity

load_dotenv()


@pytest.fixture()
def api():
    return NutshellAPI(os.getenv("NUTSHELL_USERNAME"), password=os.getenv("NUTSHELL_KEY"))


def test_api_two_calls(api):
    find_users = FindUsers(limit=5)
    find_teams = FindTeams(limit=3)
    api.api_calls = [find_users, find_teams]
    assert len(api.api_calls) == 2


@pytest.mark.live_api
def test_find_users(api):
    find_users = FindUsers(limit=5)
    api.api_calls = find_users
    find_user_result = api.call_api().result
    assert isinstance(find_user_result, list)
    assert isinstance(find_user_result[0], User)


@pytest.mark.live_api
def test_get_user(api):
    single_user = GetUser()
    api.api_calls = single_user
    single_user_result = api.call_api().result
    assert isinstance(single_user_result, User)


@pytest.mark.live_api
def test_find_teams(api):
    find_teams = FindTeams(limit=3)
    api.api_calls = find_teams
    find_team_result = api.call_api().result
    assert isinstance(find_team_result, list)
    assert isinstance(find_team_result[0], Team)


@pytest.mark.live_api
def test_find_activity_types(api):
    find_activity_types = FindActivityTypes(limit=3)
    api.api_calls = find_activity_types
    find_activity_types_result = api.call_api().result
    assert isinstance(find_activity_types_result, list)
    assert isinstance(find_activity_types_result[0], ActivityType)


@pytest.mark.live_api
def test_get_analytics_report(api):
    user = User(id=13, entityType="Users", rev="16", name="John Doe", emails=["test@test.com"], isEnabled=True,
                isAdministrator=False, modifiedTime="2021-08-10T15:00:00Z", createdTime="2021-08-10T15:00:00Z")
    analytics_report = GetAnalyticsReport(report_type=AnalyticsReportType.EFFORT, period="-d30")
    api.api_calls = analytics_report
    analytics_report_result = api.call_api().result
    assert isinstance(analytics_report_result, AnalyticsReport)
    assert isinstance(analytics_report_result.series_data, TimeSeriesData)
    assert isinstance(analytics_report_result.summary_data, dict)
    assert isinstance(analytics_report_result.period_description, str)
    assert isinstance(analytics_report_result.delta_period_description, str)


@pytest.mark.live_api
def test_find_stagesets(api):
    stagesets = FindStagesets(limit=3)
    api.api_calls = stagesets
    stageset_result = api.call_api().result
    assert isinstance(stageset_result, list)
    assert isinstance(stageset_result[0], Stageset)


@pytest.mark.live_api
def test_find_milestones(api):
    milestone = FindMilestones(limit=3)
    api.api_calls = milestone
    milestone_result = api.call_api().result
    assert isinstance(milestone_result, list)
    assert isinstance(milestone_result[0], Milestone)


@pytest.mark.live_api
def test_find_leads(api):
    find_leads = FindLeads(limit=5)
    api.api_calls = find_leads
    find_leads_result = api.call_api().result
    assert isinstance(find_leads_result, list)
    assert isinstance(find_leads_result[0], Lead)


@pytest.mark.live_api
def test_find_activities(api):
    find_activities = FindActivities(limit=5)
    api.api_calls = find_activities
    find_activities_result = api.call_api().result
    assert isinstance(find_activities_result, list)
    assert isinstance(find_activities_result[0], Activity)


@pytest.mark.live_api
def test_get_lead(api):
    get_lead = GetLead(lead_id=23195)  # need a valid lead_id, will be dependent on your instance of Nutshell
    api.api_calls = get_lead
    get_lead_result = api.call_api().result
    assert isinstance(get_lead_result, Lead)
