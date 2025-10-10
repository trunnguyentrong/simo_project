#!/bin/bash
# MongoDB Import Script for Docker Container
# This script imports data into MongoDB running in Docker

CONTAINER_NAME="mongodb"
DB_NAME="banking_db"

echo "============================================================"
echo "Importing data to MongoDB in Docker container: $CONTAINER_NAME"
echo "Database: $DB_NAME"
echo "============================================================"
echo ""

# Check if container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "ERROR: MongoDB container '$CONTAINER_NAME' is not running!"
    echo "Please start the container first with: docker-compose up -d mongodb"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Importing T24_T24CORE_CUSTOMER..."
docker exec -i $CONTAINER_NAME mongoimport \
    --username admin \
    --password password \
    --authenticationDatabase admin \
    --db $DB_NAME \
    --collection T24_T24CORE_CUSTOMER \
    --jsonArray \
    < "$SCRIPT_DIR/T24_T24CORE_CUSTOMER.json"

echo "Importing T24_T24CORE_ACCOUNT..."
docker exec -i $CONTAINER_NAME mongoimport \
    --username admin \
    --password password \
    --authenticationDatabase admin \
    --db $DB_NAME \
    --collection T24_T24CORE_ACCOUNT \
    --jsonArray \
    < "$SCRIPT_DIR/T24_T24CORE_ACCOUNT.json"

echo "Importing DANH_SACH_API_23..."
docker exec -i $CONTAINER_NAME mongoimport \
    --username admin \
    --password password \
    --authenticationDatabase admin \
    --db $DB_NAME \
    --collection DANH_SACH_API_23 \
    --jsonArray \
    < "$SCRIPT_DIR/DANH_SACH_API_23.json"

echo "Importing CORP..."
docker exec -i $CONTAINER_NAME mongoimport \
    --username admin \
    --password password \
    --authenticationDatabase admin \
    --db $DB_NAME \
    --collection CORP \
    --jsonArray \
    < "$SCRIPT_DIR/CORP.json"

echo "Importing CORP_ACCT..."
docker exec -i $CONTAINER_NAME mongoimport \
    --username admin \
    --password password \
    --authenticationDatabase admin \
    --db $DB_NAME \
    --collection CORP_ACCT \
    --jsonArray \
    < "$SCRIPT_DIR/CORP_ACCT.json"

echo ""
echo "============================================================"
echo "Import completed!"
echo "============================================================"
echo ""
echo "To verify the data, run:"
echo "  docker exec -it $CONTAINER_NAME mongosh -u admin -p password --authenticationDatabase admin $DB_NAME"
echo ""
echo "Then run queries like:"
echo "  db.T24_T24CORE_CUSTOMER.countDocuments()"
echo "  db.T24_T24CORE_ACCOUNT.countDocuments()"
