#!/bin/bash
# Test script for Ori AI Trends API

echo "🧪 Testing Ori AI Developers AI Trends API"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${BLUE}Test 1: Health Check${NC}"
curl -s http://localhost:5000/api/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Get 5 items (daily)
echo -e "${BLUE}Test 2: Get 5 Daily News Items${NC}"
curl -s "http://localhost:5000/api/news?range=daily&limit=5" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"✅ Success: {data['success']}\")
print(f\"📊 Total items fetched: {data['total_items']}\")
print(f\"📋 Returned items: {data['returned_items']}\")
print(f\"Stats:\")
print(f\"  - GitHub Repos: {data['stats']['github_repos_count']}\")
print(f\"  - Papers: {data['stats']['papers_count']}\")
print(f\"  - Spaces: {data['stats']['spaces_count']}\")
print(f\"\nTop 3 items:\")
for i, item in enumerate(data['data']['all_items'][:3], 1):
    print(f\"  {i}. {item['name']}\")
    print(f\"     Source: {item['source']}, Score: {item['score']}\")
"
echo ""
echo ""

# Test 3: Get Papers Only
echo -e "${BLUE}Test 3: Get Papers Only${NC}"
curl -s "http://localhost:5000/api/news/papers?range=daily&limit=3" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"✅ Success: {data['success']}\")
print(f\"📄 Papers count: {data['count']}\")
if data['count'] > 0:
    print(f\"\nPapers:\")
    for i, paper in enumerate(data['data'][:3], 1):
        print(f\"  {i}. {paper['name']}\")
        print(f\"     Upvotes: {paper.get('upvotes', 0)}\")
else:
    print(\"No papers found in this batch\")
"
echo ""
echo ""

# Test 4: Get Spaces Only
echo -e "${BLUE}Test 4: Get Spaces Only${NC}"
curl -s "http://localhost:5000/api/news/spaces?range=daily&limit=3" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"✅ Success: {data['success']}\")
print(f\"🚀 Spaces count: {data['count']}\")
if data['count'] > 0:
    print(f\"\nSpaces:\")
    for i, space in enumerate(data['data'][:3], 1):
        print(f\"  {i}. {space['name']}\")
        print(f\"     Likes: {space.get('likes', 0)}\")
else:
    print(\"No spaces found in this batch\")
"
echo ""
echo ""

echo -e "${GREEN}✅ All tests completed!${NC}"

