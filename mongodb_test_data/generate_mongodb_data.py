from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient
import random

# ===============================================
# Original generator functions (your code)
# ===============================================
fake = Faker(['vi_VN'])
Faker.seed(42)
random.seed(42)

BUSINESS_TYPES = ['CÔNG TY TNHH', 'CÔNG TY CP', 'CÔNG TY CỔ PHẦN', 'CÔNG TY ĐẦU TƯ', 'CÔNG TY']
BUSINESS_FIELDS = ['XÂY DỰNG', 'THƯƠNG MẠI', 'SẢN XUẤT', 'DỊCH VỤ', 'ĐẦU TƯ', 'CÔNG NGHỆ',
                   'VẬN TẢI', 'DU LỊCH', 'GIÁO DỤC', 'Y TẾ', 'NÔNG NGHIỆP', 'THỰC PHẨM']
KHOI_VALUES = ['SME', 'FI', 'CIB', 'DVC']
ID_TYPES = ['CCCD', 'HO.CHIEU', 'CMTND', 'KHAC']
GENDERS = ['MALE', 'FEMALE']

def random_date(start_year=1990, end_year=2020):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    random_date = start + timedelta(days=random.randint(0, (end - start).days))
    return random_date.strftime('%Y%m%d')

def random_phone():
    prefixes = ['090', '091', '093', '094', '097', '098', '086', '096', '032', '033', '034', '035', '036', '037', '038', '039']
    return f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"

def generate_business_name():
    return f"{random.choice(BUSINESS_TYPES)} {random.choice(BUSINESS_FIELDS)} {fake.last_name().upper()}"

def generate_tax_code():
    return f"{random.randint(1000000000, 9999999999)}"

def generate_license_code():
    return f"{random.randint(100000000, 999999999)}"

def generate_customer_id():
    return f"CUS{random.randint(100000, 999999)}"

def generate_account_id():
    return f"{random.randint(1000000000, 9999999999)}"

def generate_representative_data():
    num_reps = random.choices([1, 2, 3], weights=[70, 25, 5])[0]

    names, id_nums, id_types, birth_days, genders, phones = [], [], [], [], [], []
    for _ in range(num_reps):
        gender = random.choice(GENDERS)
        name = fake.name_male() if gender == 'MALE' else fake.name_female()
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
    customers, customer_ids = [], []
    for _ in range(num_records):
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
    accounts, account_ids = [], []
    for _ in range(num_records):
        acc_id = generate_account_id()
        account_ids.append(acc_id)
        customer_id = random.choice(customer_ids)
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
    corps, corp_accts = [], []
    for _ in range(num_corps):
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

        num_accounts = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        selected_accounts = random.sample(account_ids, min(num_accounts, len(account_ids)))
        for acct_no in selected_accounts:
            corp_accts.append({
                'CORP_ID': corp_id,
                'ACCT_NO': acct_no,
                'ACCT_ROLE': random.choice(['PRIMARY', 'SECONDARY']),
                'CREATED_DATE': random_date(2015, 2024)
            })
    return corps, corp_accts

# ===============================================
# MongoDB Insertion
# ===============================================

if __name__ == "__main__":
    client = MongoClient("mongodb://admin:password@localhost:27017/")
    db = client["ods"]

    print("Generating fake data...")
    customers, customer_ids = generate_customers(1000)
    accounts, account_ids = generate_accounts(customer_ids, 1500)
    danh_sach = generate_danh_sach_api(customer_ids)
    corps, corp_accts = generate_corp_and_corp_acct(account_ids, 400)

    print("Inserting into MongoDB...")
    # db.T24_T24CORE_CUSTOMER.insert_many(customers)
    # db.T24_T24CORE_ACCOUNT.insert_many(accounts)
    # db.EXCEL.insert_many(danh_sach)
    # db.BIZ_CORP.insert_many(corps)
    # db.BIZ_CORP_ACCT.insert_many(corp_accts)

    print("✅ Data insertion completed successfully!")
