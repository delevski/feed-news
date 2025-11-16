# Ori AI Developers AI Trends - API Documentation

## Overview

REST API for fetching trending AI/ML content from GitHub and Hugging Face.

## Quick Start

### 1. Start the API Server

```bash
./run_api.sh
```

The API will be available at: `http://localhost:5000`

### 2. Test the API

```bash
# Health check
curl http://localhost:5000/api/health

# Get daily news
curl "http://localhost:5000/api/news?range=daily&limit=30"
```

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check if the API is running

**Example:**
```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Ori AI Developers AI Trends API",
  "timestamp": "2025-11-16T10:00:00.000000"
}
```

---

### 2. Get All News

**Endpoint:** `GET /api/news`

**Description:** Fetch all trending AI/ML news (repos, papers, spaces)

**Query Parameters:**
- `range` (optional): `daily`, `weekly`, or `monthly` (default: `daily`)
- `limit` (optional): Number of items (default: 30, max: 100)

**Example:**
```bash
curl "http://localhost:5000/api/news?range=daily&limit=30"
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2025-11-16T10:00:00.000000",
  "time_range": "daily",
  "total_items": 95,
  "returned_items": 30,
  "data": {
    "github_repos": [...],
    "github_collections": [...],
    "papers": [...],
    "spaces": [...],
    "all_items": [...]
  },
  "stats": {
    "github_repos_count": 15,
    "papers_count": 10,
    "spaces_count": 5,
    "collections_count": 0
  }
}
```

---

### 3. Get Only GitHub Repos

**Endpoint:** `GET /api/news/repos`

**Query Parameters:**
- `range` (optional): `daily`, `weekly`, or `monthly`
- `limit` (optional): Number of items

**Example:**
```bash
curl "http://localhost:5000/api/news/repos?range=daily&limit=20"
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2025-11-16T10:00:00.000000",
  "data": [
    {
      "name": "awesome-ai-project",
      "url": "https://github.com/...",
      "stars": 12500,
      "description": "...",
      "language": "Python",
      "score": 95.5
    }
  ],
  "count": 20
}
```

---

### 4. Get Only Papers

**Endpoint:** `GET /api/news/papers`

**Query Parameters:**
- `range` (optional): `daily`, `weekly`, or `monthly`
- `limit` (optional): Number of items

**Example:**
```bash
curl "http://localhost:5000/api/news/papers?range=weekly"
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2025-11-16T10:00:00.000000",
  "data": [
    {
      "name": "Paper Title",
      "url": "https://huggingface.co/papers/...",
      "arxiv_id": "2511.08521",
      "upvotes": 7419,
      "published_date": "2025-11"
    }
  ],
  "count": 15
}
```

---

### 5. Get Only Hugging Face Spaces

**Endpoint:** `GET /api/news/spaces`

**Query Parameters:**
- `range` (optional): `daily`, `weekly`, or `monthly`
- `limit` (optional): Number of items

**Example:**
```bash
curl "http://localhost:5000/api/news/spaces"
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2025-11-16T10:00:00.000000",
  "data": [
    {
      "name": "Cool-Space",
      "url": "https://huggingface.co/spaces/...",
      "likes": 1250,
      "sdk": "gradio"
    }
  ],
  "count": 10
}
```

---

## Scheduler Integration

### Using Python Schedule

See `scheduler_example.py` for a complete example:

```bash
python3 scheduler_example.py
```

**Options:**
1. Run once now
2. Schedule daily at 8:00 AM
3. Schedule every hour
4. Fetch repos only

### Using Cron (Linux/Mac)

Add to crontab:
```bash
# Run every day at 8:00 AM
0 8 * * * curl -s "http://localhost:5000/api/news?range=daily&limit=30" > /path/to/news.json
```

### Using Python Requests

```python
import requests

response = requests.get('http://localhost:5000/api/news?range=daily&limit=30')
data = response.json()

if data['success']:
    print(f"Fetched {data['returned_items']} items")
    # Process your data here
```

---

## Error Handling

**Error Response:**
```json
{
  "success": false,
  "error": "Error description here"
}
```

**HTTP Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Invalid parameters
- `500 Internal Server Error` - Server error

---

## Production Deployment

### Running with Gunicorn (Recommended)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

### Running as a Service (systemd)

Create `/etc/systemd/system/ori-ai-trends-api.service`:

```ini
[Unit]
Description=Ori AI Trends API
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/yuv-ai-trends
Environment="COHERE_API_KEY=your_key_here"
ExecStart=/usr/bin/python3 api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ori-ai-trends-api
sudo systemctl start ori-ai-trends-api
```

---

## Security Notes

- The API currently has no authentication
- For production, consider adding API keys or OAuth
- Use HTTPS in production
- Rate limit the endpoints to prevent abuse

---

## Support

For issues or questions, check the main README.md or the source code.

