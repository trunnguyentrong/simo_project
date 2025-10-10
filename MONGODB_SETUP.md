# MongoDB Configuration - Hướng dẫn cấu hình

## Tổng quan

Project đã được cấu hình MongoDB với Docker Compose. Dưới đây là các thông tin cấu hình.

## Cấu hình MongoDB trong Docker

### Thông tin kết nối

**Từ bên trong Docker network:**
```
URL: mongodb://admin:password@mongodb:27017
Username: admin
Password: password
```

**Từ host machine (localhost):**
```
URL: mongodb://admin:password@localhost:27017
Username: admin
Password: password
Port: 27017
```

### Databases

1. **banking_db** - Database chứa dữ liệu test (3,250 records)
   - Collections: T24_T24CORE_CUSTOMER, T24_T24CORE_ACCOUNT, DANH_SACH_API_23, CORP, CORP_ACCT

2. **ecommerce** - Database mặc định cho ứng dụng (đã cấu hình trong backend_process)

## Docker Compose Configuration

MongoDB service đã được thêm vào [docker-compose.yml](docker-compose.yml):

```yaml
mongodb:
  image: mongo:7.0
  container_name: mongodb
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: password
  ports:
    - "27017:27017"
  volumes:
    - mongodb_data:/data/db
    - ./mongodb_test_data:/docker-entrypoint-initdb.d/data:ro
  networks:
    - app-network
  healthcheck:
    test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
    interval: 10s
    timeout: 5s
    retries: 5
```

## Services sử dụng MongoDB

### backend_process

Đã được cấu hình để kết nối MongoDB:

```yaml
environment:
  MONGODB_URL: mongodb://admin:password@mongodb:27017
depends_on:
  mongodb:
    condition: service_healthy
```

File cấu hình: [backend_process/app/config/settings.py](backend_process/app/config/settings.py)

```python
class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://admin:password@mongodb:27017"
    MONGODB_DB: str = "ecommerce"
```

## Cách sử dụng

### 1. Start MongoDB

```bash
# Start only MongoDB
docker-compose up -d mongodb

# Or start all services
docker-compose up -d
```

### 2. Import dữ liệu test

Xem hướng dẫn chi tiết tại: [mongodb_test_data/README.md](mongodb_test_data/README.md)

**Cách nhanh:**
```bash
cd mongodb_test_data
import_to_docker_mongodb.bat   # Windows
# hoặc
bash import_to_docker_mongodb.sh  # Linux/Mac
```

### 3. Kết nối vào MongoDB Shell

**Sử dụng Docker:**
```bash
docker exec -it mongodb mongosh -u admin -p password --authenticationDatabase admin
```

**Sử dụng MongoDB Compass:**
```
Connection String: mongodb://admin:password@localhost:27017
```

**Sử dụng Python/FastAPI:**
```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://admin:password@mongodb:27017")
db = client.banking_db
```

### 4. Verify dữ liệu

```bash
# Kết nối vào MongoDB shell
docker exec -it mongodb mongosh -u admin -p password --authenticationDatabase admin

# Chuyển sang database banking_db
use banking_db

# Kiểm tra số lượng documents
db.T24_T24CORE_CUSTOMER.countDocuments()    // Should return 1000
db.T24_T24CORE_ACCOUNT.countDocuments()     // Should return 1000
db.DANH_SACH_API_23.countDocuments()        // Should return 1000
db.CORP.countDocuments()                     // Should return 500
db.CORP_ACCT.countDocuments()                // Should return 748

# Xem dữ liệu mẫu
db.T24_T24CORE_CUSTOMER.findOne()
```

## Quản lý MongoDB

### Stop MongoDB
```bash
docker-compose stop mongodb
```

### Restart MongoDB
```bash
docker-compose restart mongodb
```

### View logs
```bash
docker-compose logs mongodb
docker-compose logs -f mongodb  # Follow logs
```

### Xóa dữ liệu và reset
```bash
# Stop và xóa container
docker-compose down mongodb

# Xóa volume (xóa tất cả dữ liệu)
docker volume rm simo_miciroservices_mongodb_data

# Start lại
docker-compose up -d mongodb

# Import lại dữ liệu
cd mongodb_test_data
import_to_docker_mongodb.bat   # hoặc .sh
```

### Backup dữ liệu
```bash
# Backup database
docker exec mongodb mongodump \
  -u admin -p password \
  --authenticationDatabase admin \
  --db banking_db \
  --out /data/db/backup

# Copy backup ra host
docker cp mongodb:/data/db/backup ./mongodb_backup
```

### Restore dữ liệu
```bash
# Copy backup vào container
docker cp ./mongodb_backup mongodb:/data/db/restore

# Restore database
docker exec mongodb mongorestore \
  -u admin -p password \
  --authenticationDatabase admin \
  --db banking_db \
  /data/db/restore/banking_db
```

## MongoDB Tools

### Sử dụng mongosh (MongoDB Shell)

```bash
# Kết nối
docker exec -it mongodb mongosh -u admin -p password --authenticationDatabase admin

# List databases
show dbs

# Switch database
use banking_db

# List collections
show collections

# Query examples
db.T24_T24CORE_CUSTOMER.find({ KHOI: "SME" }).limit(5)
db.T24_T24CORE_ACCOUNT.find({ LOCKED_AMOUNT: { $gt: 0 } })
```

### MongoDB Compass (GUI)

1. Download từ: https://www.mongodb.com/try/download/compass
2. Connection String: `mongodb://admin:password@localhost:27017`
3. Explore databases, collections, và run queries

## Troubleshooting

### Container không start
```bash
# Xem logs
docker-compose logs mongodb

# Kiểm tra port đã được sử dụng chưa
netstat -ano | findstr :27017   # Windows
lsof -i :27017                  # Linux/Mac
```

### Không kết nối được từ host
```bash
# Kiểm tra container đang chạy
docker ps | grep mongodb

# Kiểm tra network
docker network inspect simo_miciroservices_app-network

# Test connection
docker exec mongodb mongosh --eval "db.adminCommand('ping')"
```

### Import thất bại
```bash
# Kiểm tra container health
docker ps -a | grep mongodb

# Xem logs
docker-compose logs mongodb

# Kiểm tra files JSON tồn tại
ls mongodb_test_data/*.json
```

## Tài liệu liên quan

- [MongoDB Test Data](mongodb_test_data/README.md) - Hướng dẫn về dữ liệu test
- [Docker Compose](docker-compose.yml) - Cấu hình Docker
- [Backend Process Settings](backend_process/app/config/settings.py) - Cấu hình backend

## Resources

- MongoDB Documentation: https://docs.mongodb.com/
- Motor (Async Python Driver): https://motor.readthedocs.io/
- PyMongo: https://pymongo.readthedocs.io/
