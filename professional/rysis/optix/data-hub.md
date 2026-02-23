# Optix - Data Hub PostgreSQL Table Population (`data-hub.md`)

[⬆ Back to Parent](../optix/README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This document is part of the "Optix" component documentation within the Rysis project, focusing on database operations within the data hub.

## Contents Overview

This file provides SQL commands and a PostgreSQL `DO` block for populating the `endpoint` table on the data hub. It demonstrates how to query for existing `provider_organisation_group` and `provider_endpoint` information and then insert new records into the `endpoint` table, linking various data types (Vehicle Events, POIs, Vehicle Activity, Geofences, etc.) to a specific organization group.

## Role in System

This document is crucial for the setup and configuration of data ingestion and access within the Optix data hub. It details the process of registering specific data endpoints for different functionalities, ensuring that the system can properly track and utilize data from various sources associated with an organization group.

## Key SQL Operations

### Find Tables with Relevant Details

SQL queries to retrieve information from `provider_organisation_group`, `provider_endpoint`, and `endpoint` tables using a `provider_id` or `user_name`:

```sql
select * from provider_organisation_group where provider_id = '37665c53-72a1-4bb9-9870-0b68d1efc04c';
select * from provider_endpoint where provider_id = '37665c53-72a1-4bb9-9870-0b68d1efc04c';
select * from endpoint where user_name = 'ANGL000112';
```

### Add Organisation Group into the `endpoint` Table

A PostgreSQL `DO` block containing `INSERT` statements to populate the `endpoint` table. This script defines variables for `_group_name`, `_provider_organisation_group_id`, and `_api_key`, and then inserts multiple records for different data types (e.g., Vehicle Events, POIs, Geofences) associated with the specified organization group.

**Note**: The `_provider_organisation_group_id` and `_api_key` variables need to be populated with actual values before execution.

```sql
do $$
declare
_group_name varchar(100) := 'ANGL000112';
_provider_organisation_group_id UUID := ''; -- Find id on provider_organisation_group table
_api_key varchar(200) := ''; -- email `samantha.andrews@cartrack.com` for credentials
begin
-- ... (RAISE NOTICE statements) ...

insert into endpoint
(name, provider_organisation_group_id, created_datetime, active, provider_endpoint_id, user_name, password_keyvault_path, file_name)
values
-- ... (multiple INSERT value sets for various data types) ...

end $$;
```