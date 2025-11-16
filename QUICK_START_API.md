# 🚀 Quick Start - API

## Start the API

```bash
./run_api.sh
```

The API will be available at: **http://localhost:5000**

## Test It

```bash
./test_api.sh
```

## Basic Usage

### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

### 2. Get Daily News (30 items)
```bash
curl "http://localhost:5000/api/news?range=daily&limit=30"
```

### 3. Get Weekly News (50 items)
```bash
curl "http://localhost:5000/api/news?range=weekly&limit=50"
```

### 4. Get Only Papers
```bash
curl "http://localhost:5000/api/news/papers"
```

### 5. Get Only Spaces
```bash
curl "http://localhost:5000/api/news/spaces"
```

### 6. Get Only Repos
```bash
curl "http://localhost:5000/api/news/repos"
```

## Use with Python

```python
import requests

# Fetch news
response = requests.get('http://localhost:5000/api/news?range=daily&limit=30')
data = response.json()

if data['success']:
    print(f"Total items: {data['total_items']}")
    print(f"Returned: {data['returned_items']}")
    
    # Process all items
    for item in data['data']['all_items']:
        print(f"- {item['name']} (Score: {item['score']})")
```

## Scheduler Example

Run the interactive scheduler:
```bash
python3 scheduler_example.py
```

## Files Created

- `api.py` - Main API server
- `run_api.sh` - Quick start script
- `test_api.sh` - Test all endpoints
- `scheduler_example.py` - Scheduler integration example
- `API_README.md` - Full documentation
- `QUICK_START_API.md` - This file

## Stop the API

```bash
# Find the process
ps aux | grep api.py

# Kill it
kill <PID>
```

## Next Steps

1. ✅ API is running at http://localhost:5000
2. 📖 Read `API_README.md` for full documentation
3. 🔄 Use `scheduler_example.py` for automated fetching
4. 🚀 Deploy to production with Gunicorn

Enjoy! 🎉

