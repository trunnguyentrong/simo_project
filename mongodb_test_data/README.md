# MongoDB Test Data - Banking System

Dữ liệu test cho hệ thống ngân hàng dựa trên cấu trúc SQL T24, chuyển đổi sang MongoDB.

## Nội dung Folder

### Dữ liệu JSON (1000 records mỗi collection)
- `T24_T24CORE_CUSTOMER.json` - Thông tin khách hàng doanh nghiệp
- `T24_T24CORE_ACCOUNT.json` - Thông tin tài khoản ngân hàng
- `DANH_SACH_API_23.json` - Danh sách truy cập API
- `CORP.json` - Thông tin tổ chức pháp nhân (500 records)
- `CORP_ACCT.json` - Liên kết tổ chức-tài khoản (~748 records)

### Scripts
- `generate_mongodb_data.py` - Script Python để tạo dữ liệu mới
- `import_to_docker_mongodb.bat` - Script import vào Docker MongoDB (Windows)
- `import_to_docker_mongodb.sh` - Script import vào Docker MongoDB (Linux/Mac)
- `import_to_mongodb.bat` - Script import vào MongoDB local (Windows)
- `import_to_mongodb.sh` - Script import vào MongoDB local (Linux/Mac)

### Tài liệu
- `MONGODB_DATA_README.md` - Tài liệu chi tiết đầy đủ
- `README.md` - File này (hướng dẫn nhanh)

## Cách Import Dữ liệu vào MongoDB

### Option 1: Import vào MongoDB trong Docker (Khuyến nghị)

**Bước 1: Start MongoDB container**
```bash
docker-compose up -d mongodb
```

**Bước 2: Import dữ liệu**

**Windows:**
```bash
cd mongodb_test_data
import_to_docker_mongodb.bat
```

**Linux/Mac:**
```bash
cd mongodb_test_data
bash import_to_docker_mongodb.sh
```

### Option 2: Import vào MongoDB local

**Windows:**
```bash
cd mongodb_test_data
import_to_mongodb.bat
```

**Linux/Mac:**
```bash
cd mongodb_test_data
bash import_to_mongodb.sh
```

### Option 3: Import thủ công
```bash
cd mongodb_test_data

# Đặt tên database
DB_NAME="banking_db"

# Import từng collection
mongoimport --db $DB_NAME --collection T24_T24CORE_CUSTOMER --file T24_T24CORE_CUSTOMER.json --jsonArray
mongoimport --db $DB_NAME --collection T24_T24CORE_ACCOUNT --file T24_T24CORE_ACCOUNT.json --jsonArray
mongoimport --db $DB_NAME --collection DANH_SACH_API_23 --file DANH_SACH_API_23.json --jsonArray
mongoimport --db $DB_NAME --collection CORP --file CORP.json --jsonArray
mongoimport --db $DB_NAME --collection CORP_ACCT --file CORP_ACCT.json --jsonArray
```

## Tạo Lại Dữ liệu

Nếu muốn tạo lại dữ liệu mới:

```bash
cd mongodb_test_data
python generate_mongodb_data.py
```

## Đặc điểm Dữ liệu

### Khách hàng (T24_T24CORE_CUSTOMER)
- Tên doanh nghiệp Việt Nam thực tế
- Hỗ trợ nhiều người đại diện (phân tách bằng #)
- Số điện thoại Việt Nam hợp lệ
- Mã số thuế 10 chữ số
- KHOI: SME, FI, CIB, DVC

### Tài khoản (T24_T24CORE_ACCOUNT)
- 80% tài khoản hoạt động bình thường
- 20% có số tiền bị phong tỏa
- Số dư: 10,000,000 - 5,000,000,000 VND
- Loại: SAVING, CURRENT, FIXED_DEPOSIT

## Cấu trúc Dữ liệu Mẫu

### Customer
```json
{
  "ID": "CUS770487",
  "VN_FULL_NAME": "CÔNG TY ĐẦU TƯ XÂY DỰNG PHẠM",
  "ESTAB_LIC_CODE": "131994523",
  "KHOI": "SME",
  "REP_NAME": "NGUYỄN VĂN A#TRẦN THỊ B",
  "REP_ID_NUM": "001234567890#009876543210",
  "REP_ID_TYPE": "CCCD#CMTND",
  "REP_PHONE": "0901234567#0912345678"
}
```

### Account
```json
{
  "ID": "3452611933",
  "CUSTOMER": "CUS521315",
  "OPENING_DATE": "20170605",
  "LOCKED_AMOUNT": 0,
  "BALANCE": 493240056,
  "ACCOUNT_TYPE": "CURRENT"
}
```

## Query Ví dụ

### Tìm khách hàng với tài khoản
```javascript
db.T24_T24CORE_ACCOUNT.aggregate([
  {
    $lookup: {
      from: "T24_T24CORE_CUSTOMER",
      localField: "CUSTOMER",
      foreignField: "ID",
      as: "customer_info"
    }
  },
  { $unwind: "$customer_info" },
  { $limit: 10 }
])
```

### Tìm tài khoản bị phong tỏa
```javascript
db.T24_T24CORE_ACCOUNT.find({
  LOCKED_AMOUNT: { $gt: 0 }
})
```

### Tìm khách hàng trong phân khúc SME
```javascript
db.T24_T24CORE_CUSTOMER.find({
  KHOI: "SME"
})
```

## Thống kê

- **Tổng số khách hàng**: 1,000
- **Tổng số tài khoản**: 1,000
- **Tổng số tổ chức**: 500
- **Liên kết tổ chức-TK**: ~748
- **Bản ghi API**: 1,000

## Lưu ý

1. Dữ liệu này chỉ dùng cho mục đích phát triển và testing
2. Tất cả mối quan hệ foreign key được duy trì đúng
3. Định dạng ngày: YYYYMMDD (format T24)
4. Hỗ trợ nhiều người đại diện, phân tách bằng ký tự #

---

Xem file `MONGODB_DATA_README.md` để biết thêm chi tiết và ví dụ query phức tạp hơn.
