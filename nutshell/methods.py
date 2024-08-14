from typing import Optional

from pydantic import BaseModel, computed_field

from nutshell.entities import AnalyticsReportType, FindLeadsQuery, ActivityType, User, Team, FindActivitiesQuery, \
    CreateActivity


class _APIMethod(BaseModel):
    """
    Base class for all method calls to the Nutshell API.

    This class should not be used directly, but should be subclassed for each API method.
    """
    api_method: str

    @computed_field
    @property
    def params(self) -> dict:
        return {}


class FindUsers(_APIMethod):
    """
    This method is used to retrieve a list of users from the Nutshell API.

    Attributes
    ----------
    query : Optional[dict]
        A dictionary of query parameters to filter the results.
    order_by : str
        The field to order the results by.
    order_direction : str
        The direction to order the results by.
    limit : int
        The maximum number of results to return.
    page : int
        The page of results to return.

    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API.

    """
    query: Optional[dict] = None
    order_by: str = "last_name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findUsers"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }
        if self.query:
            params["query"] = self.query

        return params


class GetUser(_APIMethod):
    """For retrieving a single user from the Nutshell API.
    
    Attributes
    ----------
    user_id : int
        The ID of the user to retrieve.
    rev : str
        The revision of the user to retrieve.
        
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API.
    """
    user_id: int = None  # with no user_id, the API will return the current user
    rev: str = None  # included to match API documentation
    api_method: str = "getUser"

    @computed_field
    @property
    def params(self) -> dict:
        params = {}
        if self.user_id:
            params["userId"] = self.user_id
        if self.rev:
            params["rev"] = self.rev
        return params


class FindTeams(_APIMethod):
    """For retrieving a list of teams from the Nutshell API.
    
    Attributes
    ----------
    order_by : str
        The field to order the results by.
    order_direction : str
        The direction to order the results by.
    limit : int
        The maximum number of results to return.
    page : int
        The page of results to return.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API.
    """
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findTeams"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }

        return params


class FindActivityTypes(_APIMethod):
    """For retrieving a list of activity types from the Nutshell API.
    
    Attributes
    ----------
    order_by : str
        The field to order the results by.
    order_direction : str
        The direction to order the results by.
    limit : int
        The maximum number of results to return.
    page : int
        The page of results to return.
        
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API.
    """
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findActivityTypes"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }

        return params


class GetAnalyticsReport(_APIMethod):
    """For building a valid query to the Nutshell API for the getAnalyticsReport method.
    
    Attributes
    ----------
    report_type : AnalyticsReportType
        The type of report to retrieve.
    period : str
        The period of the report to retrieve.
    filters : Optional[list[User | Team | ActivityType]]
        A list of entities to filter the report by.
    options : list[dict]
        A list of options to pass to the API.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API.
    """
    report_type: AnalyticsReportType
    period: str
    filters: Optional[list[User | Team | ActivityType]] = None
    options: list[dict] = None  # little documentation 
    api_method: str = "getAnalyticsReport"

    @computed_field
    @property
    def params(self) -> dict:
        params = {"reportType": self.report_type.value,
                  "period": self.period}
        if self.filters:
            params["filter"] = [{"entityId": entity.id, "entityName": entity.entity_type} for entity in self.filters]
        if self.options:
            params["options"] = self.options
        return params


class FindStagesets(_APIMethod):
    """For retreiving a list of pipelines (stagesets) from the Nutshell API.
    
    Attributes
    ----------
    order_by : str
        The field to order the results by.
    order_direction : str
        The direction to order the results by.
    limit : int
        The maximum number of results to return.
    page : int
        The page of results to return.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API.
    """
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findStagesets"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }
        return params


class FindMilestones(_APIMethod):
    """For retrieving a list of milestones from the Nutshell API.
    
    Attributes
    ----------
    order_by : str
        The field to order the results by.
    order_direction : str
        The direction to order the results by.
    limit : int
        The maximum number of results to return.
    page : int
        The page of results to return.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API
    """
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findMilestones"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }
        return params


class FindLeads(_APIMethod):
    """For retrieving a list of leads from the Nutshell API.
    
    Attributes
    ----------
    query : Optional[FindLeadsQuery]
        A query object to filter the results.
    order_by : str
        The field to order the results by.
    order_direction : str
        The direction to order the results by.
    limit : int
        The maximum number of results to return.
    page : int
        The page of results to return.
    stub_responses : bool
        Whether to return stub responses.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API."""
    query: Optional[FindLeadsQuery] = None
    order_by: str = "id"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    stub_responses: bool = True
    api_method: str = "findLeads"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "query": {},
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page,
            "stubResponses": self.stub_responses
        }
        if self.query:
            params["query"] = self.query.query
        return params


# TODO: add findActivities
class FindActivities(_APIMethod):
    """For retrieving a list of activities from the Nutshell API.
    
    Attributes
    ----------
    query : Optional[FindActivitiesQuery]
        A query object to filter the results.
    order_by : str
        The field to order the results by.
    order_direction : str
        The direction to order the results by.
    limit : int
        The maximum number of results to return.
    page : int
        The page of results to return.
    stub_responses : bool
        Whether to return stub responses.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API."""
    query: Optional[FindActivitiesQuery] = None
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    stub_responses: bool = True
    api_method: str = "findActivities"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "query": {},
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page,
            "stubResponses": self.stub_responses
        }
        if self.query:
            params["query"] = self.query.query
        return params


class NewActivity(_APIMethod):
    activity: CreateActivity
    api_method: str = "newActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activity": self.activity.model_dump(by_alias=True, exclude_none=True)
        }


class GetActivity(_APIMethod):
    """For retrieving a single activity from the Nutshell API.
    
    Attributes
    ----------
    activity_id : int
        The ID of the activity to retrieve.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API"""
    activity_id: int
    api_method: str = "getActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activityId": self.activity_id
        }


class EditActivity(_APIMethod):
    """For editing an activity in the Nutshell API.
    
    Attributes
    ----------
    activity_id : int
        The ID of the activity to edit.
    rev : str
        The revision of the activity to edit.
    activity : dict
        The updated activity data.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API"""
    activity_id: int
    rev: str
    activity: dict
    api_method: str = "editActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activityId": self.activity_id,
            "rev": self.rev,
            "activity": self.activity
        }


class DeleteActivity(_APIMethod):
    """For deleting an activity from the Nutshell API.
    
    Attributes
    ----------
    activity_id : int
        The ID of the activity to delete.
    rev : str
        The revision of the activity to delete.
    
    Computed Attributes
    -------------------
    params : dict
        A dictionary of the parameters to be passed to the API"""
    activity_id: int
    rev: str
    api_method: str = "deleteActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activityId": self.activity_id,
            "rev": self.rev
        }

# TODO: add getLead

# TODO: add findTimeline

# TODO: add searchLeads
