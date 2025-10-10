"""
Script to generate MongoDB test data based on SQL query structure
Generates approximately 1000 records for each collection
"""

import random
import json
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker with Vietnamese locale
fake = Faker(['vi_VN'])
Faker.seed(42)
random.seed(42)

# Vietnamese business name components
BUSINESS_TYPES = ['CÔNG TY TNHH', 'CÔNG TY CP', 'CÔNG TY CỔ PHẦN', 'CÔNG TY ĐẦU TƯ', 'CÔNG TY']
BUSINESS_FIELDS = ['XÂY DỰNG', 'THƯƠNG MẠI', 'SẢN XUẤT', 'DỊCH VỤ', 'ĐẦU TƯ', 'CÔNG NGHỆ',
                   'VẬN TẢI', 'DU LỊCH', 'GIÁO DỤC', 'Y TẾ', 'NÔNG NGHIỆP', 'THỰC PHẨM']
KHOI_VALUES = ['SME', 'FI', 'CIB', 'DVC']
ID_TYPES = ['CCCD', 'HO.CHIEU', 'CMTND', 'KHAC']
GENDERS = ['MALE', 'FEMALE']

def random_date(start_year=1990, end_year=2020):
    """Generate random date in YYYYMMDD format"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    random_date = start + timedelta(days=random.randint(0, (end - start).days))
    return random_date.strftime('%Y%m%d')

def random_phone():
    """Generate Vietnamese phone number"""
    prefixes = ['090', '091', '093', '094', '097', '098', '086', '096', '032', '033', '034', '035', '036', '037', '038', '039']
    return f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"

def generate_business_name():
    """Generate Vietnamese business name"""
    return f"{random.choice(BUSINESS_TYPES)} {random.choice(BUSINESS_FIELDS)} {fake.last_name().upper()}"

def generate_tax_code():
    """Generate Vietnamese tax code (10 digits)"""
    return f"{random.randint(1000000000, 9999999999)}"

def generate_license_code():
    """Generate business license code"""
    return f"{random.randint(100000000, 999999999)}"

def generate_customer_id():
    """Generate customer ID (CIF)"""
    return f"CUS{random.randint(100000, 999999)}"

def generate_account_id():
    """Generate account ID"""
    return f"{random.randint(1000000000, 9999999999)}"

def generate_representative_data():
    """Generate representative person data (can have multiple representatives separated by #)"""
    num_reps = random.choices([1, 2, 3], weights=[70, 25, 5])[0]

    names = []
    id_nums = []
    id_types = []
    birth_days = []
    genders = []
    phones = []

    for _ in range(num_reps):
        gender = random.choice(GENDERS)
        if gender == 'MALE':
            name = fake.name_male()
        else:
            name = fake.name_female()

        names.append(name.upper())
        id_types.append(random.choice(ID_TYPES))
        id_nums.append(f"{random.randint(100000000000, 999999999999)}")
        birth_days.append(random_date(1960, 1995))
        genders.append(gender)
        phones.append(random_phone())

    return {
        'REP_NAME': '#'.join(names),
        'REP_ID_NUM': '#'.join(id_nums),
        'REP_ID_TYPE': '#'.join(id_types),
        'REP_BIRTH_DAY': '#'.join(birth_days),
        'REP_GENDER': '#'.join(genders),
        'REP_PHONE': '#'.join(phones)
    }

def generate_customers(num_records=1000):
    """Generate T24_T24CORE_CUSTOMER collection data"""
    customers = []
    customer_ids = []

    for i in range(num_records):
        cus_id = generate_customer_id()
        customer_ids.append(cus_id)

        rep_data = generate_representative_data()
        birth_date = random_date(1980, 2020)

        customer = {
            'ID': cus_id,
            'VN_FULL_NAME': generate_business_name(),
            'ESTAB_LIC_CODE': generate_license_code(),
            'BIRTH_INCORP_DATE': birth_date if random.random() > 0.3 else None,
            'ESTAB_ISS_DATE': random_date(1990, 2023),
            'MST_ADDRESS': fake.address() if random.random() > 0.2 else None,
            'VN_FULL_ADDRESS': fake.address(),
            'KHOI': random.choice(KHOI_VALUES),
            **rep_data
        }
        customers.append(customer)

    return customers, customer_ids

def generate_accounts(customer_ids, num_records=1000):
    """Generate T24_T24CORE_ACCOUNT collection data"""
    accounts = []
    account_ids = []

    # Ensure we have at least as many accounts as customers
    for i in range(num_records):
        acc_id = generate_account_id()
        account_ids.append(acc_id)

        # Randomly select a customer
        customer_id = random.choice(customer_ids)

        # 80% of accounts have no locked amount (active)
        locked_amount = 0 if random.random() > 0.2 else random.randint(1000000, 100000000)

        account = {
            'ID': acc_id,
            'CUSTOMER': customer_id,
            'OPENING_DATE': random_date(2010, 2024),
            'LOCKED_AMOUNT': locked_amount,
            'BALANCE': random.randint(10000000, 5000000000),
            'CURRENCY': 'VND',
            'ACCOUNT_TYPE': random.choice(['SAVING', 'CURRENT', 'FIXED_DEPOSIT'])
        }
        accounts.append(account)

    return accounts, account_ids

def generate_danh_sach_api(customer_ids):
    """Generate DANH_SACH_API_23 collection data"""
    danh_sach = []

    for cus_id in customer_ids:
        danh_sach.append({
            'MAKH': cus_id,
            'API_VERSION': '23',
            'CREATED_DATE': random_date(2023, 2024),
            'STATUS': random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'INACTIVE'])
        })

    return danh_sach

