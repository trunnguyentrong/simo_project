@echo off
REM MongoDB Import Script for Docker Container (Windows)
REM This script imports data into MongoDB running in Docker

SET CONTAINER_NAME=mongodb
SET DB_NAME=banking_db

echo ============================================================
echo Importing data to MongoDB in Docker container: %CONTAINER_NAME%
echo Database: %DB_NAME%
echo ============================================================
echo.

REM Check if container is running
docker ps | findstr %CONTAINER_NAME% >nul
if errorlevel 1 (
    echo ERROR: MongoDB container '%CONTAINER_NAME%' is not running!
    echo Please start the container first with: docker-compose up -d mongodb
    pause
    exit /b 1
)

echo Importing T24_T24CORE_CUSTOMER...
docker exec -i %CONTAINER_NAME% mongoimport --username admin --password password --authenticationDatabase admin --db %DB_NAME% --collection T24_T24CORE_CUSTOMER --jsonArray < T24_T24CORE_CUSTOMER.json

echo Importing T24_T24CORE_ACCOUNT...
docker exec -i %CONTAINER_NAME% mongoimport --username admin --password password --authenticationDatabase admin --db %DB_NAME% --collection T24_T24CORE_ACCOUNT --jsonArray < T24_T24CORE_ACCOUNT.json

echo Importing DANH_SACH_API_23...
docker exec -i %CONTAINER_NAME% mongoimport --username admin --password password --authenticationDatabase admin --db %DB_NAME% --collection DANH_SACH_API_23 --jsonArray < DANH_SACH_API_23.json

echo Importing CORP...
docker exec -i %CONTAINER_NAME% mongoimport --username admin --password password --authenticationDatabase admin --db %DB_NAME% --collection CORP --jsonArray < CORP.json

echo Importing CORP_ACCT...
docker exec -i %CONTAINER_NAME% mongoimport --username admin --password password --authenticationDatabase admin --db %DB_NAME% --collection CORP_ACCT --jsonArray < CORP_ACCT.json

echo.
echo ============================================================
echo Import completed!
echo ============================================================
echo.
echo To verify the data, run:
echo   docker exec -it %CONTAINER_NAME% mongosh -u admin -p password --authenticationDatabase admin %DB_NAME%
echo.
echo Then run queries like:
echo   db.T24_T24CORE_CUSTOMER.countDocuments()
echo   db.T24_T24CORE_ACCOUNT.countDocuments()
echo.
pause
