# Rysis - Visibill: Unitrans Balancing

[⬆ Back to Parent](../visibill/README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This document is part of the "Visibill" component documentation within the Rysis project, focusing on data reconciliation and reporting.

## Contents Overview

This file details procedures, Excel functions, and SQL queries used for balancing and reconciling Unitrans MTN and Vodacom reports within the Visibill system. It includes examples of relevant tickets and SQL queries designed to identify discrepancies in MSISDNs (phone numbers) and amounts between different data sources.

## Role in System

This documentation is critical for maintaining data integrity and accuracy in billing and reporting for Unitrans clients within the Visibill system. It provides a systematic approach to identifying and resolving data imbalances, ensuring reliable financial and operational insights.

## Key Information and Procedures

### Ticket Examples

References to specific support tickets illustrating balancing issues or resolutions:

-   [RY-009487](https://app.chronodesk.io/rysisprod/tickets/edit/15550)
-   [RY-009558](https://app.chronodesk.io/rysisprod/tickets/edit/15621)
-   [RY-009842](https://app.chronodesk.io/rysisprod/tickets/edit/15905)

### Data Sources for Balancing

-   `Total Column` on `UNITRANS CorporateMonthlyBIllingDetail 2`
-   `AMOUNTEXVAT Column` on `AFRICA TNET`
-   `AMOUNTEXVAT Column` on `UNITRANS TNETS`

### Excel Record Functions

Examples of Excel formulas used to generate SQL `INSERT` statements for temporary tables, facilitating data comparison:

```excel
IF(AA2<>"", "INSERT INTO @TempVisibill (MSISDN,Amount) VALUES ('"&C2&"',"&AA2&")", "INSERT INTO @TempVisibill (MSISDN,Amount) VALUES ('"&C2&"', NULL)")
="INSERT INTO @TempTNET(MSISDN,Amount) VALUES ('0"&E2&"', "&J2&")"
="INSERT INTO @TempTNET(MSISDN,Amount) VALUES (substring('0"&D2&"', 1, (len('0"&D2&"') - 3)), "&AO2&")"
```

### SQL Queries for Data Reconciliation

SQL queries designed to identify discrepancies and balance data between temporary tables (`@TempVisibill` and `@TempTNET`):

-   **Check amount in TNET where MSISDN does not exist in Visibill**:
    ```sql
    SELECT t.MSISDN , t.Amount FROM @TempTNET t
    LEFT JOIN @TempVisibill v ON v.MSISDN = t.MSISDN
    WHERE v.MSISDN IS NULL
    ```

-   **Check amount in Visibill where MSISDN does not exist in TNET**:
    ```sql
    SELECT  t.MSISDN , t.Amount FROM @TempVisibill t
    LEFT JOIN @TempTNET v ON v.MSISDN = t.MSISDN
    WHERE v.MSISDN IS NULL
    ```

-   **Check for Amounts that are not matching**:
    ```sql
    SELECT  t.MSISDN , t.Amount , v.Amount FROM @TempVisibill t
    LEFT JOIN @TempTNET v ON v.MSISDN = t.MSISDN
    WHERE v.Amount <> t.Amount
    ```

-   **Extra checks (example for a specific MSISDN and BillMonth)**:
    ```sql
    SELECT * FROM [VisibillUnitrans].[dbo].[DW_SubscriberMonthTotals02]
    WHERE MSISDN = '0833062840' and BillMonth = '01 May 2023'
    ```

-   **Calculate total difference between TNET and Visibill amounts**:
    ```sql
    select ((select SUM(Amount) from @TempTNET) - (select SUM(Amount) from @TempVisibill)) as diff
    ```