def generate_corp_and_corp_acct(account_ids, num_corps=500):
    """Generate CORP and CORP_ACCT collections"""
    corps = []
    corp_accts = []

    for i in range(num_corps):
        corp_id = f"CORP{random.randint(100000, 999999)}"

        corp = {
            'ID': corp_id,
            'CORP_NAME': generate_business_name(),
            'TAX_CODE': generate_tax_code(),
            'IS_DELETE': 'N',
            'CREATED_DATE': random_date(2015, 2024),
            'STATUS': random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'SUSPENDED'])
        }
        corps.append(corp)

        # Each corp can have 1-3 accounts
        num_accounts = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        selected_accounts = random.sample(account_ids, min(num_accounts, len(account_ids)))

        for acct_no in selected_accounts:
            corp_acct = {
                'CORP_ID': corp_id,
                'ACCT_NO': acct_no,
                'ACCT_ROLE': random.choice(['PRIMARY', 'SECONDARY']),
                'CREATED_DATE': random_date(2015, 2024)
            }
            corp_accts.append(corp_acct)

    return corps, corp_accts

def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved {len(data)} records to {filename}")

def generate_mongodb_import_script(collections):
    """Generate MongoDB import script"""
    script_lines = [
        "#!/bin/bash",
        "# MongoDB Import Script",
        "# Run this script to import all generated data into MongoDB",
        "",
        "# Database name",
        "DB_NAME='banking_db'",
        "",
        "echo 'Starting MongoDB data import...'",
        ""
    ]

    for collection_name, filename in collections.items():
        script_lines.append(f"echo 'Importing {collection_name}...'")
        script_lines.append(
            f"mongoimport --db $DB_NAME --collection {collection_name} "
            f"--file {filename} --jsonArray"
        )
        script_lines.append("")

    script_lines.append("echo 'Import completed!'")

    return "\n".join(script_lines)

def main():
    print("=" * 60)
    print("MongoDB Data Generator for Banking System")
    print("=" * 60)
    print()

    # Generate customers
    print("Generating T24_T24CORE_CUSTOMER data...")
    customers, customer_ids = generate_customers(1000)
    save_to_json(customers, 'T24_T24CORE_CUSTOMER.json')

    # Generate accounts
    print("Generating T24_T24CORE_ACCOUNT data...")
    accounts, account_ids = generate_accounts(customer_ids, 1000)
    save_to_json(accounts, 'T24_T24CORE_ACCOUNT.json')

    # Generate DANH_SACH_API_23
    print("Generating DANH_SACH_API_23 data...")
    danh_sach = generate_danh_sach_api(customer_ids)
    save_to_json(danh_sach, 'DANH_SACH_API_23.json')

    # Generate CORP and CORP_ACCT
    print("Generating CORP and CORP_ACCT data...")
    corps, corp_accts = generate_corp_and_corp_acct(account_ids, 500)
    save_to_json(corps, 'CORP.json')
    save_to_json(corp_accts, 'CORP_ACCT.json')

    # Generate import script
    print("\nGenerating MongoDB import script...")
    collections = {
        'T24_T24CORE_CUSTOMER': 'T24_T24CORE_CUSTOMER.json',
        'T24_T24CORE_ACCOUNT': 'T24_T24CORE_ACCOUNT.json',
        'DANH_SACH_API_23': 'DANH_SACH_API_23.json',
        'CORP': 'CORP.json',
        'CORP_ACCT': 'CORP_ACCT.json'
    }

    import_script = generate_mongodb_import_script(collections)
    with open('import_to_mongodb.sh', 'w', encoding='utf-8') as f:
        f.write(import_script)
    print("[OK] Saved MongoDB import script to import_to_mongodb.sh")

    # Generate Windows batch script
    batch_script = "@echo off\n"
    batch_script += "REM MongoDB Import Script for Windows\n"
    batch_script += "SET DB_NAME=banking_db\n\n"
    batch_script += "echo Starting MongoDB data import...\n\n"

    for collection_name, filename in collections.items():
        batch_script += f"echo Importing {collection_name}...\n"
        batch_script += f"mongoimport --db %DB_NAME% --collection {collection_name} --file {filename} --jsonArray\n\n"

    batch_script += "echo Import completed!\npause\n"

    with open('import_to_mongodb.bat', 'w', encoding='utf-8') as f:
        f.write(batch_script)
    print("[OK] Saved Windows batch script to import_to_mongodb.bat")

    print("\n" + "=" * 60)
    print("Data generation completed!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - T24_T24CORE_CUSTOMER.json (1000 records)")
    print("  - T24_T24CORE_ACCOUNT.json (1000 records)")
    print("  - DANH_SACH_API_23.json (1000 records)")
    print("  - CORP.json (500 records)")
    print("  - CORP_ACCT.json (~1000 records)")
    print("  - import_to_mongodb.sh (Linux/Mac import script)")
    print("  - import_to_mongodb.bat (Windows import script)")
    print("\nTo import data into MongoDB:")
    print("  Linux/Mac: bash import_to_mongodb.sh")
    print("  Windows:   import_to_mongodb.bat")
    print()

if __name__ == "__main__":
    main()
