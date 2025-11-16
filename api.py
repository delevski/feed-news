"""
Flask API for Ori AI Developers AI Trends
Provides JSON endpoints for fetching trending AI/ML content
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os

from fetchers import GitHubTrendingFetcher, GitHubExploreFetcher, HuggingFaceFetcher
from ranker import ContentRanker
import config

app = Flask(__name__)

# Set COHERE_API_KEY from environment
COHERE_API_KEY = os.environ.get('COHERE_API_KEY', 'vFEFFraWFP4wCCPXitxfrrwkbNPzZWrs7WA7Uumf')


def fetch_all_news(time_range='daily', limit=30):
    """
    Fetch and rank all news items
    
    Args:
        time_range: 'daily', 'weekly', or 'monthly'
        limit: Maximum number of items to return
    
    Returns:
        dict: Structured news data
    """
    try:
        # Determine time range in days
        time_range_days = config.TIME_RANGES.get(time_range, 1)
        
        # Initialize components
        github_trending = GitHubTrendingFetcher()
        github_explore = GitHubExploreFetcher()
        hf_fetcher = HuggingFaceFetcher()
        ranker = ContentRanker()
        
        all_items = []
        
        # Fetch GitHub Trending
        try:
            gh_time_range = time_range if time_range in ['daily', 'weekly', 'monthly'] else 'daily'
            github_repos = github_trending.fetch_all_languages(since=gh_time_range)
            all_items.extend(github_repos)
        except Exception as e:
            print(f"GitHub trending error: {e}")
        
        # Fetch GitHub Explore
        try:
            collections = github_explore.fetch_collections()
            all_items.extend(collections)
        except Exception as e:
            print(f"GitHub explore error: {e}")
        
        # Fetch Hugging Face Papers
        try:
            papers = hf_fetcher.fetch_papers(limit=20)
            all_items.extend(papers)
        except Exception as e:
            print(f"HF papers error: {e}")
        
        # Fetch Hugging Face Spaces
        try:
            spaces = hf_fetcher.fetch_trending_spaces(limit=config.HF_SPACES_TRENDING_LIMIT)
            all_items.extend(spaces)
        except Exception as e:
            print(f"HF spaces error: {e}")
        
        if not all_items:
            return {
                'success': False,
                'error': 'No items found',
                'data': []
            }
        
        # Rank items
        ranked_items = ranker.rank_items(all_items, days_range=time_range_days)
        
        # Get top items
        top_items = ranker.get_top_items(ranked_items, limit=limit)
        
        # Group by source
        grouped_items = ranker.group_by_source(top_items)
        
        return {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'time_range': time_range,
            'total_items': len(all_items),
            'returned_items': len(top_items),
            'data': {
                'github_repos': grouped_items.get('github', []),
                'github_collections': grouped_items.get('github_collection', []),
                'papers': grouped_items.get('paper', []),
                'spaces': grouped_items.get('space', []),
                'all_items': top_items
            },
            'stats': {
                'github_repos_count': len(grouped_items.get('github', [])),
                'papers_count': len(grouped_items.get('paper', [])),
                'spaces_count': len(grouped_items.get('space', [])),
                'collections_count': len(grouped_items.get('github_collection', []))
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': []
        }


@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API documentation"""
    return jsonify({
        'service': 'Ori AI Developers AI Trends API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'news': '/api/news?range=daily&limit=30',
            'repos': '/api/news/repos',
            'papers': '/api/news/papers',
            'spaces': '/api/news/spaces'
        },
        'documentation': 'https://github.com/delevski/feed-news',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api', methods=['GET'])
def api_root():
    """API root endpoint"""
    return jsonify({
        'service': 'Ori AI Developers AI Trends API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'news': '/api/news?range=daily&limit=30',
            'repos': '/api/news/repos',
            'papers': '/api/news/papers',
            'spaces': '/api/news/spaces'
        }
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Ori AI Developers AI Trends API',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/news', methods=['GET'])
def get_news():
    """
    Main endpoint to fetch news
    
    Query Parameters:
        - range: 'daily', 'weekly', or 'monthly' (default: 'daily')
        - limit: Number of items to return (default: 30, max: 100)
    
    Example:
        GET /api/news?range=daily&limit=50
    """
    time_range = request.args.get('range', 'daily').lower()
    limit = int(request.args.get('limit', 30))
    
    # Validate parameters
    if time_range not in ['daily', 'weekly', 'monthly']:
        return jsonify({
            'success': False,
            'error': 'Invalid time_range. Must be daily, weekly, or monthly'
        }), 400
    
    if limit > 100:
        limit = 100
    
    result = fetch_all_news(time_range=time_range, limit=limit)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500


@app.route('/api/news/repos', methods=['GET'])
def get_repos():
    """Get only GitHub repositories"""
    time_range = request.args.get('range', 'daily').lower()
    limit = int(request.args.get('limit', 30))
    
    result = fetch_all_news(time_range=time_range, limit=limit)
    
    if result['success']:
        return jsonify({
            'success': True,
            'timestamp': result['timestamp'],
            'data': result['data']['github_repos'],
            'count': len(result['data']['github_repos'])
        })
    else:
        return jsonify(result), 500


@app.route('/api/news/papers', methods=['GET'])
def get_papers():
    """Get only papers"""
    time_range = request.args.get('range', 'daily').lower()
    limit = int(request.args.get('limit', 30))
    
    result = fetch_all_news(time_range=time_range, limit=limit)
    
    if result['success']:
        return jsonify({
            'success': True,
            'timestamp': result['timestamp'],
            'data': result['data']['papers'],
            'count': len(result['data']['papers'])
        })
    else:
        return jsonify(result), 500


@app.route('/api/news/spaces', methods=['GET'])
def get_spaces():
    """Get only Hugging Face spaces"""
    time_range = request.args.get('range', 'daily').lower()
    limit = int(request.args.get('limit', 30))
    
    result = fetch_all_news(time_range=time_range, limit=limit)
    
    if result['success']:
        return jsonify({
            'success': True,
            'timestamp': result['timestamp'],
            'data': result['data']['spaces'],
            'count': len(result['data']['spaces'])
        })
    else:
        return jsonify(result), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on this server',
        'available_endpoints': {
            'root': '/',
            'api_root': '/api',
            'health': '/api/health',
            'news': '/api/news?range=daily&limit=30',
            'repos': '/api/news/repos',
            'papers': '/api/news/papers',
            'spaces': '/api/news/spaces'
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    # Set API key from environment
    if COHERE_API_KEY:
        os.environ['COHERE_API_KEY'] = COHERE_API_KEY
    
    print("🚀 Starting Ori AI Developers AI Trends API...")
    print("📍 API will be available at: http://localhost:5000")
    print("\n📋 Available endpoints:")
    print("   GET / - API documentation")
    print("   GET /api - API root")
    print("   GET /api/health - Health check")
    print("   GET /api/news?range=daily&limit=30 - Get all news")
    print("   GET /api/news/repos - Get only repos")
    print("   GET /api/news/papers - Get only papers")
    print("   GET /api/news/spaces - Get only spaces")
    print("\n✨ Press Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

