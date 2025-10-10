@echo off
REM MongoDB Import Script for Windows
SET DB_NAME=banking_db

echo Starting MongoDB data import...

echo Importing T24_T24CORE_CUSTOMER...
mongoimport --db %DB_NAME% --collection T24_T24CORE_CUSTOMER --file T24_T24CORE_CUSTOMER.json --jsonArray

echo Importing T24_T24CORE_ACCOUNT...
mongoimport --db %DB_NAME% --collection T24_T24CORE_ACCOUNT --file T24_T24CORE_ACCOUNT.json --jsonArray

@REM echo Importing DANH_SACH_API_23...
@REM mongoimport --db %DB_NAME% --collection DANH_SACH_API_23 --file DANH_SACH_API_23.json --jsonArray

echo Importing CORP...
mongoimport --db %DB_NAME% --collection CORP --file CORP.json --jsonArray

echo Importing CORP_ACCT...
mongoimport --db %DB_NAME% --collection CORP_ACCT --file CORP_ACCT.json --jsonArray

echo Import completed!
pause
