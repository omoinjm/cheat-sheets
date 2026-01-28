# Optix - Data Analytics Statistics (`da-stats.md`)

[⬆ Back to Parent](../optix/README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This document is part of the "Optix" component documentation within the Rysis project, focusing on data analytics and reporting.

## Contents Overview

This file details the database tables, stored procedures (`PROC`), and API configurations associated with various data analytics and reporting tabs within the Optix system. It provides a breakdown of the data sources and parameters used for generating statistics related to Drive Alert, User Performance, Early Warning Summaries, Vehicle Behaviour Counts, and Early Warning Reports.

## Role in System

This document is crucial for understanding the data model and reporting mechanisms of the Optix system. It serves as a reference for developers, data analysts, and support staff who need to interpret reports, troubleshoot data discrepancies, or extend the reporting capabilities.

## Tables Related to Each Tab

### DriveCam - Statistics

-   **Link**: [DriveCam - Statistics](https://qa.velocity.optixonline.co.za/pages/drivecam/da-stats)

### Drive Alert Stats

-   **API Endpoint**: `https://reports.optixonline.co.za/api/`
-   **Associated Tables/Configs**:
    -   `GROUP`: `_DriveCam_GroupInfo_`
    -   `CUSTOMER`: `_MA_Customer_`
    -   `API CONFIG`: `_DriveCam_ApiConfig_`
    -   `DATE INTERVAL`: `_LU_DateRange_`
    -   `YEAR`: `_vLU_Year_`
    -   `TYPE`: `_LU_ReportType_`

### User Performance Stats

-   **API Endpoint**: `https://reports.optixonline.co.za/api/`
-   **Parameters**:
    -   `START DATE`: User Interface (`_UI_`)
    -   `END DATE`: User Interface (`_UI_`)
    -   `REPORT TYPE`: `_EW_IncidentType_`

### Early Warning Summary

-   **Stored Procedure**: `_STATS_EarlyWarningFigures_`
-   **Associated Tables**:
    -   `_DriveCamIncidentNotificationHeader_Reviewed_`
    -   `_DriveCamIncidentType_`
    -   `_EW_IncidentType_`
    -   `_LU_DriveCamEventBehaviourOutcome_`
    -   `_LU_BehaviourOutcome_`
-   **Parameters**:
    -   `START DATE`: User Interface (`_UI_`)
    -   `END DATE`: User Interface (`_UI_`)

### Vehicle Behaviour Count

-   **Stored Procedure**: `_STATS_VehicleCount_`
-   **Associated Tables**:
    -   `_DriveCamIncidentNotificationHeader_Reviewed_`
    -   `_LU_DriveCamEventBehaviourOutcome_`
    -   `_LU_BehaviourOutcome_`
-   **Parameters**:
    -   `RECORDED TIME`: User Interface (`_UI_`)
    -   `OBSERVATIONS`: `_LU_ObservationOutcome_`
    -   `BEHAVIOURS`: `_LU_BehaviourOutcome_`

### Early Warning Reports

-   **Parameters/Configs**:
    -   `GROUP NAME`: `_LYTX_Group_List_Modal_`
    -   `PRODUCT`: `_EW_IncidentType_`
    -   `EVENT`: N/A
    -   `VEHICLE`: N/A
    -   `STATUS`: N/A
    -   `CLIENT`: `_MA_Customer_`
    -   `API`: `_DriveCam_ApiConfig_`
    -   `BEHAVIOURS`: `_LU_BehaviourOutcome_`
    -   `OBSERVATIONS`: `_LU_ObservationOutcome_`
    -   `START DATE`: User Interface (`_UI_`)
    -   `END DATE`: User Interface (`_UI_`)