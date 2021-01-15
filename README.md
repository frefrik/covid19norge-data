# COVID-19 Datasets for Norway
![badge-last-update](https://img.shields.io/github/last-commit/frefrik/c19norge-data?label=Last%20update)
## Description
This repository contains datasets of daily time-series data related to COVID-19 in Norway.  

## Overview
<!-- table starts -->
|Data|Source|Last updated|Download|Preview|
| :--- | :--- | :--- | :--- | :--- |
|[Confirmed](#confirmedcsv)|FHI / MSIS|2021-01-15 15:10:04+01:00|[<center>csv</center>](https://raw.githubusercontent.com/frefrik/c19norge-data/main/data/confirmed.csv)|[<center>preview</center>](data/confirmed.csv)|
|[Dead](#deadcsv)|FHI|2021-01-15 13:25:03+01:00|[<center>csv</center>](https://raw.githubusercontent.com/frefrik/c19norge-data/main/data/dead.csv)|[<center>preview</center>](data/dead.csv)|
|[Hospitalized](#hospitalizedcsv)|Helsedirektoratet|2021-01-15 13:00:02+01:00|[<center>csv</center>](https://raw.githubusercontent.com/frefrik/c19norge-data/main/data/hospitalized.csv)|[<center>preview</center>](data/hospitalized.csv)|
|[Tested](#testedcsv)|FHI|2021-01-15 13:25:02+01:00|[<center>csv</center>](https://raw.githubusercontent.com/frefrik/c19norge-data/main/data/tested.csv)|[<center>preview</center>](data/tested.csv)|
|[Tested Lab](#tested_labcsv)|FHI|2021-01-15 13:20:03+01:00|[<center>csv</center>](https://raw.githubusercontent.com/frefrik/c19norge-data/main/data/tested_lab.csv)|[<center>preview</center>](data/tested_lab.csv)|
|[Transport](#transportcsv)|FHI|2021-01-15 13:59:07+01:00|[<center>csv</center>](https://raw.githubusercontent.com/frefrik/c19norge-data/main/data/transport.csv)|[<center>preview</center>](data/transport.csv)|
|[Vaccine Doses](#vaccine_dosescsv)|FHI|2021-01-15 14:05:13+01:00|[<center>csv</center>](https://raw.githubusercontent.com/frefrik/c19norge-data/main/data/vaccine_doses.csv)|[<center>preview</center>](data/vaccine_doses.csv)|
<!-- table ends -->
## Datafiles
### confirmed.csv
Number of cases reported daily in Norway since the start of the epidemic.

**Data source:**
- https://statistikk.fhi.no/msis
- https://github.com/folkehelseinstituttet/surveillance_data


```
date,new,total,source
2020-11-13,687,28807,fhi:git
2020-11-14,366,29173,fhi:git
2020-11-15,259,29432,fhi:git
2020-11-16,78,29510,fhi:git
2020-11-17,239,29749,msis:api
...
```  

---
### dead.csv
Number of COVID-19 associated deaths notified to the Norwegian Institute of Public Health.

**Data source:**
- https://github.com/folkehelseinstituttet/surveillance_data


```
date,new,total,source
2020-11-11,0,285,fhi:git
2020-11-12,6,291,fhi:git
2020-11-13,3,294,fhi:git
2020-11-16,0,294,fhi:git
2020-11-17,4,298,fhi:git
...
```

---
### hospitalized.csv
Number of hospitalized patients.  
The hospitals register the daily number of patients who are admitted to hospital with proven covid-19 and the number of admitted patients who receive invasive respiratory treatment.

**Data source:**
* https://www.helsedirektoratet.no/statistikk/antall-innlagte-pasienter-pa-sykehus-med-pavist-covid-19

```
date,admissions,respiratory,source
2020-11-13,109,13,helsedir:api
2020-11-14,117,13,helsedir:api
2020-11-15,127,13,helsedir:api
2020-11-16,135,16,helsedir:api
2020-11-17,139,15,helsedir:api
...
```

---
### tested.csv
Number of COVID-19 tests performed.

**Data source:**
* https://www.fhi.no/sv/smittsomme-sykdommer/corona/dags--og-ukerapporter/dags--og-ukerapporter-om-koronavirus/

```
date,new,total,source
2020-11-11,25697,1924640,fhi:web
2020-11-12,27645,1952285,fhi:web
2020-11-13,27145,1979430,fhi:web
2020-11-16,55298,2034728,fhi:web
2020-11-17,16009,2050737,fhi:web
...
```

---
### tested_lab.csv
Number of tested persons per specimen collection date and number of positive results.  
The laboratory results are collected in the MSIS Laboratory Database.

**Data source:**
* https://github.com/folkehelseinstituttet/surveillance_data

```
date,new_neg,new_pos,pr100_pos,new_total,total_neg,total_pos,total,source
2020-11-12,22854,607,2.6,23461,1959573,27657,1987230,fhi:git
2020-11-13,20850,656,3.1,21506,1980423,28313,2008736,fhi:git
2020-11-14,9213,350,3.7,9563,1989636,28663,2018299,fhi:git
2020-11-15,8284,262,3.1,8546,1997920,28925,2026845,fhi:git
2020-11-16,4143,72,1.7,4215,2002063,28997,2031060,fhi:git
...
```

---
### transport.csv
List of departures where persons infected with covid-19 have been on board aircraft, ships, trains and buses.

**Data source:**
* https://www.fhi.no/sv/smittsomme-sykdommer/corona/koronavirus-og-covid-19-pa-offentlig-kommunikasjon/

```
tr_type,route,company,tr_from,tr_to,departure,arrival,source
Fly,SK330,SAS,Oslo,Trondheim,2020-11-16 06:55:00,2020-11-16 07:55:00,fhi:web
Fly,SK1474,SAS,København,Oslo,2020-11-15 22:55:00,,fhi:web
Fly,SK4035,SAS,Oslo,Stavanger,2020-11-15 15:30:00,2020-11-15 16:25:00,fhi:web
Fly,DY620,Norwegian,Oslo,Bergen,2020-11-13 16:29:00,2020-11-13 17:05:00,fhi:web
Fly,SK1320,SAS,Oslo,Ålesund,2020-11-13 13:00:00,2020-11-13 13:55:00,fhi:web
Fly,WF568,Widerøe,Bergen,Kristiansund,2020-11-13 11:00:00,2020-11-13 11:55:00,fhi:web
...
```

---
### vaccine_doses.csv
Number of people vaccinated with the 1st dose of the coronary vaccine.

**Data source:**
* https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/

```
date,new_doses_administered,total_doses_administered,source
2020-12-27,5,5,fhi:web
2020-12-28,591,596,fhi:web
2020-12-29,1066,1662,fhi:web
2020-12-30,420,2082,fhi:web
2020-12-31,72,2154,fhi:web
2021-01-01,5,2159,fhi:web
...
```
