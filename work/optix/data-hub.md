# Populate Postgres table on data hub

### Add Organisation Group into the endpoint table

```sql
do $$
declare
_group_name varchar(100) := 'ANGL000112';
_provider_organisation_group_id UUID := ''; -- `Find id on provider_organisation_group` table
_api_key varchar(200) := ''; -- email `samantha.andrews@cartrack.com` for credentials
begin
-- Print the variable
RAISE NOTICE '%', _provider_organisation_group_id;
RAISE NOTICE '%', _group_name;
RAISE NOTICE '%', _api_key;

insert into endpoint
(name, provider_organisation_group_id, created_datetime, active, provider_endpoint_id, user_name, password_keyvault_path, file_name)
values
(_group_name || ' Vehicles Events', _provider_organisation_group_id, now(), true, '16a4397b-06b0-4747-a0da-e906bdb49c20', _group_name, _api_key, lower(_group_name) || 'vehicleevents'),
(_group_name || ' POIS', _provider_organisation_group_id, now(), true, '0d7d0a47-34c4-4c6f-a03a-7187cdf619ae', _group_name, _api_key, lower(_group_name) || 'pois'),
(_group_name || ' Vehicles Activity', _provider_organisation_group_id, now(), true, 'bb84ccc7-8c9b-4581-8023-a50d514d0ee6', _group_name, _api_key, lower(_group_name) || 'vehicleactivity'),
(_group_name || ' Geofences Visitors', _provider_organisation_group_id, now(), true, 'cc3955a4-59c0-4ed9-b6c6-ffdb756e370f', _group_name, _api_key, lower(_group_name) || 'geofencesvisitors'),
(_group_name || ' Geofences', _provider_organisation_group_id, now(), true, '1620f6c5-1d5e-4a9a-bc7a-2a8a2d2009e1', _group_name, _api_key, lower(_group_name) || 'geofences'),
(_group_name || ' Notifications', _provider_organisation_group_id, now(), true, '1a1588bf-b73b-43b0-9ecb-8f52ad42e864', _group_name, _api_key, lower(_group_name) || 'notifications'),
(_group_name || ' Trips', _provider_organisation_group_id, now(), true, '1260c213-27d8-441f-a8e8-ed6207f8a76e', _group_name, _api_key, lower(_group_name) || 'trips'),
(_group_name || ' Drivers', _provider_organisation_group_id, now(), true, 'd0e5224f-05a1-4ec4-9410-eb8ed06ec53a', _group_name, _api_key, lower(_group_name) || 'drivers'),
(_group_name || ' Vehicles', _provider_organisation_group_id, now(), true, 'b0b53db3-e8e7-49df-9921-38712dc0bd38', _group_name, _api_key, lower(_group_name) || 'vehicles'),
(_group_name || ' Vehicles Groups', _provider_organisation_group_id, now(), true, 'b58a4583-490c-46d0-b6b7-0aafcb087c87', _group_name, _api_key, lower(_group_name) || 'vehiclegroups');

end $$;

```
