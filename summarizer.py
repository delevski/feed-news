"""AI-powered summarizer for generating summaries and explanations"""

import anthropic
import os
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class AIContentSummarizer:
    """Generate summaries and trending explanations using Claude API"""
    
    def __init__(self, api_key: str = None):
        """Initialize with Anthropic API key"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Please set it in environment variables.")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate_summary_and_explanation(self, item: Dict) -> Dict:
        """
        Generate one-sentence summary and trending explanation for an item
        
        Args:
            item: Dict containing item data (name, description, source, etc.)
        
        Returns:
            Dict with 'summary' and 'trending_reason' keys
        """
        # Build context based on item type
        source = item.get('source', '')
        name = item.get('name', '')
        description = item.get('description', '')
        
        # Additional context based on source
        context_info = []
        if source == 'github_trending':
            stars = item.get('stars', 0)
            stars_today = item.get('stars_today', 0)
            language = item.get('language', '')
            topics = ', '.join(item.get('topics', [])[:5])
            context_info.append(f"GitHub repository with {stars:,} stars (+{stars_today} today)")
            if language:
                context_info.append(f"Language: {language}")
            if topics:
                context_info.append(f"Topics: {topics}")
        
        elif source == 'huggingface_papers':
            upvotes = item.get('upvotes', 0)
            published_date = item.get('published_date', '')
            context_info.append(f"Research paper with {upvotes} upvotes")
            if published_date:
                context_info.append(f"Published: {published_date}")
        
        elif source == 'huggingface_spaces':
            likes = item.get('likes', 0)
            sdk = item.get('sdk', '')
            context_info.append(f"Hugging Face Space with {likes} likes")
            if sdk:
                context_info.append(f"SDK: {sdk}")
        
        context = '\n'.join(context_info)
        
        prompt = f"""You are analyzing trending AI/ML content. Generate:

1. A single concise sentence (max 15 words) summarizing what this project/paper/space does
2. A brief explanation (2-3 sentences) of why it's trending and what makes it exciting or innovative

Project: {name}
Description: {description}
Context: {context}

Format your response as:
SUMMARY: [one sentence]
TRENDING: [2-3 sentences explaining why it's trending and what's new/exciting]"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            # Parse response
            summary = ""
            trending_reason = ""
            
            lines = response_text.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('SUMMARY:'):
                    current_section = 'summary'
                    summary = line.replace('SUMMARY:', '').strip()
                elif line.startswith('TRENDING:'):
                    current_section = 'trending'
                    trending_reason = line.replace('TRENDING:', '').strip()
                elif current_section == 'summary' and line:
                    summary += ' ' + line
                elif current_section == 'trending' and line:
                    trending_reason += ' ' + line
            
            return {
                'summary': summary.strip(),
                'trending_reason': trending_reason.strip()
            }
        
        except Exception as e:
            print(f"Error generating summary for {name}: {e}")
            return {
                'summary': description[:100] + '...' if len(description) > 100 else description,
                'trending_reason': 'Trending in the AI/ML community.'
            }
    
    def enrich_items_batch(self, items: List[Dict], max_workers: int = 5) -> List[Dict]:
        """
        Enrich multiple items with summaries and explanations in parallel
        
        Args:
            items: List of items to enrich
            max_workers: Max number of parallel API calls
        
        Returns:
            List of enriched items
        """
        enriched_items = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(self.generate_summary_and_explanation, item): item 
                for item in items
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    item['ai_summary'] = result['summary']
                    item['ai_trending_reason'] = result['trending_reason']
                except Exception as e:
                    print(f"Error processing item {item.get('name', 'unknown')}: {e}")
                    item['ai_summary'] = item.get('description', '')[:100]
                    item['ai_trending_reason'] = 'Trending in the AI/ML community.'
                
                enriched_items.append(item)
        
        return enriched_items
