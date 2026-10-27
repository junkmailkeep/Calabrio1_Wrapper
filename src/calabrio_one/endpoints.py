"""Generated typed WFM methods. See tools/generate_endpoints.py."""
from abc import ABC, abstractmethod
from datetime import date, datetime  # noqa: F401
from typing import Any
from uuid import UUID  # noqa: F401

from calabrio_one._arguments import UNSET, Unset


class WFMEndpoints(ABC):
    """One named method per public WFM operation; no raw payload required."""
    _wfm_schemas: dict = {'DateTimePeriodDto': {'type': 'object', 'properties': {'StartTime': {'type': 'string', 'format': 'date-time'}, 'EndTime': {'type': 'string', 'format': 'date-time'}}, 'additionalProperties': False}, 'IntervalWiseActualHeads': {'type': 'object', 'required': ['ActualStaffHeads', 'StartDateTime'], 'properties': {'StartDateTime': {'type': 'string', 'format': 'date-time'}, 'ActualStaffHeads': {'type': 'number', 'format': 'double'}}, 'additionalProperties': False}, 'IntervalWiseActualDto': {'type': 'object', 'required': ['StartDateTime'], 'properties': {'StartDateTime': {'type': 'string', 'format': 'date-time'}, 'ActualVolume': {'type': 'number', 'format': 'double', 'nullable': True}, 'ActualAht': {'type': 'number', 'format': 'double', 'nullable': True}, 'BusyHours': {'type': 'number', 'format': 'double', 'nullable': True}}, 'additionalProperties': False}, 'DateOnlyPeriodDto': {'type': 'object', 'properties': {'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'EndDate': {'type': 'string', 'format': 'date', 'nullable': True}}, 'additionalProperties': False}, 'AddMeetingInfoDto': {'type': 'object', 'required': ['ActivityId', 'ExternalMeetingId', 'Participants', 'Period'], 'properties': {'ExternalMeetingId': {'type': 'string'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'Participants': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'ActivityId': {'type': 'string', 'format': 'guid'}, 'Title': {'type': 'string', 'nullable': True}, 'Location': {'type': 'string', 'nullable': True}, 'Agenda': {'type': 'string', 'nullable': True}}, 'additionalProperties': False}, 'IntervalWiseScheduledHeadsDto': {'type': 'object', 'required': ['ScheduledHeads', 'StartDateTime'], 'properties': {'StartDateTime': {'type': 'string', 'format': 'date-time'}, 'ScheduledHeads': {'type': 'number', 'format': 'double'}}, 'additionalProperties': False}, 'EditMeetingInfoDto': {'type': 'object', 'required': ['ExternalMeetingId'], 'properties': {'ExternalMeetingId': {'type': 'string'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto', 'nullable': True}, 'Participants': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}, 'ActivityId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Title': {'type': 'string', 'nullable': True}, 'Location': {'type': 'string', 'nullable': True}, 'Agenda': {'type': 'string', 'nullable': True}}, 'additionalProperties': False}, 'BacklogQueueTask': {'type': 'object', 'required': ['AfterTaskWorkTimeSeconds', 'IsHandledWithinServiceLevel', 'OfferedAt', 'QueueId', 'QueueName', 'QueuingTimeSeconds', 'TaskId', 'TaskStatusDescription', 'TaskWorkTimeSeconds'], 'properties': {'QueueId': {'type': 'string'}, 'QueueName': {'type': 'string'}, 'TaskId': {'type': 'string'}, 'OfferedAt': {'type': 'string', 'format': 'date-time'}, 'FirstHandledAt': {'type': 'string', 'format': 'date-time', 'nullable': True}, 'CompletedAt': {'type': 'string', 'format': 'date-time', 'nullable': True}, 'TaskWorkTimeSeconds': {'type': 'integer', 'format': 'int32'}, 'AfterTaskWorkTimeSeconds': {'type': 'integer', 'format': 'int32'}, 'QueuingTimeSeconds': {'type': 'integer', 'format': 'int32'}, 'IsHandledWithinServiceLevel': {'type': 'boolean'}, 'TaskStatusDescription': {'type': 'string'}}, 'additionalProperties': False}, 'SetForecastDayDto': {'type': 'object', 'properties': {'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Intervals': {'type': 'array', 'nullable': True, 'items': {'$ref': '#/components/schemas/SetForecastIntervalDto'}}}, 'additionalProperties': False}, 'SetForecastIntervalDto': {'type': 'object', 'properties': {'Tasks': {'type': 'number', 'format': 'double'}, 'AverageTaskTimeSeconds': {'type': 'number', 'format': 'double'}, 'AverageAfterTaskTimeSeconds': {'type': 'number', 'format': 'double'}, 'AgentsOverride': {'type': 'number', 'format': 'double', 'nullable': True}, 'StartTimeUtc': {'type': 'string', 'format': 'date-time'}}, 'additionalProperties': False}, 'SetForecastDailyDayDto': {'type': 'object', 'properties': {'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Tasks': {'type': 'number', 'format': 'double', 'nullable': True}, 'AverageTaskTimeSeconds': {'type': 'number', 'format': 'double', 'nullable': True}, 'AverageAfterTaskTimeSeconds': {'type': 'number', 'format': 'double', 'nullable': True}, 'WorkLoadId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, 'ScheduleDayDto': {'type': 'object', 'required': ['Date'], 'properties': {'Date': {'type': 'string', 'format': 'date'}, 'ShiftCategoryId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'DayOffTemplateId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'FullDayAbsenceId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'AttributeId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Layers': {'type': 'array', 'nullable': True, 'items': {'$ref': '#/components/schemas/LayerDto'}}}, 'additionalProperties': False}, 'LayerDto': {'type': 'object', 'required': ['Period'], 'properties': {'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'ActivityId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'AbsenceId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'AttributeId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, 'SetShrinkageDayDto': {'type': 'object', 'properties': {'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Intervals': {'type': 'array', 'nullable': True, 'items': {'$ref': '#/components/schemas/SetShrinkageIntervalDto'}}}, 'additionalProperties': False}, 'SetShrinkageIntervalDto': {'type': 'object', 'properties': {'StartTimeUtc': {'type': 'string', 'format': 'date-time'}, 'Shrinkage': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, 'PersonIncludeDto': {'type': 'object', 'properties': {'OptionalColumns': {'type': 'boolean'}}, 'additionalProperties': False}}
    _wfm_requests: dict = {'/command/AddActivityRequest': {'type': 'object', 'nullable': True, 'required': ['ActivityId', 'BusinessUnitId', 'Period', 'PersonId', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'ActivityId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}}, 'additionalProperties': False}, '/command/AddActualHeadsPerDp': {'type': 'object', 'nullable': True, 'required': ['DpId', 'IntervalWiseActualHeads', 'TimeZone'], 'properties': {'TimeZone': {'type': 'string'}, 'DpId': {'type': 'string', 'format': 'guid'}, 'IntervalWiseActualHeads': {'type': 'array', 'items': {'$ref': '#/components/schemas/IntervalWiseActualHeads'}}}, 'additionalProperties': False}, '/command/AddActualPerDpWorkload': {'type': 'object', 'nullable': True, 'required': ['DpId', 'IntervalWiseActual', 'TimeZone', 'WorkloadId'], 'properties': {'TimeZone': {'type': 'string'}, 'DpId': {'type': 'string', 'format': 'guid'}, 'WorkloadId': {'type': 'string', 'format': 'guid'}, 'IntervalWiseActual': {'type': 'array', 'items': {'$ref': '#/components/schemas/IntervalWiseActualDto'}}}, 'additionalProperties': False}, '/command/AddFullDayAbsence': {'type': 'object', 'nullable': True, 'required': ['AbsenceId', 'BusinessUnitId', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto', 'nullable': True}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'AbsenceId': {'type': 'string', 'format': 'guid'}, 'AttributeId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/command/AddFullDayAbsenceRequest': {'type': 'object', 'nullable': True, 'required': ['AbsenceId', 'BusinessUnitId', 'Message', 'Period', 'PersonId', 'Subject'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'AbsenceId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'Subject': {'type': 'string'}, 'Message': {'type': 'string'}}, 'additionalProperties': False}, '/command/AddIntradayAbsenceRequest': {'type': 'object', 'nullable': True, 'required': ['AbsenceId', 'BusinessUnitId', 'Message', 'Period', 'PersonId', 'Subject', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'AbsenceId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'Subject': {'type': 'string'}, 'Message': {'type': 'string'}}, 'additionalProperties': False}, '/command/AddMeetings': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'ExternalMeetings', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'ExternalMeetings': {'type': 'array', 'items': {'$ref': '#/components/schemas/AddMeetingInfoDto'}}, 'HandleNonOverwritableActivities': {'type': 'string', 'nullable': True}}, 'additionalProperties': False}, '/command/AddOrUpdatePersonAccountForPerson': {'type': 'object', 'nullable': True, 'required': ['AbsenceId', 'DateFrom', 'PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'AbsenceId': {'type': 'string', 'format': 'guid'}, 'DateFrom': {'type': 'string', 'format': 'date'}, 'BalanceIn': {'type': 'integer', 'format': 'int32'}, 'Extra': {'type': 'integer', 'format': 'int32'}, 'Accrued': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, '/command/AddOvertime': {'type': 'object', 'nullable': True, 'required': ['ActivityId', 'BusinessUnitId', 'MultiplicatorDefinitionSetId', 'Period', 'PersonId', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'ActivityId': {'type': 'string', 'format': 'guid'}, 'MultiplicatorDefinitionSetId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/command/AddOvertimeRequest': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Message', 'OvertimeType', 'Period', 'PersonId', 'Subject', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'Subject': {'type': 'string'}, 'Message': {'type': 'string'}, 'OvertimeType': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/command/AddPartDayAbsence': {'type': 'object', 'nullable': True, 'required': ['AbsenceId', 'BusinessUnitId', 'Period', 'PersonId', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'AbsenceId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'ConvertIfApplicableForFullDay': {'type': 'integer', 'format': 'int32'}, 'AttributeId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/command/AddPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'FirstName': {'type': 'string', 'nullable': True}, 'LastName': {'type': 'string', 'nullable': True}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'Email': {'type': 'string', 'nullable': True}, 'EmploymentNumber': {'type': 'string', 'nullable': True}, 'ApplicationLogon': {'type': 'string', 'nullable': True}, 'Identity': {'type': 'string', 'nullable': True}, 'TeamId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'ContractId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'ContractScheduleId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'PartTimePercentageId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'RoleIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}, 'WorkflowControlSetId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'ShiftBagId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'BudgetGroupId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'FirstDayOfWeek': {'type': 'integer', 'format': 'int32', 'nullable': True}, 'Culture': {'type': 'string', 'nullable': True}}, 'additionalProperties': False}, '/command/AddScheduleChangesListener': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'DaysEndFromCurrentDate', 'DaysStartFromCurrentDate', 'Name', 'Url'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'Url': {'type': 'string'}, 'Name': {'type': 'string'}, 'DaysStartFromCurrentDate': {'type': 'integer', 'format': 'int32'}, 'DaysEndFromCurrentDate': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, '/command/AddScheduledHeadsPerDp': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'DpId', 'IntervalWiseScheduledHeads', 'TimeZone'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'TimeZone': {'type': 'string'}, 'DpId': {'type': 'string', 'format': 'guid'}, 'IntervalWiseScheduledHeads': {'type': 'array', 'items': {'$ref': '#/components/schemas/IntervalWiseScheduledHeadsDto'}}}, 'additionalProperties': False}, '/command/AddSkillsToPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'SkillIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}}, 'additionalProperties': False}, '/command/AddTeam': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'TeamName'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'TeamName': {'type': 'string'}, 'SiteId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/command/ClearLeavingDateForPerson': {'type': 'object', 'nullable': True, 'required': ['PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/command/DeleteAccountForPersonAccount': {'type': 'object', 'nullable': True, 'required': ['AbsenceId', 'DateFrom', 'PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'DateFrom': {'type': 'string', 'format': 'date'}, 'AbsenceId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/command/EditMeetings': {'type': 'object', 'nullable': True, 'required': ['ExternalMeetings'], 'properties': {'TimeZoneId': {'type': 'string', 'nullable': True}, 'ExternalMeetings': {'type': 'array', 'items': {'$ref': '#/components/schemas/EditMeetingInfoDto'}}, 'HandleNonOverwritableActivities': {'type': 'string', 'nullable': True}}, 'additionalProperties': False}, '/command/ImportBacklogQueue': {'type': 'object', 'nullable': True, 'required': ['Tasks', 'UploadId'], 'properties': {'Tasks': {'type': 'array', 'items': {'$ref': '#/components/schemas/BacklogQueueTask'}}, 'UploadId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/command/ProcessBacklogQueue': {'type': 'object', 'nullable': True, 'additionalProperties': False}, '/command/RemoveFullDayAbsence': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/command/RemoveMeetings': {'type': 'object', 'nullable': True, 'required': ['ExternalMeetingIds'], 'properties': {'ExternalMeetingIds': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False}, '/command/RemoveOvertime': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/command/RemovePartDayAbsence': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'AbsenceIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}, 'AttributeIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}}, 'additionalProperties': False}, '/command/RemoveSkillsForPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'SkillIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}}, 'additionalProperties': False}, '/command/SetAvailability': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'AvailabilityId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}}, 'additionalProperties': False}, '/command/SetBudgetGroupForPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'BudgetGroupId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/command/SetDetailsForPerson': {'type': 'object', 'nullable': True, 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'FirstName': {'type': 'string', 'nullable': True}, 'LastName': {'type': 'string', 'nullable': True}, 'Email': {'type': 'string', 'nullable': True}, 'WorkflowControlSetId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Note': {'type': 'string', 'nullable': True}, 'EmploymentNumber': {'type': 'string', 'nullable': True}, 'Identity': {'type': 'string', 'nullable': True}}, 'additionalProperties': False}, '/command/SetEmploymentDetailsForPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'ContractId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'ContractScheduleId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'PartTimePercentageId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'TeamId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/command/SetExternalLogonsForPerson': {'type': 'object', 'nullable': True, 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'ExternalLogonIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}}, 'additionalProperties': False}, '/command/SetForecast': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'SkillId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Days': {'type': 'array', 'nullable': True, 'items': {'$ref': '#/components/schemas/SetForecastDayDto'}}}, 'additionalProperties': False}, '/command/SetForecastDaily': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'SkillId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Days': {'type': 'array', 'nullable': True, 'items': {'$ref': '#/components/schemas/SetForecastDailyDayDto'}}}, 'additionalProperties': False}, '/command/SetLeavingDateForPerson': {'type': 'object', 'nullable': True, 'required': ['Date', 'PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}, '/command/SetLocation': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonIds'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonIds': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'Location': {'type': 'string', 'nullable': True}}, 'additionalProperties': False}, '/command/SetNoteForScheduleDay': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Date', 'IsPublic', 'Note', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}, 'Note': {'type': 'string'}, 'IsPublic': {'type': 'boolean'}}, 'additionalProperties': False}, '/command/SetOptionalColumnForPeople': {'type': 'object', 'nullable': True, 'required': ['OptionalColumnId', 'PersonIds', 'Value'], 'properties': {'PersonIds': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'OptionalColumnId': {'type': 'string', 'format': 'guid'}, 'Value': {'type': 'string'}}, 'additionalProperties': False}, '/command/SetOptionalColumnForPerson': {'type': 'object', 'nullable': True, 'required': ['OptionalColumnId', 'PersonId', 'Value'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'OptionalColumnId': {'type': 'string', 'format': 'guid'}, 'Value': {'type': 'string'}}, 'additionalProperties': False}, '/command/SetRolesForPerson': {'type': 'object', 'nullable': True, 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'RoleIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}}, 'additionalProperties': False}, '/command/SetRotation': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'RotationId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'StartWeek': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, '/command/SetSchedulesForPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'DatePeriod', 'PersonId', 'ScheduleDays', 'TimeZoneId'], 'properties': {'TimeZoneId': {'type': 'string'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'DatePeriod': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScheduleDays': {'type': 'array', 'items': {'$ref': '#/components/schemas/ScheduleDayDto'}}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/command/SetShiftBagForPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'ShiftBagId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/command/SetShrinkage': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'SkillId': {'type': 'string', 'format': 'guid'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Days': {'type': 'array', 'nullable': True, 'items': {'$ref': '#/components/schemas/SetShrinkageDayDto'}}}, 'additionalProperties': False}, '/command/SetSkillsForPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'SkillIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid'}}}, 'additionalProperties': False}, '/command/SetTeamForPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'StartDate': {'type': 'string', 'format': 'date', 'nullable': True}, 'TeamId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Absence/AllAbsences': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'Filter': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, '/query/AbsenceAttribute/GetAbsenceAttribute': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/AbsenceAttribute/GetAllAbsenceAttribute': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/AbsencePossibility/AbsencePossibilityByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}}, 'additionalProperties': False}, '/query/AbsenceRequest/AbsenceRequestById': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'RequestId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'RequestId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/AbsenceRequestRule/AbsenceRequestRulesByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}}, 'additionalProperties': False}, '/query/Activity/ActivitiesAvailableForRequestByPersonAndDate': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Date', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}, '/query/Activity/AllActivities': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'Filter': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, '/query/ActivityRequest/ActivityRequestById': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'RequestId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'RequestId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/ApplicationFunction/PermissionByPerson': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Availability/AllAvailabilities': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/BudgetGroup/AllBudgetGroups': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/BusinessUnit/AllBusinessUnits': {'type': 'object', 'nullable': True, 'additionalProperties': False}, '/query/Contract/AllContracts': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/ContractSchedule/AllContractSchedules': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/DayOffTemplate/AllDayOffTemplates': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/EmployeeDefaults/GetEmployeeDefaults': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/ExternalLogon/ExternalLogonById': {'type': 'object', 'nullable': True, 'required': ['Id'], 'properties': {'Id': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/ExternalLogon/ExternalLogonsByDataSource': {'type': 'object', 'nullable': True, 'required': ['DataSourceId'], 'properties': {'DataSourceId': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, '/query/ExternalLogon/ExternalLogonsByPerson': {'type': 'object', 'nullable': True, 'required': ['Date', 'PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}, '/query/Forecast/ForecastBySkill': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'SkillId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'SkillId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ApplyShrinkage': {'type': 'boolean'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/Location/LocationsByPersonIds': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonIds'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonIds': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}}, 'additionalProperties': False}, '/query/MultiplicatorDefinitionSet/AllMultiplicatorDefinitionSets': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/NightlyRest/NightlyRestByPersonId': {'type': 'object', 'nullable': True, 'required': ['Date', 'PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}, '/query/OptionalColumn/AllOptionalColumns': {'type': 'object', 'nullable': True, 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/OvertimePossibility/OvertimePossibilityByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}}, 'additionalProperties': False}, '/query/OvertimeRequest/OvertimeRequestById': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'RequestId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'RequestId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/OvertimeRequestConfiguration/OvertimeRequestConfigurationByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Date', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}, '/query/OvertimeValidPossibility/OvertimeValidPossibilityByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}}, 'additionalProperties': False}, '/query/PartTimePercentage/AllPartTimePercentages': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Person/PeopleByBusinessUnitId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Page': {'type': 'integer', 'format': 'int32'}, 'PageSize': {'type': 'integer', 'format': 'int32'}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/Person/PeopleByEmploymentNumbers': {'type': 'object', 'nullable': True, 'required': ['EmploymentNumbers'], 'properties': {'EmploymentNumbers': {'type': 'array', 'items': {'type': 'string'}}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/Person/PeopleByGroupPageGroup': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'GroupPageGroupId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/Person/PeopleByIdentities': {'type': 'object', 'nullable': True, 'required': ['Identities'], 'properties': {'Identities': {'type': 'array', 'items': {'type': 'string'}}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/Person/PeopleByIds': {'type': 'object', 'nullable': True, 'required': ['Ids'], 'properties': {'Ids': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/Person/PeopleBySkillGroup': {'type': 'object', 'nullable': True, 'properties': {'SkillGroupId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/Person/PeopleByTeamId': {'type': 'object', 'nullable': True, 'properties': {'TeamId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/Person/PersonById': {'type': 'object', 'nullable': True, 'required': ['PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date', 'nullable': True}, 'Include': {'$ref': '#/components/schemas/PersonIncludeDto', 'nullable': True}}, 'additionalProperties': False}, '/query/PersonAccount/PersonAccountsByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Date', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}, '/query/Role/AllRoles': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'GetApplicationFunctionsAndAvailableData': {'type': 'boolean'}}, 'additionalProperties': False}, '/query/Rotation/AllRotations': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'IncludeDetails': {'type': 'boolean'}}, 'additionalProperties': False}, '/query/Rotation/RotationById': {'type': 'object', 'nullable': True, 'required': ['RotationId'], 'properties': {'RotationId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Scenario/AllScenarios': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Schedule/ScheduleByPersonId': {'type': 'object', 'nullable': True, 'required': ['Period', 'PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/Schedule/ScheduleByPersonIds': {'type': 'object', 'nullable': True, 'required': ['Period', 'PersonIds'], 'properties': {'PersonIds': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/Schedule/ScheduleByTeamId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'TeamId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'TeamId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/ScheduleAbsence/ScheduleAbsencesByPersonIds': {'type': 'object', 'nullable': True, 'required': ['Period', 'PersonIds'], 'properties': {'PersonIds': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/ScheduleAuditTrail/ScheduleAuditTrailByPersonId': {'type': 'object', 'nullable': True, 'required': ['Date'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/ScheduleChanges/SchedulesByChangeDate': {'type': 'object', 'nullable': True, 'required': ['ChangesFrom', 'Page'], 'properties': {'ChangesFrom': {'type': 'string', 'format': 'date-time'}, 'ChangesTo': {'type': 'string', 'format': 'date-time', 'nullable': True}, 'Page': {'type': 'integer', 'format': 'int32'}, 'PageSize': {'type': 'integer', 'format': 'int32'}, 'BusinessUnitId': {'type': 'string', 'format': 'guid', 'nullable': True}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto', 'nullable': True}}, 'additionalProperties': False}, '/query/ScheduleChangesListenerSubscription/AllScheduleChangesListenerSubscription': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/ScheduleOrder/ScheduleByGroupPageGroups': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'GroupPageGroupIds', 'Period'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'GroupPageGroupIds': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/ShiftBag/AllShiftBags': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/ShiftCategory/AllShiftCategories': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Site/AllSites': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Skill/AllSkills': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/SkillGroup/AllSkillGroups': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Staffing/StaffingBySkills': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'SkillIds'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'SkillIds': {'type': 'array', 'items': {'type': 'string', 'format': 'guid'}}, 'Period': {'$ref': '#/components/schemas/DateTimePeriodDto'}}, 'additionalProperties': False}, '/query/Team/AllTeams': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Team/AllTeamsWithAgents': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}}, 'additionalProperties': False}, '/query/Team/TeamById': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'Id': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/Team/TeamsBySiteId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'SiteId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/User/UserById': {'type': 'object', 'nullable': True, 'required': ['PersonId'], 'properties': {'PersonId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}, '/query/WeeklyMaxWorkTime/WeeklyMaxWorkTimeByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Date', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Date': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}, '/query/WorkLoad/WorkloadBySkillIds': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'SkillIds': {'type': 'array', 'nullable': True, 'items': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'Page': {'type': 'integer', 'format': 'int32'}, 'PageSize': {'type': 'integer', 'format': 'int32'}}, 'additionalProperties': False}, '/query/WorkTime/WorkTimeByPersonId': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId', 'Period', 'PersonId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}, 'PersonId': {'type': 'string', 'format': 'guid'}, 'Period': {'$ref': '#/components/schemas/DateOnlyPeriodDto'}, 'ScenarioId': {'type': 'string', 'format': 'guid', 'nullable': True}}, 'additionalProperties': False}, '/query/WorkflowControlSet/AllWorkflowControlSets': {'type': 'object', 'nullable': True, 'required': ['BusinessUnitId'], 'properties': {'BusinessUnitId': {'type': 'string', 'format': 'guid'}}, 'additionalProperties': False}}

    @abstractmethod
    def _operation(self, path: str, names: dict, payload: dict | None, kwargs: dict) -> Any:
        """Dispatch supplied API fields through the implementing client."""
        ...

    def add_activity_request(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        activity_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddActivityRequest.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'person_id': person_id, 'activity_id': activity_id, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddActivityRequest', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'activity_id': 'ActivityId', 'period': 'Period'}, payload, supplied)

    def add_actual_heads_per_dp(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone: str | Unset = UNSET,
        dp_id: str | UUID | Unset = UNSET,
        interval_wise_actual_heads: list[Any] | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddActualHeadsPerDp.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone': time_zone, 'dp_id': dp_id, 'interval_wise_actual_heads': interval_wise_actual_heads}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddActualHeadsPerDp', {'time_zone': 'TimeZone', 'dp_id': 'DpId', 'interval_wise_actual_heads': 'IntervalWiseActualHeads'}, payload, supplied)

    def add_actual_per_dp_workload(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone: str | Unset = UNSET,
        dp_id: str | UUID | Unset = UNSET,
        workload_id: str | UUID | Unset = UNSET,
        interval_wise_actual: list[Any] | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddActualPerDpWorkload.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone': time_zone, 'dp_id': dp_id, 'workload_id': workload_id, 'interval_wise_actual': interval_wise_actual}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddActualPerDpWorkload', {'time_zone': 'TimeZone', 'dp_id': 'DpId', 'workload_id': 'WorkloadId', 'interval_wise_actual': 'IntervalWiseActual'}, payload, supplied)

    def add_full_day_absence(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | None | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        absence_id: str | UUID | Unset = UNSET,
        attribute_id: str | UUID | None | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddFullDayAbsence.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'date': date, 'absence_id': absence_id, 'attribute_id': attribute_id, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddFullDayAbsence', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'date': 'Date', 'absence_id': 'AbsenceId', 'attribute_id': 'AttributeId', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def add_full_day_absence_request(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        absence_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        subject: str | Unset = UNSET,
        message: str | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddFullDayAbsenceRequest.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'absence_id': absence_id, 'period': period, 'subject': subject, 'message': message}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddFullDayAbsenceRequest', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'absence_id': 'AbsenceId', 'period': 'Period', 'subject': 'Subject', 'message': 'Message'}, payload, supplied)

    def add_intraday_absence_request(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        absence_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        subject: str | Unset = UNSET,
        message: str | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddIntradayAbsenceRequest.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'person_id': person_id, 'absence_id': absence_id, 'period': period, 'subject': subject, 'message': message}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddIntradayAbsenceRequest', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'absence_id': 'AbsenceId', 'period': 'Period', 'subject': 'Subject', 'message': 'Message'}, payload, supplied)

    def add_meetings(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
        external_meetings: list[Any] | Unset = UNSET,
        handle_non_overwritable_activities: str | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddMeetings.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'scenario_id': scenario_id, 'external_meetings': external_meetings, 'handle_non_overwritable_activities': handle_non_overwritable_activities}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddMeetings', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'scenario_id': 'ScenarioId', 'external_meetings': 'ExternalMeetings', 'handle_non_overwritable_activities': 'HandleNonOverwritableActivities'}, payload, supplied)

    def add_or_update_person_account_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        absence_id: str | UUID | Unset = UNSET,
        date_from: str | date | Unset = UNSET,
        balance_in: int | Unset = UNSET,
        extra: int | Unset = UNSET,
        accrued: int | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddOrUpdatePersonAccountForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'absence_id': absence_id, 'date_from': date_from, 'balance_in': balance_in, 'extra': extra, 'accrued': accrued}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddOrUpdatePersonAccountForPerson', {'person_id': 'PersonId', 'absence_id': 'AbsenceId', 'date_from': 'DateFrom', 'balance_in': 'BalanceIn', 'extra': 'Extra', 'accrued': 'Accrued'}, payload, supplied)

    def add_overtime(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        activity_id: str | UUID | Unset = UNSET,
        multiplicator_definition_set_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddOvertime.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'activity_id': activity_id, 'multiplicator_definition_set_id': multiplicator_definition_set_id, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddOvertime', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'activity_id': 'ActivityId', 'multiplicator_definition_set_id': 'MultiplicatorDefinitionSetId', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def add_overtime_request(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        subject: str | Unset = UNSET,
        message: str | Unset = UNSET,
        overtime_type: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddOvertimeRequest.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'subject': subject, 'message': message, 'overtime_type': overtime_type}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddOvertimeRequest', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'subject': 'Subject', 'message': 'Message', 'overtime_type': 'OvertimeType'}, payload, supplied)

    def add_part_day_absence(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        absence_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
        convert_if_applicable_for_full_day: int | Unset = UNSET,
        attribute_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddPartDayAbsence.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'absence_id': absence_id, 'scenario_id': scenario_id, 'convert_if_applicable_for_full_day': convert_if_applicable_for_full_day, 'attribute_id': attribute_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddPartDayAbsence', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'absence_id': 'AbsenceId', 'scenario_id': 'ScenarioId', 'convert_if_applicable_for_full_day': 'ConvertIfApplicableForFullDay', 'attribute_id': 'AttributeId'}, payload, supplied)

    def add_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        first_name: str | None | Unset = UNSET,
        last_name: str | None | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        email: str | None | Unset = UNSET,
        employment_number: str | None | Unset = UNSET,
        application_logon: str | None | Unset = UNSET,
        identity: str | None | Unset = UNSET,
        team_id: str | UUID | None | Unset = UNSET,
        contract_id: str | UUID | None | Unset = UNSET,
        contract_schedule_id: str | UUID | None | Unset = UNSET,
        part_time_percentage_id: str | UUID | None | Unset = UNSET,
        role_ids: list[Any] | None | Unset = UNSET,
        workflow_control_set_id: str | UUID | None | Unset = UNSET,
        shift_bag_id: str | UUID | None | Unset = UNSET,
        budget_group_id: str | UUID | None | Unset = UNSET,
        first_day_of_week: int | None | Unset = UNSET,
        culture: str | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'first_name': first_name, 'last_name': last_name, 'start_date': start_date, 'email': email, 'employment_number': employment_number, 'application_logon': application_logon, 'identity': identity, 'team_id': team_id, 'contract_id': contract_id, 'contract_schedule_id': contract_schedule_id, 'part_time_percentage_id': part_time_percentage_id, 'role_ids': role_ids, 'workflow_control_set_id': workflow_control_set_id, 'shift_bag_id': shift_bag_id, 'budget_group_id': budget_group_id, 'first_day_of_week': first_day_of_week, 'culture': culture}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddPerson', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'first_name': 'FirstName', 'last_name': 'LastName', 'start_date': 'StartDate', 'email': 'Email', 'employment_number': 'EmploymentNumber', 'application_logon': 'ApplicationLogon', 'identity': 'Identity', 'team_id': 'TeamId', 'contract_id': 'ContractId', 'contract_schedule_id': 'ContractScheduleId', 'part_time_percentage_id': 'PartTimePercentageId', 'role_ids': 'RoleIds', 'workflow_control_set_id': 'WorkflowControlSetId', 'shift_bag_id': 'ShiftBagId', 'budget_group_id': 'BudgetGroupId', 'first_day_of_week': 'FirstDayOfWeek', 'culture': 'Culture'}, payload, supplied)

    def add_schedule_changes_listener(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        url: str | Unset = UNSET,
        name: str | Unset = UNSET,
        days_start_from_current_date: int | Unset = UNSET,
        days_end_from_current_date: int | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddScheduleChangesListener.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'url': url, 'name': name, 'days_start_from_current_date': days_start_from_current_date, 'days_end_from_current_date': days_end_from_current_date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddScheduleChangesListener', {'business_unit_id': 'BusinessUnitId', 'url': 'Url', 'name': 'Name', 'days_start_from_current_date': 'DaysStartFromCurrentDate', 'days_end_from_current_date': 'DaysEndFromCurrentDate'}, payload, supplied)

    def add_scheduled_heads_per_dp(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        time_zone: str | Unset = UNSET,
        dp_id: str | UUID | Unset = UNSET,
        interval_wise_scheduled_heads: list[Any] | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddScheduledHeadsPerDp.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'time_zone': time_zone, 'dp_id': dp_id, 'interval_wise_scheduled_heads': interval_wise_scheduled_heads}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddScheduledHeadsPerDp', {'business_unit_id': 'BusinessUnitId', 'time_zone': 'TimeZone', 'dp_id': 'DpId', 'interval_wise_scheduled_heads': 'IntervalWiseScheduledHeads'}, payload, supplied)

    def add_skills_to_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        skill_ids: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddSkillsToPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'start_date': start_date, 'skill_ids': skill_ids}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddSkillsToPerson', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'start_date': 'StartDate', 'skill_ids': 'SkillIds'}, payload, supplied)

    def add_team(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        team_name: str | Unset = UNSET,
        site_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/AddTeam.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'team_name': team_name, 'site_id': site_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/AddTeam', {'business_unit_id': 'BusinessUnitId', 'team_name': 'TeamName', 'site_id': 'SiteId'}, payload, supplied)

    def clear_leaving_date_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/ClearLeavingDateForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/ClearLeavingDateForPerson', {'person_id': 'PersonId'}, payload, supplied)

    def delete_account_for_person_account(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        date_from: str | date | Unset = UNSET,
        absence_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/DeleteAccountForPersonAccount.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'date_from': date_from, 'absence_id': absence_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/DeleteAccountForPersonAccount', {'person_id': 'PersonId', 'date_from': 'DateFrom', 'absence_id': 'AbsenceId'}, payload, supplied)

    def edit_meetings(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | None | Unset = UNSET,
        external_meetings: list[Any] | Unset = UNSET,
        handle_non_overwritable_activities: str | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/EditMeetings.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'external_meetings': external_meetings, 'handle_non_overwritable_activities': handle_non_overwritable_activities}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/EditMeetings', {'time_zone_id': 'TimeZoneId', 'external_meetings': 'ExternalMeetings', 'handle_non_overwritable_activities': 'HandleNonOverwritableActivities'}, payload, supplied)

    def import_backlog_queue(
        self,
        payload: dict[str, Any] | None = None,
        *,
        tasks: list[Any] | Unset = UNSET,
        upload_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/ImportBacklogQueue.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'tasks': tasks, 'upload_id': upload_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/ImportBacklogQueue', {'tasks': 'Tasks', 'upload_id': 'UploadId'}, payload, supplied)

    def process_backlog_queue(
        self,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        """Write operation: /command/ProcessBacklogQueue.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/ProcessBacklogQueue', {}, payload, supplied)

    def remove_full_day_absence(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/RemoveFullDayAbsence.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/RemoveFullDayAbsence', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def remove_meetings(
        self,
        payload: dict[str, Any] | None = None,
        *,
        external_meeting_ids: list[Any] | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/RemoveMeetings.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'external_meeting_ids': external_meeting_ids}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/RemoveMeetings', {'external_meeting_ids': 'ExternalMeetingIds'}, payload, supplied)

    def remove_overtime(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/RemoveOvertime.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/RemoveOvertime', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def remove_part_day_absence(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
        absence_ids: list[Any] | None | Unset = UNSET,
        attribute_ids: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/RemovePartDayAbsence.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'scenario_id': scenario_id, 'absence_ids': absence_ids, 'attribute_ids': attribute_ids}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/RemovePartDayAbsence', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'scenario_id': 'ScenarioId', 'absence_ids': 'AbsenceIds', 'attribute_ids': 'AttributeIds'}, payload, supplied)

    def remove_skills_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        skill_ids: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/RemoveSkillsForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'start_date': start_date, 'skill_ids': skill_ids}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/RemoveSkillsForPerson', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'start_date': 'StartDate', 'skill_ids': 'SkillIds'}, payload, supplied)

    def set_availability(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        availability_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetAvailability.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'availability_id': availability_id, 'start_date': start_date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetAvailability', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'availability_id': 'AvailabilityId', 'start_date': 'StartDate'}, payload, supplied)

    def set_budget_group_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        budget_group_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetBudgetGroupForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'start_date': start_date, 'person_id': person_id, 'budget_group_id': budget_group_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetBudgetGroupForPerson', {'business_unit_id': 'BusinessUnitId', 'start_date': 'StartDate', 'person_id': 'PersonId', 'budget_group_id': 'BudgetGroupId'}, payload, supplied)

    def set_details_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        first_name: str | None | Unset = UNSET,
        last_name: str | None | Unset = UNSET,
        email: str | None | Unset = UNSET,
        workflow_control_set_id: str | UUID | None | Unset = UNSET,
        note: str | None | Unset = UNSET,
        employment_number: str | None | Unset = UNSET,
        identity: str | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetDetailsForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'first_name': first_name, 'last_name': last_name, 'email': email, 'workflow_control_set_id': workflow_control_set_id, 'note': note, 'employment_number': employment_number, 'identity': identity}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetDetailsForPerson', {'person_id': 'PersonId', 'first_name': 'FirstName', 'last_name': 'LastName', 'email': 'Email', 'workflow_control_set_id': 'WorkflowControlSetId', 'note': 'Note', 'employment_number': 'EmploymentNumber', 'identity': 'Identity'}, payload, supplied)

    def set_employment_details_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        contract_id: str | UUID | None | Unset = UNSET,
        contract_schedule_id: str | UUID | None | Unset = UNSET,
        part_time_percentage_id: str | UUID | None | Unset = UNSET,
        team_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetEmploymentDetailsForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'start_date': start_date, 'person_id': person_id, 'contract_id': contract_id, 'contract_schedule_id': contract_schedule_id, 'part_time_percentage_id': part_time_percentage_id, 'team_id': team_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetEmploymentDetailsForPerson', {'business_unit_id': 'BusinessUnitId', 'start_date': 'StartDate', 'person_id': 'PersonId', 'contract_id': 'ContractId', 'contract_schedule_id': 'ContractScheduleId', 'part_time_percentage_id': 'PartTimePercentageId', 'team_id': 'TeamId'}, payload, supplied)

    def set_external_logons_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        external_logon_ids: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetExternalLogonsForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'date': date, 'external_logon_ids': external_logon_ids}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetExternalLogonsForPerson', {'person_id': 'PersonId', 'date': 'Date', 'external_logon_ids': 'ExternalLogonIds'}, payload, supplied)

    def set_forecast(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        skill_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
        days: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetForecast.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'skill_id': skill_id, 'scenario_id': scenario_id, 'days': days}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetForecast', {'business_unit_id': 'BusinessUnitId', 'skill_id': 'SkillId', 'scenario_id': 'ScenarioId', 'days': 'Days'}, payload, supplied)

    def set_forecast_daily(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        skill_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
        days: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetForecastDaily.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'skill_id': skill_id, 'scenario_id': scenario_id, 'days': days}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetForecastDaily', {'business_unit_id': 'BusinessUnitId', 'skill_id': 'SkillId', 'scenario_id': 'ScenarioId', 'days': 'Days'}, payload, supplied)

    def set_leaving_date_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetLeavingDateForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'date': date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetLeavingDateForPerson', {'person_id': 'PersonId', 'date': 'Date'}, payload, supplied)

    def set_location(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_ids: list[Any] | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        location: str | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetLocation.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_ids': person_ids, 'period': period, 'location': location}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetLocation', {'business_unit_id': 'BusinessUnitId', 'person_ids': 'PersonIds', 'period': 'Period', 'location': 'Location'}, payload, supplied)

    def set_note_for_schedule_day(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
        note: str | Unset = UNSET,
        is_public: bool | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetNoteForScheduleDay.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'scenario_id': scenario_id, 'person_id': person_id, 'date': date, 'note': note, 'is_public': is_public}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetNoteForScheduleDay', {'business_unit_id': 'BusinessUnitId', 'scenario_id': 'ScenarioId', 'person_id': 'PersonId', 'date': 'Date', 'note': 'Note', 'is_public': 'IsPublic'}, payload, supplied)

    def set_optional_column_for_people(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_ids: list[Any] | Unset = UNSET,
        optional_column_id: str | UUID | Unset = UNSET,
        value: str | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetOptionalColumnForPeople.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_ids': person_ids, 'optional_column_id': optional_column_id, 'value': value}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetOptionalColumnForPeople', {'person_ids': 'PersonIds', 'optional_column_id': 'OptionalColumnId', 'value': 'Value'}, payload, supplied)

    def set_optional_column_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        optional_column_id: str | UUID | Unset = UNSET,
        value: str | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetOptionalColumnForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'optional_column_id': optional_column_id, 'value': value}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetOptionalColumnForPerson', {'person_id': 'PersonId', 'optional_column_id': 'OptionalColumnId', 'value': 'Value'}, payload, supplied)

    def set_roles_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        role_ids: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetRolesForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'role_ids': role_ids}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetRolesForPerson', {'person_id': 'PersonId', 'role_ids': 'RoleIds'}, payload, supplied)

    def set_rotation(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        rotation_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        start_week: int | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetRotation.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'rotation_id': rotation_id, 'start_date': start_date, 'start_week': start_week}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetRotation', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'rotation_id': 'RotationId', 'start_date': 'StartDate', 'start_week': 'StartWeek'}, payload, supplied)

    def set_schedules_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        time_zone_id: str | Unset = UNSET,
        business_unit_id: str | UUID | Unset = UNSET,
        date_period: dict[str, Any] | Unset = UNSET,
        schedule_days: list[Any] | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetSchedulesForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'time_zone_id': time_zone_id, 'business_unit_id': business_unit_id, 'date_period': date_period, 'schedule_days': schedule_days, 'person_id': person_id, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetSchedulesForPerson', {'time_zone_id': 'TimeZoneId', 'business_unit_id': 'BusinessUnitId', 'date_period': 'DatePeriod', 'schedule_days': 'ScheduleDays', 'person_id': 'PersonId', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def set_shift_bag_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        shift_bag_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetShiftBagForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'start_date': start_date, 'person_id': person_id, 'shift_bag_id': shift_bag_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetShiftBagForPerson', {'business_unit_id': 'BusinessUnitId', 'start_date': 'StartDate', 'person_id': 'PersonId', 'shift_bag_id': 'ShiftBagId'}, payload, supplied)

    def set_shrinkage(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        skill_id: str | UUID | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
        days: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetShrinkage.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'skill_id': skill_id, 'scenario_id': scenario_id, 'days': days}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetShrinkage', {'business_unit_id': 'BusinessUnitId', 'skill_id': 'SkillId', 'scenario_id': 'ScenarioId', 'days': 'Days'}, payload, supplied)

    def set_skills_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        skill_ids: list[Any] | None | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetSkillsForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'start_date': start_date, 'skill_ids': skill_ids}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetSkillsForPerson', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'start_date': 'StartDate', 'skill_ids': 'SkillIds'}, payload, supplied)

    def set_team_for_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        start_date: str | date | None | Unset = UNSET,
        team_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Write operation: /command/SetTeamForPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'start_date': start_date, 'team_id': team_id, 'person_id': person_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/command/SetTeamForPerson', {'business_unit_id': 'BusinessUnitId', 'start_date': 'StartDate', 'team_id': 'TeamId', 'person_id': 'PersonId'}, payload, supplied)

    def all_absences(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        filter: int | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Absence/AllAbsences.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'filter': filter}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Absence/AllAbsences', {'business_unit_id': 'BusinessUnitId', 'filter': 'Filter'}, payload, supplied)

    def get_absence_attribute(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/AbsenceAttribute/GetAbsenceAttribute.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/AbsenceAttribute/GetAbsenceAttribute', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def get_all_absence_attribute(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/AbsenceAttribute/GetAllAbsenceAttribute.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/AbsenceAttribute/GetAllAbsenceAttribute', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def absence_possibility_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/AbsencePossibility/AbsencePossibilityByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/AbsencePossibility/AbsencePossibilityByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period'}, payload, supplied)

    def absence_request_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        request_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/AbsenceRequest/AbsenceRequestById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'request_id': request_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/AbsenceRequest/AbsenceRequestById', {'business_unit_id': 'BusinessUnitId', 'request_id': 'RequestId'}, payload, supplied)

    def absence_request_rules_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/AbsenceRequestRule/AbsenceRequestRulesByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/AbsenceRequestRule/AbsenceRequestRulesByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period'}, payload, supplied)

    def activities_available_for_request_by_person_and_date(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Activity/ActivitiesAvailableForRequestByPersonAndDate.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'date': date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Activity/ActivitiesAvailableForRequestByPersonAndDate', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'date': 'Date'}, payload, supplied)

    def all_activities(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        filter: int | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Activity/AllActivities.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'filter': filter}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Activity/AllActivities', {'business_unit_id': 'BusinessUnitId', 'filter': 'Filter'}, payload, supplied)

    def activity_request_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        request_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ActivityRequest/ActivityRequestById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'request_id': request_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ActivityRequest/ActivityRequestById', {'business_unit_id': 'BusinessUnitId', 'request_id': 'RequestId'}, payload, supplied)

    def permission_by_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ApplicationFunction/PermissionByPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ApplicationFunction/PermissionByPerson', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId'}, payload, supplied)

    def all_availabilities(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Availability/AllAvailabilities.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Availability/AllAvailabilities', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_budget_groups(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/BudgetGroup/AllBudgetGroups.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/BudgetGroup/AllBudgetGroups', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_business_units(
        self,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        """Read operation: /query/BusinessUnit/AllBusinessUnits.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/BusinessUnit/AllBusinessUnits', {}, payload, supplied)

    def all_contracts(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Contract/AllContracts.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Contract/AllContracts', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_contract_schedules(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ContractSchedule/AllContractSchedules.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ContractSchedule/AllContractSchedules', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_day_off_templates(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/DayOffTemplate/AllDayOffTemplates.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/DayOffTemplate/AllDayOffTemplates', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def get_employee_defaults(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/EmployeeDefaults/GetEmployeeDefaults.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/EmployeeDefaults/GetEmployeeDefaults', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def external_logon_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ExternalLogon/ExternalLogonById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'id': id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ExternalLogon/ExternalLogonById', {'id': 'Id'}, payload, supplied)

    def external_logons_by_data_source(
        self,
        payload: dict[str, Any] | None = None,
        *,
        data_source_id: int | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ExternalLogon/ExternalLogonsByDataSource.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'data_source_id': data_source_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ExternalLogon/ExternalLogonsByDataSource', {'data_source_id': 'DataSourceId'}, payload, supplied)

    def external_logons_by_person(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ExternalLogon/ExternalLogonsByPerson.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'date': date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ExternalLogon/ExternalLogonsByPerson', {'person_id': 'PersonId', 'date': 'Date'}, payload, supplied)

    def forecast_by_skill(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        skill_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        apply_shrinkage: bool | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Forecast/ForecastBySkill.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'skill_id': skill_id, 'period': period, 'apply_shrinkage': apply_shrinkage, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Forecast/ForecastBySkill', {'business_unit_id': 'BusinessUnitId', 'skill_id': 'SkillId', 'period': 'Period', 'apply_shrinkage': 'ApplyShrinkage', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def locations_by_person_ids(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_ids: list[Any] | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Location/LocationsByPersonIds.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_ids': person_ids, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Location/LocationsByPersonIds', {'business_unit_id': 'BusinessUnitId', 'person_ids': 'PersonIds', 'period': 'Period'}, payload, supplied)

    def all_multiplicator_definition_sets(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/MultiplicatorDefinitionSet/AllMultiplicatorDefinitionSets.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/MultiplicatorDefinitionSet/AllMultiplicatorDefinitionSets', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def nightly_rest_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/NightlyRest/NightlyRestByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'date': date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/NightlyRest/NightlyRestByPersonId', {'person_id': 'PersonId', 'date': 'Date'}, payload, supplied)

    def all_optional_columns(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/OptionalColumn/AllOptionalColumns.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/OptionalColumn/AllOptionalColumns', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def overtime_possibility_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/OvertimePossibility/OvertimePossibilityByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/OvertimePossibility/OvertimePossibilityByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period'}, payload, supplied)

    def overtime_request_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        request_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/OvertimeRequest/OvertimeRequestById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'request_id': request_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/OvertimeRequest/OvertimeRequestById', {'business_unit_id': 'BusinessUnitId', 'request_id': 'RequestId'}, payload, supplied)

    def overtime_request_configuration_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/OvertimeRequestConfiguration/OvertimeRequestConfigurationByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'date': date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/OvertimeRequestConfiguration/OvertimeRequestConfigurationByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'date': 'Date'}, payload, supplied)

    def overtime_valid_possibility_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/OvertimeValidPossibility/OvertimeValidPossibilityByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/OvertimeValidPossibility/OvertimeValidPossibilityByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period'}, payload, supplied)

    def all_part_time_percentages(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/PartTimePercentage/AllPartTimePercentages.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/PartTimePercentage/AllPartTimePercentages', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def people_by_business_unit_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        page: int | Unset = UNSET,
        page_size: int | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PeopleByBusinessUnitId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'date': date, 'page': page, 'page_size': page_size, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PeopleByBusinessUnitId', {'business_unit_id': 'BusinessUnitId', 'date': 'Date', 'page': 'Page', 'page_size': 'PageSize', 'include': 'Include'}, payload, supplied)

    def people_by_employment_numbers(
        self,
        payload: dict[str, Any] | None = None,
        *,
        employment_numbers: list[Any] | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PeopleByEmploymentNumbers.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'employment_numbers': employment_numbers, 'date': date, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PeopleByEmploymentNumbers', {'employment_numbers': 'EmploymentNumbers', 'date': 'Date', 'include': 'Include'}, payload, supplied)

    def people_by_group_page_group(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        group_page_group_id: str | UUID | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PeopleByGroupPageGroup.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'group_page_group_id': group_page_group_id, 'date': date, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PeopleByGroupPageGroup', {'business_unit_id': 'BusinessUnitId', 'group_page_group_id': 'GroupPageGroupId', 'date': 'Date', 'include': 'Include'}, payload, supplied)

    def people_by_identities(
        self,
        payload: dict[str, Any] | None = None,
        *,
        identities: list[Any] | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PeopleByIdentities.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'identities': identities, 'date': date, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PeopleByIdentities', {'identities': 'Identities', 'date': 'Date', 'include': 'Include'}, payload, supplied)

    def people_by_ids(
        self,
        payload: dict[str, Any] | None = None,
        *,
        ids: list[Any] | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PeopleByIds.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'ids': ids, 'date': date, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PeopleByIds', {'ids': 'Ids', 'date': 'Date', 'include': 'Include'}, payload, supplied)

    def people_by_skill_group(
        self,
        payload: dict[str, Any] | None = None,
        *,
        skill_group_id: str | UUID | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PeopleBySkillGroup.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'skill_group_id': skill_group_id, 'date': date, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PeopleBySkillGroup', {'skill_group_id': 'SkillGroupId', 'date': 'Date', 'include': 'Include'}, payload, supplied)

    def people_by_team_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        team_id: str | UUID | None | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PeopleByTeamId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'team_id': team_id, 'date': date, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PeopleByTeamId', {'team_id': 'TeamId', 'date': 'Date', 'include': 'Include'}, payload, supplied)

    def person_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | None | Unset = UNSET,
        include: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Person/PersonById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'date': date, 'include': include}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Person/PersonById', {'person_id': 'PersonId', 'date': 'Date', 'include': 'Include'}, payload, supplied)

    def person_accounts_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/PersonAccount/PersonAccountsByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'date': date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/PersonAccount/PersonAccountsByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'date': 'Date'}, payload, supplied)

    def all_roles(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        get_application_functions_and_available_data: bool | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Role/AllRoles.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'get_application_functions_and_available_data': get_application_functions_and_available_data}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Role/AllRoles', {'business_unit_id': 'BusinessUnitId', 'get_application_functions_and_available_data': 'GetApplicationFunctionsAndAvailableData'}, payload, supplied)

    def all_rotations(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        include_details: bool | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Rotation/AllRotations.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'include_details': include_details}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Rotation/AllRotations', {'business_unit_id': 'BusinessUnitId', 'include_details': 'IncludeDetails'}, payload, supplied)

    def rotation_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        rotation_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Rotation/RotationById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'rotation_id': rotation_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Rotation/RotationById', {'rotation_id': 'RotationId'}, payload, supplied)

    def all_scenarios(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Scenario/AllScenarios.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Scenario/AllScenarios', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def schedule_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Schedule/ScheduleByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Schedule/ScheduleByPersonId', {'person_id': 'PersonId', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def schedule_by_person_ids(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_ids: list[Any] | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Schedule/ScheduleByPersonIds.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_ids': person_ids, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Schedule/ScheduleByPersonIds', {'person_ids': 'PersonIds', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def schedule_by_team_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        team_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Schedule/ScheduleByTeamId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'team_id': team_id, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Schedule/ScheduleByTeamId', {'business_unit_id': 'BusinessUnitId', 'team_id': 'TeamId', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def schedule_absences_by_person_ids(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_ids: list[Any] | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ScheduleAbsence/ScheduleAbsencesByPersonIds.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_ids': person_ids, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ScheduleAbsence/ScheduleAbsencesByPersonIds', {'person_ids': 'PersonIds', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def schedule_audit_trail_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ScheduleAuditTrail/ScheduleAuditTrailByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id, 'date': date, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ScheduleAuditTrail/ScheduleAuditTrailByPersonId', {'person_id': 'PersonId', 'date': 'Date', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def schedules_by_change_date(
        self,
        payload: dict[str, Any] | None = None,
        *,
        changes_from: str | datetime | Unset = UNSET,
        changes_to: str | datetime | None | Unset = UNSET,
        page: int | Unset = UNSET,
        page_size: int | Unset = UNSET,
        business_unit_id: str | UUID | None | Unset = UNSET,
        period: dict[str, Any] | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ScheduleChanges/SchedulesByChangeDate.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'changes_from': changes_from, 'changes_to': changes_to, 'page': page, 'page_size': page_size, 'business_unit_id': business_unit_id, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ScheduleChanges/SchedulesByChangeDate', {'changes_from': 'ChangesFrom', 'changes_to': 'ChangesTo', 'page': 'Page', 'page_size': 'PageSize', 'business_unit_id': 'BusinessUnitId', 'period': 'Period'}, payload, supplied)

    def all_schedule_changes_listener_subscription(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ScheduleChangesListenerSubscription/AllScheduleChangesListenerSubscription.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ScheduleChangesListenerSubscription/AllScheduleChangesListenerSubscription', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def schedule_by_group_page_groups(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        group_page_group_ids: list[Any] | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ScheduleOrder/ScheduleByGroupPageGroups.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'group_page_group_ids': group_page_group_ids, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ScheduleOrder/ScheduleByGroupPageGroups', {'business_unit_id': 'BusinessUnitId', 'group_page_group_ids': 'GroupPageGroupIds', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def all_shift_bags(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ShiftBag/AllShiftBags.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ShiftBag/AllShiftBags', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_shift_categories(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/ShiftCategory/AllShiftCategories.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/ShiftCategory/AllShiftCategories', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_sites(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Site/AllSites.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Site/AllSites', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_skills(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Skill/AllSkills.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Skill/AllSkills', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_skill_groups(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/SkillGroup/AllSkillGroups.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/SkillGroup/AllSkillGroups', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def staffing_by_skills(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        skill_ids: list[Any] | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Staffing/StaffingBySkills.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'skill_ids': skill_ids, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Staffing/StaffingBySkills', {'business_unit_id': 'BusinessUnitId', 'skill_ids': 'SkillIds', 'period': 'Period'}, payload, supplied)

    def all_teams(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Team/AllTeams.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Team/AllTeams', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)

    def all_teams_with_agents(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Team/AllTeamsWithAgents.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'period': period}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Team/AllTeamsWithAgents', {'business_unit_id': 'BusinessUnitId', 'period': 'Period'}, payload, supplied)

    def team_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Team/TeamById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'id': id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Team/TeamById', {'business_unit_id': 'BusinessUnitId', 'id': 'Id'}, payload, supplied)

    def teams_by_site_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        site_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/Team/TeamsBySiteId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'site_id': site_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/Team/TeamsBySiteId', {'business_unit_id': 'BusinessUnitId', 'site_id': 'SiteId'}, payload, supplied)

    def user_by_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        person_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/User/UserById.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'person_id': person_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/User/UserById', {'person_id': 'PersonId'}, payload, supplied)

    def weekly_max_work_time_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        date: str | date | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/WeeklyMaxWorkTime/WeeklyMaxWorkTimeByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'date': date}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/WeeklyMaxWorkTime/WeeklyMaxWorkTimeByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'date': 'Date'}, payload, supplied)

    def workload_by_skill_ids(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        skill_ids: list[Any] | None | Unset = UNSET,
        page: int | Unset = UNSET,
        page_size: int | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/WorkLoad/WorkloadBySkillIds.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'skill_ids': skill_ids, 'page': page, 'page_size': page_size}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/WorkLoad/WorkloadBySkillIds', {'business_unit_id': 'BusinessUnitId', 'skill_ids': 'SkillIds', 'page': 'Page', 'page_size': 'PageSize'}, payload, supplied)

    def work_time_by_person_id(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
        person_id: str | UUID | Unset = UNSET,
        period: dict[str, Any] | Unset = UNSET,
        scenario_id: str | UUID | None | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/WorkTime/WorkTimeByPersonId.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id, 'person_id': person_id, 'period': period, 'scenario_id': scenario_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/WorkTime/WorkTimeByPersonId', {'business_unit_id': 'BusinessUnitId', 'person_id': 'PersonId', 'period': 'Period', 'scenario_id': 'ScenarioId'}, payload, supplied)

    def all_workflow_control_sets(
        self,
        payload: dict[str, Any] | None = None,
        *,
        business_unit_id: str | UUID | Unset = UNSET,
    ) -> Any:
        """Read operation: /query/WorkflowControlSet/AllWorkflowControlSets.

        Named fields use snake_case, including nested dictionaries.
        Omitted values are not sent; explicit None sends null.
        Returns the server JSON response unchanged.
        """
        values: dict[str, Any] = {'business_unit_id': business_unit_id}
        supplied = {key: value for key, value in values.items() if value is not UNSET}
        return self._operation('/query/WorkflowControlSet/AllWorkflowControlSets', {'business_unit_id': 'BusinessUnitId'}, payload, supplied)
