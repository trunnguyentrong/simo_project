# Data Processing System with Kong API Gateway

Hệ thống xử lý dữ liệu hoàn chỉnh với kiến trúc microservices, bao gồm:
- **Frontend**: Giao diện upload file Excel
- **Kong API Gateway**: Enterprise-grade API Gateway
- **Backend**: Xử lý dữ liệu với FastAPI
- **MinIO**: Lưu trữ file
- **MongoDB**: Database cho reference data
- **PostgreSQL**: Database cho Kong

## 🏗️ Kiến trúc hệ thống

```
┌─────────────┐
│  Frontend   │ (Port 3000)
│  (Nginx)    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐         ┌──────────────┐
│  Kong Gateway   │────────▶│  PostgreSQL  │
│   (Port 8000)   │         │  (Kong DB)   │
└──────┬──────────┘         └──────────────┘
       │
       ▼
┌─────────────────┐         ┌─────────────┐
│    Backend      │────────▶│   MinIO     │ (Port 9000)
│   (FastAPI)     │         │  (Storage)  │
└────┬────────────┘         └─────────────┘
     │
     ▼
┌─────────────┐         ┌─────────────────┐
│  MongoDB    │         │  External API   │
│ (Database)  │         │  (Third-party)  │
└─────────────┘         └─────────────────┘
     Port 27017
```

## 🔄 Luồng xử lý dữ liệu

1. **Upload**: Frontend → Kong Gateway → Backend → MinIO
2. **Process**:
   - Backend lấy file từ MinIO
   - Parse Excel data
   - Join với data từ MongoDB
   - Gửi kết quả đến External API
   - Lưu processed data vào MongoDB

## 🚀 Kong API Gateway

### Vai trò của Kong:

1. **Enterprise-grade Gateway**: Production-ready, scalable
2. **Routing**: Route requests đến backend services
3. **Load Balancing**: Phân tải tự động
4. **Plugins Ecosystem**:
   - CORS
   - Rate Limiting
   - Authentication (JWT, OAuth2, API Key)
   - Logging & Monitoring (Prometheus)
   - Request/Response Transformation
5. **Admin UI**: Kong Manager trên port 8002
6. **High Performance**: Written in Lua/Nginx

### Kong Features Enabled:

- ✅ **CORS**: Allow all origins
- ✅ **Request Size Limiting**: 100MB for file uploads
- ✅ **Prometheus Metrics**: Monitoring integration
- 🔧 **Extensible**: Add plugins easily via `kong.yaml`

## 📋 Yêu cầu

- Docker & Docker Compose

## 🛠️ Cài đặt và chạy

### 1. Clone và setup

```bash
cd vibe_coding
cp .env.example .env
```

### 2. Chỉnh sửa file .env (optional)

```env
EXTERNAL_API_URL=https://your-external-api.com/endpoint
EXTERNAL_API_KEY=your-actual-api-key
```

### 3. Khởi động hệ thống

```bash
docker-compose up -d
```

**Services:**
- Frontend: http://localhost:3000
- Kong Gateway: http://localhost:8000
- Kong Manager UI: http://localhost:8002
- Kong Admin API: http://localhost:8001
- MinIO Console: http://localhost:9001

### 4. Seed MongoDB (optional)

```bash
pip install pymongo
python scripts/seed_mongodb.py
```

## 📝 Sử dụng

### Via Frontend UI

1. Truy cập http://localhost:3000
2. Upload Excel file (.xlsx, .xls)
3. Click "Upload File"
4. Click "Process Data"

### Via API

```bash
# Upload file
curl -X POST http://localhost:8000/api/upload \
  -F "file=@sample_data/sample_upload.xlsx"

# Process file
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{"file_id": "your-file-id"}'
```

## 🔧 Kong Configuration

### Routes:

| Route | Method | Backend | Description |
|-------|--------|---------|-------------|
| `/api/upload` | POST | `/upload/` | Upload file |
| `/api/process` | POST | `/process/` | Process data |
| `/api/health` | GET | `/health/` | Health check |

### Kong Admin API:

```bash
# List services
curl http://localhost:8001/services

# List routes
curl http://localhost:8001/routes

# List plugins
curl http://localhost:8001/plugins
```

### Kong Manager UI:

Visit http://localhost:8002 để quản lý Kong qua giao diện web.

## 🔌 Thêm Kong Plugins

Edit `kong/kong.yaml`:

```yaml
plugins:
  - name: rate-limiting
    config:
      minute: 100
      policy: local

  - name: jwt
    config:
      secret_is_base64: false
```

Sau đó:
```bash
docker-compose restart kong-config
```

## 📊 Monitoring

Kong Prometheus metrics:
```bash
curl http://localhost:8001/metrics
```

## 🐛 Troubleshooting

```bash
# Check logs
docker-compose logs -f kong
docker-compose logs -f backend

# Restart services
docker-compose restart kong
docker-compose restart backend

# Rebuild
docker-compose down
docker-compose up -d --build
```

## 🚀 Production Tips

1. **Security**:
   - Enable JWT/OAuth2 authentication
   - Setup rate limiting
   - Configure IP restrictions
   - Use HTTPS

2. **Scaling**:
   ```bash
   docker-compose up -d --scale backend=3
   ```

3. **Monitoring**:
   - Setup Prometheus + Grafana
   - Enable Kong Vitals (Enterprise)
   - Centralized logging

## 📁 Cấu trúc

```
vibe_coding/
├── frontend/           # UI
├── kong/              # Kong config
│   └── kong.yaml
├── backend/           # FastAPI service
├── docker-compose.yml
└── README.md
```

## 📄 License

MIT
