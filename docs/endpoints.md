# WFM method reference

All 111 operations in the reviewed public schema use named Python arguments.
Use `client.method(field=value)`; autocomplete/help shows every field and type.
Nested dictionaries accept snake_case or original API field names. Omitted values
are not sent; `None` sends JSON null. UNSET is internal: do not pass it yourself.
Required fields below come from the schema; complete server validation still applies.
A raw API dictionary remains available as `payload={...}` (or the first positional argument).
Raw payloads are passed unchanged; do not mix them with named fields.

Responses preserve the server JSON/envelope. Commands change data and are never retried.

## Methods

| Method | Endpoint | Kind |
| --- | --- | --- |
| [add_activity_request](#add-activity-request) | `/command/AddActivityRequest` | Write |
| [add_actual_heads_per_dp](#add-actual-heads-per-dp) | `/command/AddActualHeadsPerDp` | Write |
| [add_actual_per_dp_workload](#add-actual-per-dp-workload) | `/command/AddActualPerDpWorkload` | Write |
| [add_full_day_absence](#add-full-day-absence) | `/command/AddFullDayAbsence` | Write |
| [add_full_day_absence_request](#add-full-day-absence-request) | `/command/AddFullDayAbsenceRequest` | Write |
| [add_intraday_absence_request](#add-intraday-absence-request) | `/command/AddIntradayAbsenceRequest` | Write |
| [add_meetings](#add-meetings) | `/command/AddMeetings` | Write |
| [add_or_update_person_account_for_person](#add-or-update-person-account-for-person) | `/command/AddOrUpdatePersonAccountForPerson` | Write |
| [add_overtime](#add-overtime) | `/command/AddOvertime` | Write |
| [add_overtime_request](#add-overtime-request) | `/command/AddOvertimeRequest` | Write |
| [add_part_day_absence](#add-part-day-absence) | `/command/AddPartDayAbsence` | Write |
| [add_person](#add-person) | `/command/AddPerson` | Write |
| [add_schedule_changes_listener](#add-schedule-changes-listener) | `/command/AddScheduleChangesListener` | Write |
| [add_scheduled_heads_per_dp](#add-scheduled-heads-per-dp) | `/command/AddScheduledHeadsPerDp` | Write |
| [add_skills_to_person](#add-skills-to-person) | `/command/AddSkillsToPerson` | Write |
| [add_team](#add-team) | `/command/AddTeam` | Write |
| [clear_leaving_date_for_person](#clear-leaving-date-for-person) | `/command/ClearLeavingDateForPerson` | Write |
| [delete_account_for_person_account](#delete-account-for-person-account) | `/command/DeleteAccountForPersonAccount` | Write |
| [edit_meetings](#edit-meetings) | `/command/EditMeetings` | Write |
| [import_backlog_queue](#import-backlog-queue) | `/command/ImportBacklogQueue` | Write |
| [process_backlog_queue](#process-backlog-queue) | `/command/ProcessBacklogQueue` | Write |
| [remove_full_day_absence](#remove-full-day-absence) | `/command/RemoveFullDayAbsence` | Write |
| [remove_meetings](#remove-meetings) | `/command/RemoveMeetings` | Write |
| [remove_overtime](#remove-overtime) | `/command/RemoveOvertime` | Write |
| [remove_part_day_absence](#remove-part-day-absence) | `/command/RemovePartDayAbsence` | Write |
| [remove_skills_for_person](#remove-skills-for-person) | `/command/RemoveSkillsForPerson` | Write |
| [set_availability](#set-availability) | `/command/SetAvailability` | Write |
| [set_budget_group_for_person](#set-budget-group-for-person) | `/command/SetBudgetGroupForPerson` | Write |
| [set_details_for_person](#set-details-for-person) | `/command/SetDetailsForPerson` | Write |
| [set_employment_details_for_person](#set-employment-details-for-person) | `/command/SetEmploymentDetailsForPerson` | Write |
| [set_external_logons_for_person](#set-external-logons-for-person) | `/command/SetExternalLogonsForPerson` | Write |
| [set_forecast](#set-forecast) | `/command/SetForecast` | Write |
| [set_forecast_daily](#set-forecast-daily) | `/command/SetForecastDaily` | Write |
| [set_leaving_date_for_person](#set-leaving-date-for-person) | `/command/SetLeavingDateForPerson` | Write |
| [set_location](#set-location) | `/command/SetLocation` | Write |
| [set_note_for_schedule_day](#set-note-for-schedule-day) | `/command/SetNoteForScheduleDay` | Write |
| [set_optional_column_for_people](#set-optional-column-for-people) | `/command/SetOptionalColumnForPeople` | Write |
| [set_optional_column_for_person](#set-optional-column-for-person) | `/command/SetOptionalColumnForPerson` | Write |
| [set_roles_for_person](#set-roles-for-person) | `/command/SetRolesForPerson` | Write |
| [set_rotation](#set-rotation) | `/command/SetRotation` | Write |
| [set_schedules_for_person](#set-schedules-for-person) | `/command/SetSchedulesForPerson` | Write |
| [set_shift_bag_for_person](#set-shift-bag-for-person) | `/command/SetShiftBagForPerson` | Write |
| [set_shrinkage](#set-shrinkage) | `/command/SetShrinkage` | Write |
| [set_skills_for_person](#set-skills-for-person) | `/command/SetSkillsForPerson` | Write |
| [set_team_for_person](#set-team-for-person) | `/command/SetTeamForPerson` | Write |
| [all_absences](#all-absences) | `/query/Absence/AllAbsences` | Read |
| [get_absence_attribute](#get-absence-attribute) | `/query/AbsenceAttribute/GetAbsenceAttribute` | Read |
| [get_all_absence_attribute](#get-all-absence-attribute) | `/query/AbsenceAttribute/GetAllAbsenceAttribute` | Read |
| [absence_possibility_by_person_id](#absence-possibility-by-person-id) | `/query/AbsencePossibility/AbsencePossibilityByPersonId` | Read |
| [absence_request_by_id](#absence-request-by-id) | `/query/AbsenceRequest/AbsenceRequestById` | Read |
| [absence_request_rules_by_person_id](#absence-request-rules-by-person-id) | `/query/AbsenceRequestRule/AbsenceRequestRulesByPersonId` | Read |
| [activities_available_for_request_by_person_and_date](#activities-available-for-request-by-person-and-date) | `/query/Activity/ActivitiesAvailableForRequestByPersonAndDate` | Read |
| [all_activities](#all-activities) | `/query/Activity/AllActivities` | Read |
| [activity_request_by_id](#activity-request-by-id) | `/query/ActivityRequest/ActivityRequestById` | Read |
| [permission_by_person](#permission-by-person) | `/query/ApplicationFunction/PermissionByPerson` | Read |
| [all_availabilities](#all-availabilities) | `/query/Availability/AllAvailabilities` | Read |
| [all_budget_groups](#all-budget-groups) | `/query/BudgetGroup/AllBudgetGroups` | Read |
| [all_business_units](#all-business-units) | `/query/BusinessUnit/AllBusinessUnits` | Read |
| [all_contracts](#all-contracts) | `/query/Contract/AllContracts` | Read |
| [all_contract_schedules](#all-contract-schedules) | `/query/ContractSchedule/AllContractSchedules` | Read |
| [all_day_off_templates](#all-day-off-templates) | `/query/DayOffTemplate/AllDayOffTemplates` | Read |
| [get_employee_defaults](#get-employee-defaults) | `/query/EmployeeDefaults/GetEmployeeDefaults` | Read |
| [external_logon_by_id](#external-logon-by-id) | `/query/ExternalLogon/ExternalLogonById` | Read |
| [external_logons_by_data_source](#external-logons-by-data-source) | `/query/ExternalLogon/ExternalLogonsByDataSource` | Read |
| [external_logons_by_person](#external-logons-by-person) | `/query/ExternalLogon/ExternalLogonsByPerson` | Read |
| [forecast_by_skill](#forecast-by-skill) | `/query/Forecast/ForecastBySkill` | Read |
| [locations_by_person_ids](#locations-by-person-ids) | `/query/Location/LocationsByPersonIds` | Read |
| [all_multiplicator_definition_sets](#all-multiplicator-definition-sets) | `/query/MultiplicatorDefinitionSet/AllMultiplicatorDefinitionSets` | Read |
| [nightly_rest_by_person_id](#nightly-rest-by-person-id) | `/query/NightlyRest/NightlyRestByPersonId` | Read |
| [all_optional_columns](#all-optional-columns) | `/query/OptionalColumn/AllOptionalColumns` | Read |
| [overtime_possibility_by_person_id](#overtime-possibility-by-person-id) | `/query/OvertimePossibility/OvertimePossibilityByPersonId` | Read |
| [overtime_request_by_id](#overtime-request-by-id) | `/query/OvertimeRequest/OvertimeRequestById` | Read |
| [overtime_request_configuration_by_person_id](#overtime-request-configuration-by-person-id) | `/query/OvertimeRequestConfiguration/OvertimeRequestConfigurationByPersonId` | Read |
| [overtime_valid_possibility_by_person_id](#overtime-valid-possibility-by-person-id) | `/query/OvertimeValidPossibility/OvertimeValidPossibilityByPersonId` | Read |
| [all_part_time_percentages](#all-part-time-percentages) | `/query/PartTimePercentage/AllPartTimePercentages` | Read |
| [people_by_business_unit_id](#people-by-business-unit-id) | `/query/Person/PeopleByBusinessUnitId` | Read |
| [people_by_employment_numbers](#people-by-employment-numbers) | `/query/Person/PeopleByEmploymentNumbers` | Read |
| [people_by_group_page_group](#people-by-group-page-group) | `/query/Person/PeopleByGroupPageGroup` | Read |
| [people_by_identities](#people-by-identities) | `/query/Person/PeopleByIdentities` | Read |
| [people_by_ids](#people-by-ids) | `/query/Person/PeopleByIds` | Read |
| [people_by_skill_group](#people-by-skill-group) | `/query/Person/PeopleBySkillGroup` | Read |
| [people_by_team_id](#people-by-team-id) | `/query/Person/PeopleByTeamId` | Read |
| [person_by_id](#person-by-id) | `/query/Person/PersonById` | Read |
| [person_accounts_by_person_id](#person-accounts-by-person-id) | `/query/PersonAccount/PersonAccountsByPersonId` | Read |
| [all_roles](#all-roles) | `/query/Role/AllRoles` | Read |
| [all_rotations](#all-rotations) | `/query/Rotation/AllRotations` | Read |
| [rotation_by_id](#rotation-by-id) | `/query/Rotation/RotationById` | Read |
| [all_scenarios](#all-scenarios) | `/query/Scenario/AllScenarios` | Read |
| [schedule_by_person_id](#schedule-by-person-id) | `/query/Schedule/ScheduleByPersonId` | Read |
| [schedule_by_person_ids](#schedule-by-person-ids) | `/query/Schedule/ScheduleByPersonIds` | Read |
| [schedule_by_team_id](#schedule-by-team-id) | `/query/Schedule/ScheduleByTeamId` | Read |
| [schedule_absences_by_person_ids](#schedule-absences-by-person-ids) | `/query/ScheduleAbsence/ScheduleAbsencesByPersonIds` | Read |
| [schedule_audit_trail_by_person_id](#schedule-audit-trail-by-person-id) | `/query/ScheduleAuditTrail/ScheduleAuditTrailByPersonId` | Read |
| [schedules_by_change_date](#schedules-by-change-date) | `/query/ScheduleChanges/SchedulesByChangeDate` | Read |
| [all_schedule_changes_listener_subscription](#all-schedule-changes-listener-subscription) | `/query/ScheduleChangesListenerSubscription/AllScheduleChangesListenerSubscription` | Read |
| [schedule_by_group_page_groups](#schedule-by-group-page-groups) | `/query/ScheduleOrder/ScheduleByGroupPageGroups` | Read |
| [all_shift_bags](#all-shift-bags) | `/query/ShiftBag/AllShiftBags` | Read |
| [all_shift_categories](#all-shift-categories) | `/query/ShiftCategory/AllShiftCategories` | Read |
| [all_sites](#all-sites) | `/query/Site/AllSites` | Read |
| [all_skills](#all-skills) | `/query/Skill/AllSkills` | Read |
| [all_skill_groups](#all-skill-groups) | `/query/SkillGroup/AllSkillGroups` | Read |
| [staffing_by_skills](#staffing-by-skills) | `/query/Staffing/StaffingBySkills` | Read |
| [all_teams](#all-teams) | `/query/Team/AllTeams` | Read |
| [all_teams_with_agents](#all-teams-with-agents) | `/query/Team/AllTeamsWithAgents` | Read |
| [team_by_id](#team-by-id) | `/query/Team/TeamById` | Read |
| [teams_by_site_id](#teams-by-site-id) | `/query/Team/TeamsBySiteId` | Read |
| [user_by_id](#user-by-id) | `/query/User/UserById` | Read |
| [weekly_max_work_time_by_person_id](#weekly-max-work-time-by-person-id) | `/query/WeeklyMaxWorkTime/WeeklyMaxWorkTimeByPersonId` | Read |
| [workload_by_skill_ids](#workload-by-skill-ids) | `/query/WorkLoad/WorkloadBySkillIds` | Read |
| [work_time_by_person_id](#work-time-by-person-id) | `/query/WorkTime/WorkTimeByPersonId` | Read |
| [all_workflow_control_sets](#all-workflow-control-sets) | `/query/WorkflowControlSet/AllWorkflowControlSets` | Read |

## add activity request

`/command/AddActivityRequest`

```python
client.add_activity_request(time_zone_id=..., business_unit_id=..., person_id=..., activity_id=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `activity_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## add actual heads per dp

`/command/AddActualHeadsPerDp`

```python
client.add_actual_heads_per_dp(time_zone=..., dp_id=..., interval_wise_actual_heads=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone` | `str` | Yes |
| `dp_id` | `str / UUID` | Yes |
| `interval_wise_actual_heads` | `list[Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `interval_wise_actual_heads[].start_date_time` | `str / datetime` | Yes |
| `interval_wise_actual_heads[].actual_staff_heads` | `float` | Yes |

## add actual per dp workload

`/command/AddActualPerDpWorkload`

```python
client.add_actual_per_dp_workload(time_zone=..., dp_id=..., workload_id=..., interval_wise_actual=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone` | `str` | Yes |
| `dp_id` | `str / UUID` | Yes |
| `workload_id` | `str / UUID` | Yes |
| `interval_wise_actual` | `list[Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `interval_wise_actual[].start_date_time` | `str / datetime` | Yes |
| `interval_wise_actual[].actual_volume` | `float / None` | No |
| `interval_wise_actual[].actual_aht` | `float / None` | No |
| `interval_wise_actual[].busy_hours` | `float / None` | No |

## add full day absence

`/command/AddFullDayAbsence`

```python
client.add_full_day_absence(business_unit_id=..., person_id=..., period=..., date=..., absence_id=..., attribute_id=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any] / None` | No |
| `date` | `str / date / None` | No |
| `absence_id` | `str / UUID` | Yes |
| `attribute_id` | `str / UUID / None` | No |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## add full day absence request

`/command/AddFullDayAbsenceRequest`

```python
client.add_full_day_absence_request(business_unit_id=..., person_id=..., absence_id=..., period=..., subject=..., message=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `absence_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `subject` | `str` | Yes |
| `message` | `str` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## add intraday absence request

`/command/AddIntradayAbsenceRequest`

```python
client.add_intraday_absence_request(time_zone_id=..., business_unit_id=..., person_id=..., absence_id=..., period=..., subject=..., message=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `absence_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `subject` | `str` | Yes |
| `message` | `str` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## add meetings

`/command/AddMeetings`

```python
client.add_meetings(time_zone_id=..., business_unit_id=..., scenario_id=..., external_meetings=..., handle_non_overwritable_activities=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `scenario_id` | `str / UUID / None` | No |
| `external_meetings` | `list[Any]` | Yes |
| `handle_non_overwritable_activities` | `str / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `external_meetings[].external_meeting_id` | `str` | Yes |
| `external_meetings[].period` | `dict[str, Any]` | Yes |
| `external_meetings[].period.start_time` | `str / datetime` | No |
| `external_meetings[].period.end_time` | `str / datetime` | No |
| `external_meetings[].participants` | `list[Any]` | Yes |
| `external_meetings[].activity_id` | `str / UUID` | Yes |
| `external_meetings[].title` | `str / None` | No |
| `external_meetings[].location` | `str / None` | No |
| `external_meetings[].agenda` | `str / None` | No |

## add or update person account for person

`/command/AddOrUpdatePersonAccountForPerson`

```python
client.add_or_update_person_account_for_person(person_id=..., absence_id=..., date_from=..., balance_in=..., extra=..., accrued=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `absence_id` | `str / UUID` | Yes |
| `date_from` | `str / date` | Yes |
| `balance_in` | `int` | No |
| `extra` | `int` | No |
| `accrued` | `int` | No |

## add overtime

`/command/AddOvertime`

```python
client.add_overtime(time_zone_id=..., business_unit_id=..., person_id=..., period=..., activity_id=..., multiplicator_definition_set_id=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `activity_id` | `str / UUID` | Yes |
| `multiplicator_definition_set_id` | `str / UUID` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## add overtime request

`/command/AddOvertimeRequest`

```python
client.add_overtime_request(time_zone_id=..., business_unit_id=..., person_id=..., period=..., subject=..., message=..., overtime_type=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `subject` | `str` | Yes |
| `message` | `str` | Yes |
| `overtime_type` | `str / UUID` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## add part day absence

`/command/AddPartDayAbsence`

```python
client.add_part_day_absence(time_zone_id=..., business_unit_id=..., person_id=..., period=..., absence_id=..., scenario_id=..., convert_if_applicable_for_full_day=..., attribute_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `absence_id` | `str / UUID` | Yes |
| `scenario_id` | `str / UUID / None` | No |
| `convert_if_applicable_for_full_day` | `int` | No |
| `attribute_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## add person

`/command/AddPerson`

```python
client.add_person(time_zone_id=..., business_unit_id=..., first_name=..., last_name=..., start_date=..., email=..., employment_number=..., application_logon=..., identity=..., team_id=..., contract_id=..., contract_schedule_id=..., part_time_percentage_id=..., role_ids=..., workflow_control_set_id=..., shift_bag_id=..., budget_group_id=..., first_day_of_week=..., culture=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `first_name` | `str / None` | No |
| `last_name` | `str / None` | No |
| `start_date` | `str / date / None` | No |
| `email` | `str / None` | No |
| `employment_number` | `str / None` | No |
| `application_logon` | `str / None` | No |
| `identity` | `str / None` | No |
| `team_id` | `str / UUID / None` | No |
| `contract_id` | `str / UUID / None` | No |
| `contract_schedule_id` | `str / UUID / None` | No |
| `part_time_percentage_id` | `str / UUID / None` | No |
| `role_ids` | `list[Any] / None` | No |
| `workflow_control_set_id` | `str / UUID / None` | No |
| `shift_bag_id` | `str / UUID / None` | No |
| `budget_group_id` | `str / UUID / None` | No |
| `first_day_of_week` | `int / None` | No |
| `culture` | `str / None` | No |

## add schedule changes listener

`/command/AddScheduleChangesListener`

```python
client.add_schedule_changes_listener(business_unit_id=..., url=..., name=..., days_start_from_current_date=..., days_end_from_current_date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `url` | `str` | Yes |
| `name` | `str` | Yes |
| `days_start_from_current_date` | `int` | Yes |
| `days_end_from_current_date` | `int` | Yes |

## add scheduled heads per dp

`/command/AddScheduledHeadsPerDp`

```python
client.add_scheduled_heads_per_dp(business_unit_id=..., time_zone=..., dp_id=..., interval_wise_scheduled_heads=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `time_zone` | `str` | Yes |
| `dp_id` | `str / UUID` | Yes |
| `interval_wise_scheduled_heads` | `list[Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `interval_wise_scheduled_heads[].start_date_time` | `str / datetime` | Yes |
| `interval_wise_scheduled_heads[].scheduled_heads` | `float` | Yes |

## add skills to person

`/command/AddSkillsToPerson`

```python
client.add_skills_to_person(business_unit_id=..., person_id=..., start_date=..., skill_ids=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | No |
| `start_date` | `str / date / None` | No |
| `skill_ids` | `list[Any] / None` | No |

## add team

`/command/AddTeam`

```python
client.add_team(business_unit_id=..., team_name=..., site_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `team_name` | `str` | Yes |
| `site_id` | `str / UUID` | No |

## clear leaving date for person

`/command/ClearLeavingDateForPerson`

```python
client.clear_leaving_date_for_person(person_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |

## delete account for person account

`/command/DeleteAccountForPersonAccount`

```python
client.delete_account_for_person_account(person_id=..., date_from=..., absence_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `date_from` | `str / date` | Yes |
| `absence_id` | `str / UUID` | Yes |

## edit meetings

`/command/EditMeetings`

```python
client.edit_meetings(time_zone_id=..., external_meetings=..., handle_non_overwritable_activities=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str / None` | No |
| `external_meetings` | `list[Any]` | Yes |
| `handle_non_overwritable_activities` | `str / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `external_meetings[].external_meeting_id` | `str` | Yes |
| `external_meetings[].period` | `dict[str, Any] / None` | No |
| `external_meetings[].period.start_time` | `str / datetime` | No |
| `external_meetings[].period.end_time` | `str / datetime` | No |
| `external_meetings[].participants` | `list[Any] / None` | No |
| `external_meetings[].activity_id` | `str / UUID / None` | No |
| `external_meetings[].title` | `str / None` | No |
| `external_meetings[].location` | `str / None` | No |
| `external_meetings[].agenda` | `str / None` | No |

## import backlog queue

`/command/ImportBacklogQueue`

```python
client.import_backlog_queue(tasks=..., upload_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `tasks` | `list[Any]` | Yes |
| `upload_id` | `str / UUID` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `tasks[].queue_id` | `str` | Yes |
| `tasks[].queue_name` | `str` | Yes |
| `tasks[].task_id` | `str` | Yes |
| `tasks[].offered_at` | `str / datetime` | Yes |
| `tasks[].first_handled_at` | `str / datetime / None` | No |
| `tasks[].completed_at` | `str / datetime / None` | No |
| `tasks[].task_work_time_seconds` | `int` | Yes |
| `tasks[].after_task_work_time_seconds` | `int` | Yes |
| `tasks[].queuing_time_seconds` | `int` | Yes |
| `tasks[].is_handled_within_service_level` | `bool` | Yes |
| `tasks[].task_status_description` | `str` | Yes |

## process backlog queue

`/command/ProcessBacklogQueue`

```python
client.process_backlog_queue()
```

No arguments needed.

## remove full day absence

`/command/RemoveFullDayAbsence`

```python
client.remove_full_day_absence(business_unit_id=..., person_id=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## remove meetings

`/command/RemoveMeetings`

```python
client.remove_meetings(external_meeting_ids=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `external_meeting_ids` | `list[Any]` | Yes |

## remove overtime

`/command/RemoveOvertime`

```python
client.remove_overtime(time_zone_id=..., business_unit_id=..., person_id=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## remove part day absence

`/command/RemovePartDayAbsence`

```python
client.remove_part_day_absence(time_zone_id=..., business_unit_id=..., person_id=..., period=..., scenario_id=..., absence_ids=..., attribute_ids=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |
| `absence_ids` | `list[Any] / None` | No |
| `attribute_ids` | `list[Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## remove skills for person

`/command/RemoveSkillsForPerson`

```python
client.remove_skills_for_person(business_unit_id=..., person_id=..., start_date=..., skill_ids=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | No |
| `start_date` | `str / date / None` | No |
| `skill_ids` | `list[Any] / None` | No |

## set availability

`/command/SetAvailability`

```python
client.set_availability(business_unit_id=..., person_id=..., availability_id=..., start_date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | No |
| `availability_id` | `str / UUID` | No |
| `start_date` | `str / date / None` | No |

## set budget group for person

`/command/SetBudgetGroupForPerson`

```python
client.set_budget_group_for_person(business_unit_id=..., start_date=..., person_id=..., budget_group_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `start_date` | `str / date / None` | No |
| `person_id` | `str / UUID` | No |
| `budget_group_id` | `str / UUID` | No |

## set details for person

`/command/SetDetailsForPerson`

```python
client.set_details_for_person(person_id=..., first_name=..., last_name=..., email=..., workflow_control_set_id=..., note=..., employment_number=..., identity=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | No |
| `first_name` | `str / None` | No |
| `last_name` | `str / None` | No |
| `email` | `str / None` | No |
| `workflow_control_set_id` | `str / UUID / None` | No |
| `note` | `str / None` | No |
| `employment_number` | `str / None` | No |
| `identity` | `str / None` | No |

## set employment details for person

`/command/SetEmploymentDetailsForPerson`

```python
client.set_employment_details_for_person(business_unit_id=..., start_date=..., person_id=..., contract_id=..., contract_schedule_id=..., part_time_percentage_id=..., team_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `start_date` | `str / date / None` | No |
| `person_id` | `str / UUID` | No |
| `contract_id` | `str / UUID / None` | No |
| `contract_schedule_id` | `str / UUID / None` | No |
| `part_time_percentage_id` | `str / UUID / None` | No |
| `team_id` | `str / UUID / None` | No |

## set external logons for person

`/command/SetExternalLogonsForPerson`

```python
client.set_external_logons_for_person(person_id=..., date=..., external_logon_ids=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | No |
| `date` | `str / date / None` | No |
| `external_logon_ids` | `list[Any] / None` | No |

## set forecast

`/command/SetForecast`

```python
client.set_forecast(business_unit_id=..., skill_id=..., scenario_id=..., days=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `skill_id` | `str / UUID` | No |
| `scenario_id` | `str / UUID / None` | No |
| `days` | `list[Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `days[].date` | `str / date / None` | No |
| `days[].intervals` | `list[Any] / None` | No |
| `days[].intervals[].tasks` | `float` | No |
| `days[].intervals[].average_task_time_seconds` | `float` | No |
| `days[].intervals[].average_after_task_time_seconds` | `float` | No |
| `days[].intervals[].agents_override` | `float / None` | No |
| `days[].intervals[].start_time_utc` | `str / datetime` | No |

## set forecast daily

`/command/SetForecastDaily`

```python
client.set_forecast_daily(business_unit_id=..., skill_id=..., scenario_id=..., days=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `skill_id` | `str / UUID` | No |
| `scenario_id` | `str / UUID / None` | No |
| `days` | `list[Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `days[].date` | `str / date / None` | No |
| `days[].tasks` | `float / None` | No |
| `days[].average_task_time_seconds` | `float / None` | No |
| `days[].average_after_task_time_seconds` | `float / None` | No |
| `days[].work_load_id` | `str / UUID / None` | No |

## set leaving date for person

`/command/SetLeavingDateForPerson`

```python
client.set_leaving_date_for_person(person_id=..., date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |

## set location

`/command/SetLocation`

```python
client.set_location(business_unit_id=..., person_ids=..., period=..., location=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_ids` | `list[Any]` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `location` | `str / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## set note for schedule day

`/command/SetNoteForScheduleDay`

```python
client.set_note_for_schedule_day(business_unit_id=..., scenario_id=..., person_id=..., date=..., note=..., is_public=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `scenario_id` | `str / UUID / None` | No |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |
| `note` | `str` | Yes |
| `is_public` | `bool` | Yes |

## set optional column for people

`/command/SetOptionalColumnForPeople`

```python
client.set_optional_column_for_people(person_ids=..., optional_column_id=..., value=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_ids` | `list[Any]` | Yes |
| `optional_column_id` | `str / UUID` | Yes |
| `value` | `str` | Yes |

## set optional column for person

`/command/SetOptionalColumnForPerson`

```python
client.set_optional_column_for_person(person_id=..., optional_column_id=..., value=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `optional_column_id` | `str / UUID` | Yes |
| `value` | `str` | Yes |

## set roles for person

`/command/SetRolesForPerson`

```python
client.set_roles_for_person(person_id=..., role_ids=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | No |
| `role_ids` | `list[Any] / None` | No |

## set rotation

`/command/SetRotation`

```python
client.set_rotation(business_unit_id=..., person_id=..., rotation_id=..., start_date=..., start_week=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | No |
| `rotation_id` | `str / UUID` | No |
| `start_date` | `str / date / None` | No |
| `start_week` | `int` | No |

## set schedules for person

`/command/SetSchedulesForPerson`

```python
client.set_schedules_for_person(time_zone_id=..., business_unit_id=..., date_period=..., schedule_days=..., person_id=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `time_zone_id` | `str` | Yes |
| `business_unit_id` | `str / UUID` | Yes |
| `date_period` | `dict[str, Any]` | Yes |
| `schedule_days` | `list[Any]` | Yes |
| `person_id` | `str / UUID` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `date_period.start_date` | `str / date / None` | No |
| `date_period.end_date` | `str / date / None` | No |
| `schedule_days[].date` | `str / date` | Yes |
| `schedule_days[].shift_category_id` | `str / UUID / None` | No |
| `schedule_days[].day_off_template_id` | `str / UUID / None` | No |
| `schedule_days[].full_day_absence_id` | `str / UUID / None` | No |
| `schedule_days[].attribute_id` | `str / UUID / None` | No |
| `schedule_days[].layers` | `list[Any] / None` | No |
| `schedule_days[].layers[].period` | `dict[str, Any]` | Yes |
| `schedule_days[].layers[].period.start_time` | `str / datetime` | No |
| `schedule_days[].layers[].period.end_time` | `str / datetime` | No |
| `schedule_days[].layers[].activity_id` | `str / UUID / None` | No |
| `schedule_days[].layers[].absence_id` | `str / UUID / None` | No |
| `schedule_days[].layers[].attribute_id` | `str / UUID / None` | No |

## set shift bag for person

`/command/SetShiftBagForPerson`

```python
client.set_shift_bag_for_person(business_unit_id=..., start_date=..., person_id=..., shift_bag_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `start_date` | `str / date / None` | No |
| `person_id` | `str / UUID` | No |
| `shift_bag_id` | `str / UUID` | No |

## set shrinkage

`/command/SetShrinkage`

```python
client.set_shrinkage(business_unit_id=..., skill_id=..., scenario_id=..., days=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `skill_id` | `str / UUID` | No |
| `scenario_id` | `str / UUID / None` | No |
| `days` | `list[Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `days[].date` | `str / date / None` | No |
| `days[].intervals` | `list[Any] / None` | No |
| `days[].intervals[].start_time_utc` | `str / datetime` | No |
| `days[].intervals[].shrinkage` | `int` | No |

## set skills for person

`/command/SetSkillsForPerson`

```python
client.set_skills_for_person(business_unit_id=..., person_id=..., start_date=..., skill_ids=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | No |
| `start_date` | `str / date / None` | No |
| `skill_ids` | `list[Any] / None` | No |

## set team for person

`/command/SetTeamForPerson`

```python
client.set_team_for_person(business_unit_id=..., start_date=..., team_id=..., person_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `start_date` | `str / date / None` | No |
| `team_id` | `str / UUID` | No |
| `person_id` | `str / UUID` | No |

## all absences

`/query/Absence/AllAbsences`

```python
client.all_absences(business_unit_id=..., filter=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `filter` | `int` | No |

## get absence attribute

`/query/AbsenceAttribute/GetAbsenceAttribute`

```python
client.get_absence_attribute(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## get all absence attribute

`/query/AbsenceAttribute/GetAllAbsenceAttribute`

```python
client.get_all_absence_attribute(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## absence possibility by person id

`/query/AbsencePossibility/AbsencePossibilityByPersonId`

```python
client.absence_possibility_by_person_id(business_unit_id=..., person_id=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## absence request by id

`/query/AbsenceRequest/AbsenceRequestById`

```python
client.absence_request_by_id(business_unit_id=..., request_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `request_id` | `str / UUID` | Yes |

## absence request rules by person id

`/query/AbsenceRequestRule/AbsenceRequestRulesByPersonId`

```python
client.absence_request_rules_by_person_id(business_unit_id=..., person_id=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## activities available for request by person and date

`/query/Activity/ActivitiesAvailableForRequestByPersonAndDate`

```python
client.activities_available_for_request_by_person_and_date(business_unit_id=..., person_id=..., date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |

## all activities

`/query/Activity/AllActivities`

```python
client.all_activities(business_unit_id=..., filter=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `filter` | `int` | No |

## activity request by id

`/query/ActivityRequest/ActivityRequestById`

```python
client.activity_request_by_id(business_unit_id=..., request_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `request_id` | `str / UUID` | Yes |

## permission by person

`/query/ApplicationFunction/PermissionByPerson`

```python
client.permission_by_person(business_unit_id=..., person_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |

## all availabilities

`/query/Availability/AllAvailabilities`

```python
client.all_availabilities(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all budget groups

`/query/BudgetGroup/AllBudgetGroups`

```python
client.all_budget_groups(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all business units

`/query/BusinessUnit/AllBusinessUnits`

```python
client.all_business_units()
```

No arguments needed.

## all contracts

`/query/Contract/AllContracts`

```python
client.all_contracts(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all contract schedules

`/query/ContractSchedule/AllContractSchedules`

```python
client.all_contract_schedules(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all day off templates

`/query/DayOffTemplate/AllDayOffTemplates`

```python
client.all_day_off_templates(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## get employee defaults

`/query/EmployeeDefaults/GetEmployeeDefaults`

```python
client.get_employee_defaults(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## external logon by id

`/query/ExternalLogon/ExternalLogonById`

```python
client.external_logon_by_id(id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `id` | `str / UUID` | Yes |

## external logons by data source

`/query/ExternalLogon/ExternalLogonsByDataSource`

```python
client.external_logons_by_data_source(data_source_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `data_source_id` | `int` | Yes |

## external logons by person

`/query/ExternalLogon/ExternalLogonsByPerson`

```python
client.external_logons_by_person(person_id=..., date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |

## forecast by skill

`/query/Forecast/ForecastBySkill`

```python
client.forecast_by_skill(business_unit_id=..., skill_id=..., period=..., apply_shrinkage=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `skill_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `apply_shrinkage` | `bool` | No |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## locations by person ids

`/query/Location/LocationsByPersonIds`

```python
client.locations_by_person_ids(business_unit_id=..., person_ids=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_ids` | `list[Any]` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## all multiplicator definition sets

`/query/MultiplicatorDefinitionSet/AllMultiplicatorDefinitionSets`

```python
client.all_multiplicator_definition_sets(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## nightly rest by person id

`/query/NightlyRest/NightlyRestByPersonId`

```python
client.nightly_rest_by_person_id(person_id=..., date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |

## all optional columns

`/query/OptionalColumn/AllOptionalColumns`

```python
client.all_optional_columns(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID / None` | No |

## overtime possibility by person id

`/query/OvertimePossibility/OvertimePossibilityByPersonId`

```python
client.overtime_possibility_by_person_id(business_unit_id=..., person_id=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## overtime request by id

`/query/OvertimeRequest/OvertimeRequestById`

```python
client.overtime_request_by_id(business_unit_id=..., request_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `request_id` | `str / UUID` | Yes |

## overtime request configuration by person id

`/query/OvertimeRequestConfiguration/OvertimeRequestConfigurationByPersonId`

```python
client.overtime_request_configuration_by_person_id(business_unit_id=..., person_id=..., date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |

## overtime valid possibility by person id

`/query/OvertimeValidPossibility/OvertimeValidPossibilityByPersonId`

```python
client.overtime_valid_possibility_by_person_id(business_unit_id=..., person_id=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## all part time percentages

`/query/PartTimePercentage/AllPartTimePercentages`

```python
client.all_part_time_percentages(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## people by business unit id

`/query/Person/PeopleByBusinessUnitId`

```python
client.people_by_business_unit_id(business_unit_id=..., date=..., page=..., page_size=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `date` | `str / date / None` | No |
| `page` | `int` | No |
| `page_size` | `int` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## people by employment numbers

`/query/Person/PeopleByEmploymentNumbers`

```python
client.people_by_employment_numbers(employment_numbers=..., date=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `employment_numbers` | `list[Any]` | Yes |
| `date` | `str / date / None` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## people by group page group

`/query/Person/PeopleByGroupPageGroup`

```python
client.people_by_group_page_group(business_unit_id=..., group_page_group_id=..., date=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `group_page_group_id` | `str / UUID` | No |
| `date` | `str / date / None` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## people by identities

`/query/Person/PeopleByIdentities`

```python
client.people_by_identities(identities=..., date=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `identities` | `list[Any]` | Yes |
| `date` | `str / date / None` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## people by ids

`/query/Person/PeopleByIds`

```python
client.people_by_ids(ids=..., date=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `ids` | `list[Any]` | Yes |
| `date` | `str / date / None` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## people by skill group

`/query/Person/PeopleBySkillGroup`

```python
client.people_by_skill_group(skill_group_id=..., date=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `skill_group_id` | `str / UUID` | No |
| `date` | `str / date / None` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## people by team id

`/query/Person/PeopleByTeamId`

```python
client.people_by_team_id(team_id=..., date=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `team_id` | `str / UUID / None` | No |
| `date` | `str / date / None` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## person by id

`/query/Person/PersonById`

```python
client.person_by_id(person_id=..., date=..., include=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date / None` | No |
| `include` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `include.optional_columns` | `bool` | No |

## person accounts by person id

`/query/PersonAccount/PersonAccountsByPersonId`

```python
client.person_accounts_by_person_id(business_unit_id=..., person_id=..., date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |

## all roles

`/query/Role/AllRoles`

```python
client.all_roles(business_unit_id=..., get_application_functions_and_available_data=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `get_application_functions_and_available_data` | `bool` | No |

## all rotations

`/query/Rotation/AllRotations`

```python
client.all_rotations(business_unit_id=..., include_details=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `include_details` | `bool` | No |

## rotation by id

`/query/Rotation/RotationById`

```python
client.rotation_by_id(rotation_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `rotation_id` | `str / UUID` | Yes |

## all scenarios

`/query/Scenario/AllScenarios`

```python
client.all_scenarios(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## schedule by person id

`/query/Schedule/ScheduleByPersonId`

```python
client.schedule_by_person_id(person_id=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## schedule by person ids

`/query/Schedule/ScheduleByPersonIds`

```python
client.schedule_by_person_ids(person_ids=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_ids` | `list[Any]` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## schedule by team id

`/query/Schedule/ScheduleByTeamId`

```python
client.schedule_by_team_id(business_unit_id=..., team_id=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `team_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## schedule absences by person ids

`/query/ScheduleAbsence/ScheduleAbsencesByPersonIds`

```python
client.schedule_absences_by_person_ids(person_ids=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_ids` | `list[Any]` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## schedule audit trail by person id

`/query/ScheduleAuditTrail/ScheduleAuditTrailByPersonId`

```python
client.schedule_audit_trail_by_person_id(person_id=..., date=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | No |
| `date` | `str / date` | Yes |
| `scenario_id` | `str / UUID / None` | No |

## schedules by change date

`/query/ScheduleChanges/SchedulesByChangeDate`

```python
client.schedules_by_change_date(changes_from=..., changes_to=..., page=..., page_size=..., business_unit_id=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `changes_from` | `str / datetime` | Yes |
| `changes_to` | `str / datetime / None` | No |
| `page` | `int` | Yes |
| `page_size` | `int` | No |
| `business_unit_id` | `str / UUID / None` | No |
| `period` | `dict[str, Any] / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## all schedule changes listener subscription

`/query/ScheduleChangesListenerSubscription/AllScheduleChangesListenerSubscription`

```python
client.all_schedule_changes_listener_subscription(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## schedule by group page groups

`/query/ScheduleOrder/ScheduleByGroupPageGroups`

```python
client.schedule_by_group_page_groups(business_unit_id=..., group_page_group_ids=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `group_page_group_ids` | `list[Any]` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## all shift bags

`/query/ShiftBag/AllShiftBags`

```python
client.all_shift_bags(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all shift categories

`/query/ShiftCategory/AllShiftCategories`

```python
client.all_shift_categories(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all sites

`/query/Site/AllSites`

```python
client.all_sites(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all skills

`/query/Skill/AllSkills`

```python
client.all_skills(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all skill groups

`/query/SkillGroup/AllSkillGroups`

```python
client.all_skill_groups(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## staffing by skills

`/query/Staffing/StaffingBySkills`

```python
client.staffing_by_skills(business_unit_id=..., skill_ids=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `skill_ids` | `list[Any]` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_time` | `str / datetime` | No |
| `period.end_time` | `str / datetime` | No |

## all teams

`/query/Team/AllTeams`

```python
client.all_teams(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |

## all teams with agents

`/query/Team/AllTeamsWithAgents`

```python
client.all_teams_with_agents(business_unit_id=..., period=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## team by id

`/query/Team/TeamById`

```python
client.team_by_id(business_unit_id=..., id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `id` | `str / UUID` | No |

## teams by site id

`/query/Team/TeamsBySiteId`

```python
client.teams_by_site_id(business_unit_id=..., site_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `site_id` | `str / UUID` | No |

## user by id

`/query/User/UserById`

```python
client.user_by_id(person_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `person_id` | `str / UUID` | Yes |

## weekly max work time by person id

`/query/WeeklyMaxWorkTime/WeeklyMaxWorkTimeByPersonId`

```python
client.weekly_max_work_time_by_person_id(business_unit_id=..., person_id=..., date=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `date` | `str / date` | Yes |

## workload by skill ids

`/query/WorkLoad/WorkloadBySkillIds`

```python
client.workload_by_skill_ids(business_unit_id=..., skill_ids=..., page=..., page_size=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `skill_ids` | `list[Any] / None` | No |
| `page` | `int` | No |
| `page_size` | `int` | No |

## work time by person id

`/query/WorkTime/WorkTimeByPersonId`

```python
client.work_time_by_person_id(business_unit_id=..., person_id=..., period=..., scenario_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
| `person_id` | `str / UUID` | Yes |
| `period` | `dict[str, Any]` | Yes |
| `scenario_id` | `str / UUID / None` | No |

Nested dictionary/list fields (use these snake_case names):

| Field | Accepted type | Required by API |
| --- | --- | --- |
| `period.start_date` | `str / date / None` | No |
| `period.end_date` | `str / date / None` | No |

## all workflow control sets

`/query/WorkflowControlSet/AllWorkflowControlSets`

```python
client.all_workflow_control_sets(business_unit_id=...)
```

| Argument | Accepted type | Required by API |
| --- | --- | --- |
| `business_unit_id` | `str / UUID` | Yes |
