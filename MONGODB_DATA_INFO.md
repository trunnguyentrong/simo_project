# MongoDB Test Data - Hướng dẫn nhanh

Tất cả dữ liệu MongoDB test đã được tổ chức trong folder: **[mongodb_test_data](mongodb_test_data/)**

## Nội dung

Folder chứa:
- 5 file JSON với tổng cộng ~3,250 records
- Scripts để import vào MongoDB
- Script Python để tạo lại dữ liệu
- Tài liệu chi tiết

## Cách sử dụng

### 1. Start MongoDB (Docker)

```bash
docker-compose up -d mongodb
```

### 2. Import dữ liệu vào MongoDB

**Docker MongoDB (Khuyến nghị):**

Windows:
```bash
cd mongodb_test_data
import_to_docker_mongodb.bat
```

Linux/Mac:
```bash
cd mongodb_test_data
bash import_to_docker_mongodb.sh
```

**MongoDB Local:**

Windows:
```bash
cd mongodb_test_data
import_to_mongodb.bat
```

Linux/Mac:
```bash
cd mongodb_test_data
bash import_to_mongodb.sh
```

### 3. Xem tài liệu chi tiết

- [mongodb_test_data/README.md](mongodb_test_data/README.md) - Hướng dẫn nhanh (Tiếng Việt)
- [mongodb_test_data/MONGODB_DATA_README.md](mongodb_test_data/MONGODB_DATA_README.md) - Tài liệu đầy đủ (English)

### 4. Tạo lại dữ liệu mới

```bash
cd mongodb_test_data
python generate_mongodb_data.py
```

## Collections được tạo

| Collection | Records | Mô tả |
|------------|---------|-------|
| T24_T24CORE_CUSTOMER | 1,000 | Khách hàng doanh nghiệp |
| T24_T24CORE_ACCOUNT | 1,000 | Tài khoản ngân hàng |
| DANH_SACH_API_23 | 1,000 | Danh sách API |
| CORP | 500 | Tổ chức pháp nhân |
| CORP_ACCT | ~748 | Liên kết tổ chức-tài khoản |

## Thông tin MongoDB

**Connection từ Docker:**
```
mongodb://admin:password@mongodb:27017
```

**Connection từ Host:**
```
mongodb://admin:password@localhost:27017
```

**Database:** `banking_db`

Xem hướng dẫn chi tiết: [MONGODB_SETUP.md](MONGODB_SETUP.md)

---

Xem chi tiết trong folder [mongodb_test_data](mongodb_test_data/)
