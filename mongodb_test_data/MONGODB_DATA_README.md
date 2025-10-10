# MongoDB Test Data Generator

This project generates test data for a banking system based on a T24 Oracle SQL query structure, converted to MongoDB collections.

## Generated Data Overview

The script generates approximately **1000 records** for each main collection:

### Collections Generated

1. **T24_T24CORE_CUSTOMER** (1000 records)
   - Customer information (Vietnamese businesses)
   - Representative details (name, ID, birth date, gender, phone)
   - Company addresses and establishment information
   - Supports multiple representatives (separated by #)

2. **T24_T24CORE_ACCOUNT** (1000 records)
   - Bank account information linked to customers
   - Account opening dates, balances, locked amounts
   - Account types: SAVING, CURRENT, FIXED_DEPOSIT

3. **DANH_SACH_API_23** (1000 records)
   - API access list for customers
   - Tracks API version 23 access status

4. **CORP** (500 records)
   - Corporate entity information
   - Tax codes, business names
   - Deletion flags and status tracking

5. **CORP_ACCT** (~748 records)
   - Links corporate entities to bank accounts
   - Relationship table between CORP and T24_T24CORE_ACCOUNT

## Data Characteristics

### Vietnamese Business Data
- **Business Names**: Realistic Vietnamese company names (CÔNG TY TNHH, CÔNG TY CP, etc.)
- **Business Fields**: Construction, Trading, Manufacturing, Services, Investment, Technology, etc.
- **Phone Numbers**: Valid Vietnamese mobile prefixes (090, 091, 093, 094, etc.)
- **Tax Codes**: 10-digit Vietnamese tax identification numbers
- **License Codes**: 9-digit business license numbers
- **KHOI Values**: SME, FI, CIB, DVC (business segments)

### Representative Data
- Multiple representatives per customer (1-3 people, weighted 70%/25%/5%)
- ID Types: CCCD (Citizen ID), CMTND (Old ID), HO.CHIEU (Passport), KHAC (Other)
- Gender: MALE/FEMALE
- Birth dates: 1960-1995 for representatives

### Account Data
- 80% active accounts (LOCKED_AMOUNT = 0)
- 20% have locked amounts (frozen/restricted)
- Opening dates: 2010-2024
- Balances: 10,000,000 - 5,000,000,000 VND

## SQL to MongoDB Mapping

The original SQL query structure maps to MongoDB as follows:

| SQL Table | MongoDB Collection | Purpose |
|-----------|-------------------|---------|
| T24_T24CORE_CUSTOMER | T24_T24CORE_CUSTOMER | Customer master data |
| T24_T24CORE_ACCOUNT | T24_T24CORE_ACCOUNT | Account information |
| DANH_SACH_API_23 | DANH_SACH_API_23 | API access list |
| BIZ.CORP | CORP | Corporate entities |
| BIZ.CORP_ACCT | CORP_ACCT | Corp-Account relationships |

### Key Fields from SQL Query

```sql
-- Customer fields
cus.ID AS Cif
cus.VN_FULL_NAME AS TenToChuc
cus.ESTAB_LIC_CODE AS SoGiayPhepThanhLap

-- Representative fields (supports multiple with # separator)
REGEXP_SUBSTR(cus.REP_NAME, '[^#]+', 1, 1) AS HoTenNguoiDaiDien
REGEXP_SUBSTR(cus.REP_ID_NUM, '[^#]+', 1, 1) AS SoGiayToTuyThan
REGEXP_SUBSTR(cus.REP_ID_TYPE, '[^#]+', 1, 1) AS LoaiGiayToTuyThan

-- Account fields
acc.ID AS SoTaiKhoanToChuc
acc.LOCKED_AMOUNT AS TrangThaiTaiKhoan
```

## Installation & Usage

### Prerequisites
- Python 3.8+
- MongoDB server running locally or remotely

### Step 1: Generate Data

The data has already been generated. If you need to regenerate:

```bash
python generate_mongodb_data.py
```

### Step 2: Import to MongoDB

#### On Windows:
```bash
import_to_mongodb.bat
```

#### On Linux/Mac:
```bash
bash import_to_mongodb.sh
```

#### Manual Import:
```bash
# Set your database name
DB_NAME="banking_db"

# Import each collection
mongoimport --db $DB_NAME --collection T24_T24CORE_CUSTOMER --file T24_T24CORE_CUSTOMER.json --jsonArray
mongoimport --db $DB_NAME --collection T24_T24CORE_ACCOUNT --file T24_T24CORE_ACCOUNT.json --jsonArray
mongoimport --db $DB_NAME --collection DANH_SACH_API_23 --file DANH_SACH_API_23.json --jsonArray
mongoimport --db $DB_NAME --collection CORP --file CORP.json --jsonArray
mongoimport --db $DB_NAME --collection CORP_ACCT --file CORP_ACCT.json --jsonArray
```

## Sample Data Structures

### T24_T24CORE_CUSTOMER Sample
```json
{
  "ID": "CUS123456",
  "VN_FULL_NAME": "CÔNG TY TNHH XÂY DỰNG NGUYỄN",
  "ESTAB_LIC_CODE": "123456789",
  "BIRTH_INCORP_DATE": "20150315",
  "ESTAB_ISS_DATE": "20150310",
  "MST_ADDRESS": "123 Nguyễn Văn Cừ, Quận 5, TP.HCM",
  "VN_FULL_ADDRESS": "123 Nguyễn Văn Cừ, Quận 5, TP.HCM",
  "KHOI": "SME",
  "REP_NAME": "NGUYỄN VĂN A#TRẦN THỊ B",
  "REP_ID_NUM": "001234567890#009876543210",
  "REP_ID_TYPE": "CCCD#CMTND",
  "REP_BIRTH_DAY": "19750612#19800315",
  "REP_GENDER": "MALE#FEMALE",
  "REP_PHONE": "0901234567#0912345678"
}
```

### T24_T24CORE_ACCOUNT Sample
```json
{
  "ID": "1234567890",
  "CUSTOMER": "CUS123456",
  "OPENING_DATE": "20200115",
  "LOCKED_AMOUNT": 0,
  "BALANCE": 125000000,
  "CURRENCY": "VND",
  "ACCOUNT_TYPE": "CURRENT"
}
```

### CORP Sample
```json
{
  "ID": "CORP123456",
  "CORP_NAME": "CÔNG TY CP SẢN XUẤT LÊ",
  "TAX_CODE": "1234567890",
  "IS_DELETE": "N",
  "CREATED_DATE": "20180520",
  "STATUS": "ACTIVE"
}
```

### CORP_ACCT Sample
```json
{
  "CORP_ID": "CORP123456",
  "ACCT_NO": "1234567890",
  "ACCT_ROLE": "PRIMARY",
  "CREATED_DATE": "20180520"
}
```

## Query Examples

### Find customers with their accounts
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

### Find accounts with locked amounts
```javascript
db.T24_T24CORE_ACCOUNT.find({
  LOCKED_AMOUNT: { $gt: 0 }
})
```

### Find customers in SME segment
```javascript
db.T24_T24CORE_CUSTOMER.find({
  KHOI: "SME"
})
```

### Join CORP with accounts
```javascript
db.CORP_ACCT.aggregate([
  {
    $lookup: {
      from: "CORP",
      localField: "CORP_ID",
      foreignField: "ID",
      as: "corp_info"
    }
  },
  {
    $lookup: {
      from: "T24_T24CORE_ACCOUNT",
      localField: "ACCT_NO",
      foreignField: "ID",
      as: "account_info"
    }
  },
  { $match: { "corp_info.IS_DELETE": "N" } }
])
```

### Replicate the original SQL query in MongoDB
```javascript
db.T24_T24CORE_ACCOUNT.aggregate([
  // Join with customer
  {
    $lookup: {
      from: "T24_T24CORE_CUSTOMER",
      localField: "CUSTOMER",
      foreignField: "ID",
      as: "customer"
    }
  },
  { $unwind: "$customer" },

  // Join with API list
  {
    $lookup: {
      from: "DANH_SACH_API_23",
      localField: "customer.ID",
      foreignField: "MAKH",
      as: "api_list"
    }
  },
  { $unwind: { path: "$api_list", preserveNullAndEmptyArrays: false } },

  // Join with CORP_ACCT
  {
    $lookup: {
      from: "CORP_ACCT",
      localField: "ID",
      foreignField: "ACCT_NO",
      as: "corp_acct"
    }
  },

  // Filter by KHOI
  { $match: { "customer.KHOI": { $in: ["SME", "FI", "CIB", "DVC"] } } },

  // Project fields
  {
    $project: {
      Cif: "$customer.ID",
      TenToChuc: "$customer.VN_FULL_NAME",
      SoGiayPhepThanhLap: "$customer.ESTAB_LIC_CODE",
      LoaiGiayToThanhLapToChuc: "1",
      NgayThanhLap: {
        $dateToString: {
          format: "%d/%m/%Y",
          date: {
            $dateFromString: {
              dateString: {
                $ifNull: ["$customer.BIRTH_INCORP_DATE", "$customer.ESTAB_ISS_DATE"]
              },
              format: "%Y%m%d"
            }
          }
        }
      },
      DiaChiToChuc: {
        $ifNull: ["$customer.MST_ADDRESS", "$customer.VN_FULL_ADDRESS"]
      },
      HoTenNguoiDaiDien: {
        $arrayElemAt: [{ $split: ["$customer.REP_NAME", "#"] }, 0]
      },
      SoGiayToTuyThan: {
        $arrayElemAt: [{ $split: ["$customer.REP_ID_NUM", "#"] }, 0]
      },
      SoTaiKhoanToChuc: "$ID",
      TrangThaiTaiKhoan: "$LOCKED_AMOUNT"
    }
  }
])
```

## Data Statistics

- **Total Customers**: 1,000
- **Total Accounts**: 1,000
- **Total Corporate Entities**: 500
- **Total Corp-Account Links**: ~748
- **API Access Records**: 1,000

### Distribution
- **KHOI Distribution**: Equal distribution across SME, FI, CIB, DVC
- **Account Status**: 80% active, 20% with locked amounts
- **ID Types**: CCCD, CMTND, HO.CHIEU, KHAC (randomly distributed)
- **Representatives per Customer**: 70% have 1, 25% have 2, 5% have 3

## Notes

1. **Multiple Representatives**: The data supports multiple representatives per customer, with fields separated by "#" character, matching the Oracle REGEXP_SUBSTR pattern in the original SQL.

2. **Date Format**: Dates are stored in YYYYMMDD format in MongoDB (matching T24 format), but can be converted to DD/MM/YYYY format in queries as shown in examples.

3. **Relationships**:
   - One customer can have multiple accounts
   - One corporate entity can have multiple accounts
   - Account-Customer relationship is maintained via CUSTOMER field

4. **Data Consistency**: All foreign key relationships are maintained properly for testing purposes.

## Customization

To modify the data generation:

1. Edit [generate_mongodb_data.py](generate_mongodb_data.py)
2. Adjust the following parameters:
   - `generate_customers(num_records=1000)` - change number of customers
   - `generate_accounts(customer_ids, num_records=1000)` - change number of accounts
   - `generate_corp_and_corp_acct(account_ids, num_corps=500)` - change number of corps
3. Modify business name components, phone prefixes, or other Vietnamese-specific data
4. Re-run the script to generate new data

## License

This is a test data generator for development and testing purposes only.
