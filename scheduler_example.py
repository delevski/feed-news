"""
Example scheduler script for fetching daily news from the API
"""

import requests
import schedule
import time
from datetime import datetime
import json


def fetch_daily_news():
    """Fetch daily news from API"""
    try:
        print(f"\n🔄 Fetching news at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        
        response = requests.get('http://localhost:5000/api/news?range=daily&limit=30')
        data = response.json()
        
        if data['success']:
            print(f"✅ Success! Fetched {data['returned_items']} items")
            print(f"   - GitHub Repos: {data['stats']['github_repos_count']}")
            print(f"   - Papers: {data['stats']['papers_count']}")
            print(f"   - Spaces: {data['stats']['spaces_count']}")
            
            # Example: Save to file
            filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"   💾 Saved to {filename}")
            
            return data
        else:
            print(f"❌ Error: {data.get('error')}")
    except Exception as e:
        print(f"❌ Exception: {e}")


def fetch_repos_only():
    """Fetch only GitHub repositories"""
    try:
        response = requests.get('http://localhost:5000/api/news/repos?range=daily&limit=20')
        data = response.json()
        
        if data['success']:
            print(f"✅ Fetched {data['count']} repos")
            for repo in data['data'][:5]:  # Show first 5
                print(f"   - {repo['name']} (⭐ {repo.get('stars', 0)})")
            return data
    except Exception as e:
        print(f"❌ Exception: {e}")


if __name__ == "__main__":
    print("🤖 Ori AI Developers AI Trends - Scheduler Example")
    print("=" * 60)
    print("\n📋 Options:")
    print("1. Run once now")
    print("2. Schedule daily at 8:00 AM")
    print("3. Schedule every hour")
    print("4. Fetch repos only")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == '1':
        # Run once immediately
        fetch_daily_news()
    
    elif choice == '2':
        # Schedule daily at 8 AM
        schedule.every().day.at("08:00").do(fetch_daily_news)
        print("\n🕒 Scheduled to run every day at 8:00 AM")
        print("⏳ Waiting for scheduled time...\n")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    elif choice == '3':
        # Schedule every hour
        schedule.every().hour.do(fetch_daily_news)
        print("\n🕒 Scheduled to run every hour")
        print("⏳ Running first fetch...\n")
        fetch_daily_news()
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    elif choice == '4':
        # Fetch repos only
        fetch_repos_only()
    
    else:
        print("Invalid choice!")

