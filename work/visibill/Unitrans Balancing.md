# Unitrans MTN and Vodacom Reports

Ticket Examples:

[RY-009487](https://app.chronodesk.io/rysisprod/tickets/edit/15550)

[RY-009558](https://app.chronodesk.io/rysisprod/tickets/edit/15621)

[RY-009842](https://app.chronodesk.io/rysisprod/tickets/edit/15905)

- Select from Total Column on UNITRANS CorporateMonthlyBIllingDetail 2
- Select from AMOUNTEXVAT Column on AFRICA TNET
- Select from AMOUNTEXVAT Column on UNITRANS TNETS

Excel record functions:

```excel
IF(AA2<>"", "INSERT INTO @TempVisibill (MSISDN,Amount) VALUES ('"&C2&"',"&AA2&")", "INSERT INTO @TempVisibill (MSISDN,Amount) VALUES ('"&C2&"', NULL)"
```

```excel
="INSERT INTO @TempTNET(MSISDN,Amount) VALUES ('0"&E2&"', "&J2&")"
```

```excel
="INSERT INTO @TempTNET(MSISDN,Amount) VALUES (substring('0"&D2&"', 1, (len('0"&D2&"') - 3)), "&AO2&")"
```

Query Data:

- Check amount in TNET where Msisdn does not exists

```sql
SELECT t.MSISDN , t.Amount FROM @TempTNET t
LEFT JOIN @TempVisibill v ON v.MSISDN = t.MSISDN
WHERE v.MSISDN IS NULL
```

- Checks Amnount on Visibill where Msisdn does not Exists

```sql
SELECT  t.MSISDN , t.Amount FROM @TempVisibill t
LEFT JOIN @TempTNET v ON v.MSISDN = t.MSISDN
WHERE v.MSISDN IS NULL
```

- Checks for Amounts that are not matching

```sql
SELECT  t.MSISDN , t.Amount , v.Amount FROM @TempVisibill t
LEFT JOIN @TempTNET v ON v.MSISDN = t.MSISDN
WHERE v.Amount <> t.Amount
```

- Extra checks

```sql
SELECT * FROM [VisibillUnitrans].[dbo].[DW_SubscriberMonthTotals02]
WHERE MSISDN = '0833062840' and BillMonth = '01 May 2023'
```

```sql
select ((select SUM(Amount) from @TempTNET) - (select SUM(Amount) from @TempVisibill)) as diff
```
