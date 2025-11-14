# Prompt for Coding Agent: Build a Stunning Gen AI News Aggregator

## Project Overview
Create a beautiful, modern web application that aggregates and displays trending AI/ML content from multiple sources (GitHub Trending, Hugging Face Papers, Hugging Face Spaces) in a visually stunning, magazine-style layout.

## Creator Information
**Yuval Avidani** - AI Builder & Speaker

**Social Media & Links:**
- Website: https://yuv.ai
- Linktree: https://linktr.ee/yuvai
- Instagram: @yuval_770
- X/Twitter: @yuvalav
- GitHub: @hoodini
- YouTube: @yuv-ai
- TikTok: @yuval.ai

**Branding:** YUV.AI Developers AI Trends

---

## Design Philosophy
- **Inspiration**: Apple Newsroom, Medium, Stripe's product pages - clean, modern, premium feel
- **Style**: Minimalist, spacious, high-end design with subtle animations
- **Typography**: Clean sans-serif, excellent hierarchy, generous whitespace
- **Colors**: Sophisticated gradients (purple/blue tones), dark text on white cards, subtle shadows
- **Layout**: Card-based grid system, responsive, mobile-first

---

## Core Features & Logic

### 1. Data Aggregation System

#### GitHub Trending Scraper
- **Source**: https://github.com/trending
- **Extract for each repository:**
  - Repository name (owner/repo format)
  - URL to repository
  - Description
  - Total stars count
  - Stars gained today (velocity metric)
  - Forks count
  - Programming language
  - Topics/tags array
  - Number of contributors (from "Built by" section)
  - Time range (daily/weekly/monthly)
- **Language filtering**: Support filtering by specific languages (Python, JavaScript, TypeScript, Jupyter Notebook, etc.)
- **Deduplication**: Remove duplicate repos when fetching multiple languages
- **URL patterns**: Support `/trending`, `/trending/{language}`, `?since=daily|weekly|monthly`

#### Hugging Face Papers Fetcher
- **Source**: https://huggingface.co/papers
- **Extract for each paper:**
  - Paper title
  - Authors list
  - URL to paper page
  - Upvotes count
  - arXiv ID (extract from URL using regex: `\d+\.\d+`)
  - Publication date (parse from arXiv ID format YYMM.NNNNN or from time element)
  - Fetched timestamp
- **Limit**: Fetch top 20 papers by default
- **arXiv parsing logic**: Year-month extraction from arXiv ID (e.g., 2311.12345 → Nov 2023)

#### Hugging Face Spaces Fetcher
- **Source**: Hugging Face Hub API
- **Method**: Use official API to list spaces sorted by likes
- **Extract for each space:**
  - Space ID (author/space-name)
  - URL to space
  - Description (from card data if available)
  - Likes count
  - SDK used (Gradio/Streamlit/Docker/Static)
  - Creation date (formatted as YYYY-MM-DD)
  - Fetched timestamp
- **Limit**: Fetch top 20 spaces by default
- **Fallback**: If API fails, gracefully handle and return empty list

### 2. Smart Ranking Algorithm

#### Scoring System
Create a scoring function that calculates a 0-100 score for each item based on:

**For GitHub Repositories:**
- **Stars score**: `log10(stars + 1) * 10`, capped at 50
- **Velocity score**: `stars_today * 2`, capped at 30
- **Recency score**: 20 (base score for trending items)
- **Formula**: `(stars_score * 0.4) + (velocity_score * 0.3) + (recency_score * 0.3)`

**For Papers:**
- **Upvote score**: `upvotes * 3`, capped at 50
- **Recency score**: 30
- **Formula**: `(upvote_score * 0.6) + (recency_score * 0.4)`

**For Spaces:**
- **Likes score**: `log10(likes + 1) * 15`, capped at 50
- **Recency score**: 30
- **Formula**: `(likes_score * 0.5) + (recency_score * 0.5)`

**For Collections:**
- **Fixed score**: 70 (curated content gets consistent good score)

#### Ranking Logic
1. Calculate score for each item
2. Sort all items by score descending
3. Apply limit (default 50 items)
4. Group by source type for organized display

### 3. Time Range Filtering

**Time ranges:**
- Daily: 1 day
- Weekly: 7 days
- Monthly: 30 days
- Custom: User-specified number of days

**Implementation:**
- GitHub: Use URL parameter `?since=daily|weekly|monthly`
- Papers/Spaces: Filter by fetched timestamp
- Compare item timestamps against cutoff date: `now - timedelta(days=N)`

### 4. Configuration System

**Configurable parameters:**
- GitHub languages to track: `["python", "jupyter-notebook", "typescript", "javascript"]`
- GitHub topics of interest: `["machine-learning", "deep-learning", "llm", "generative-ai", "transformers"]`
- Scoring weights: `stars_weight=0.4, recency_weight=0.3, velocity_weight=0.3`
- Limits per source: HF Spaces limit=20, Papers limit=20, etc.
- Output directory path
- Template directory path

---

## UI/UX Design Specifications

### Header Section
**Layout:**
- **Top bar** (on gradient background):
  - Text: "**Yuval Avidani** • AI Builder & Speaker • **YUV.AI**"
  - Make name and YUV.AI bold
  - Link YUV.AI to https://yuv.ai
  - White text with slight transparency (0.95 opacity)
- **Main title**: "🤖 YUV.AI Developers AI Trends"
- **Subtitle**: Date (format: "November 13, 2025") • Time range (e.g., "Daily Update")
- **Background**: Linear gradient from #667eea to #764ba2

### Stats Dashboard
**4 stat cards showing:**
1. Total Items (not clickable)
2. GitHub Repos (clicks to #github-trending)
3. Papers (clicks to #hf-papers)
4. Spaces (clicks to #hf-spaces)

**Card styling:**
- Number displayed large and bold, colored #667eea
- Label below in uppercase, small gray text
- Hover effect: Background rgba(102, 126, 234, 0.1), lift up 2px
- Smooth scroll behavior when clicked

### Content Cards

**Grid layout:**
- 3 columns on desktop (min 350px per card)
- 2 columns on tablet
- 1 column on mobile
- Gap: 24px between cards

**Card structure:**
```
┌─────────────────────────────────────┐
│ Title (left)            Metric      │
│                         (right)     │
├─────────────────────────────────────┤
│ Badge (if applicable: arXiv, etc.)  │
│ Description text...                 │
│                                     │
│ [tag] [tag] [tag]                   │
│                                     │
│ meta • meta • meta                  │
└─────────────────────────────────────┘
```

**Card styling:**
- White background, no border
- Border radius: 12px
- Box shadow: `0 2px 8px rgba(0,0,0,0.08)`
- Hover: `0 8px 24px rgba(102, 126, 234, 0.15)`, translateY(-4px)
- Padding: 24px
- Smooth transition: 0.3s ease

**GitHub Repo Card specifics:**
- Title: Repository name, dark (#1d1d1f), bold, links to repo
- Right side metrics:
  - Star count: Large (1.2em), bold, purple (#667eea), ⭐ emoji
  - Growth: Smaller (0.85em), green (#34c759), "+X ⭐ today"
- Description: Gray (#6e6e73), line-height 1.6
- Topic tags: Pill-shaped, light gray background (#f5f5f7), dark text
- Meta: Language tag, forks count, contributors count

**Paper Card specifics:**
- Title: Paper title, dark, bold, links to paper
- Right side metrics:
  - Upvotes: Large, bold, purple, 👍 emoji
  - Date: Smaller, gray, publication date
- arXiv badge: Green background (#e8f5e9), dark green text (#2e7d32), "arXiv:XXXX.XXXXX"
- Description: Authors list
- Context badge: "📄 Research Paper"

**Space Card specifics:**
- Title: Space ID, dark, bold, links to space
- Right side metrics:
  - Likes: Large, bold, purple, ❤️ emoji
  - Date: Smaller, gray, "Created: YYYY-MM-DD"
- Description: Space description
- Context badge: "🚀 Interactive Demo"
- SDK tag: Shows Gradio/Streamlit/Docker

### Section Headers
- Large emoji icon (1.5em)
- Bold title (2em, #1d1d1f, weight 700, negative letter-spacing -0.5px)
- Count badge on right (shows number of items)
- Margin-bottom: 30px

### Footer
**Layout:**
- Light gray background (#f8f9fa)
- Center-aligned text
- Credits: "Generated by **Gen AI News Aggregator**"
- Data sources: Links to GitHub and Hugging Face
- Timestamp: When generated

**Creator section (prominent):**
- Border-top: 2px solid #667eea
- Heading: "✨ Built by"
- Name: **Yuval Avidani** (bold)
- Title: "AI Builder & Speaker"
- Button: Gradient background (#667eea to #764ba2), white text, rounded (20px), padding 8px 20px
  - Text: "🌐 YUV.AI"
  - Links to: https://yuv.ai
  - Hover: Scale 1.05

**Social links section:**
- Display links to all social profiles
- Format: Icon/emoji + platform name
- Links:
  - Website: https://yuv.ai
  - Linktree: https://linktr.ee/yuvai
  - Instagram: @yuval_770
  - Twitter/X: @yuvalav
  - GitHub: @hoodini
  - YouTube: @yuv-ai
  - TikTok: @yuval.ai

### Color Palette
- **Primary gradient**: #667eea to #764ba2
- **Card background**: #ffffff
- **Text primary**: #1d1d1f
- **Text secondary**: #6e6e73
- **Text tertiary**: #86868b
- **Growth green**: #34c759
- **Accent purple**: #667eea
- **Tag background**: #f5f5f7
- **Shadow light**: rgba(0,0,0,0.08)
- **Shadow hover**: rgba(102, 126, 234, 0.15)

### Typography
- **Font family**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
- **Line height**: 1.6 for body text
- **Letter spacing**: -0.5px for large headings
- **Font weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

---

## CLI Interface

**Command-line options:**
- `--range [daily|weekly|monthly]`: Time range filter (default: daily)
- `--days N`: Custom number of days (overrides --range)
- `--limit N`: Maximum items in digest (default: 50)
- `--open`: Auto-open generated file in browser
- `--output filename.html`: Custom output filename

**Examples:**
```
main.py --range daily --open
main.py --range weekly --limit 30
main.py --days 14 --output custom.html
main.py --range monthly
```

**Output:**
- Progress messages with emojis (🔥, 📄, 🚀, etc.)
- Item counts found from each source
- Total items fetched
- Path to generated file
- Success message

---

## Data Flow Logic

**Step-by-step execution:**

1. **Parse CLI arguments** → Determine time range and options
2. **Initialize fetchers** → Create instances for GitHub, HF Papers, HF Spaces
3. **Fetch GitHub Trending:**
   - Fetch overall trending
   - Fetch for each configured language
   - Deduplicate by URL
   - Display count found
4. **Fetch GitHub Explore Collections:**
   - Scrape collections page
   - Parse top 10 collections
   - Display count found
5. **Fetch HF Papers:**
   - Scrape papers page
   - Extract paper details with arXiv IDs
   - Display count found
6. **Fetch HF Spaces:**
   - Use HF Hub API
   - Get spaces sorted by likes
   - Display count found
7. **Aggregate all items** → Combine into single list
8. **Rank items:**
   - Calculate score for each item
   - Sort by score descending
   - Apply limit
9. **Group by source** → Organize for display
10. **Calculate statistics** → Count items per source
11. **Generate HTML:**
    - Render template with data
    - Create output filename with timestamp
    - Write to file
12. **Open in browser** (if --open flag set)
13. **Display success message** with file path

---

## Error Handling

**Graceful failure:**
- If GitHub scraping fails → Log error, continue with 0 repos
- If HF Papers fails → Log error, continue with 0 papers
- If HF Spaces API fails → Log error, continue with 0 spaces
- If template rendering fails → Log error with details
- Always complete execution, never crash mid-process

**User feedback:**
- Show "Found X items" for each source
- Show "⚠️ Error: ..." if source fails
- Always show total items fetched
- Always show path to generated file

---

## Responsive Design Rules

**Breakpoints:**
- Desktop: > 768px → 3 columns
- Tablet: 768px → 2 columns
- Mobile: < 768px → 1 column

**Mobile optimizations:**
- Single column layout
- Larger touch targets
- Stats in vertical list instead of horizontal
- Reduce padding on mobile
- Smaller font sizes where appropriate
- Remove unnecessary margins

---

## Animation & Interaction Details

**Smooth scrolling:**
- CSS: `scroll-behavior: smooth`
- All anchor links should scroll smoothly

**Card hover:**
- Transition: 0.3s ease for all properties
- Transform: translateY(-4px)
- Shadow: Deeper, larger spread
- No border color changes

**Clickable elements:**
- Stat cards: Hover background + lift
- All links: Color transition on hover (0.2s)
- Buttons: Scale 1.05 on hover
- Cards: Entire card clickable, opens in new tab

**Loading states:**
- Show "Fetching..." messages during data collection
- Progress indicators for each source

---

## Output Format

**Filename pattern:**
- `digest_{range}_{YYYYMMDD}_{HHMMSS}.html`
- Example: `digest_daily_20251113_170236.html`

**File structure:**
- Self-contained HTML file
- Inline CSS (or linked external stylesheet)
- No external dependencies (except fonts if using CDN)
- Can be opened directly in any browser
- No JavaScript required (unless adding interactivity)

**Output directory:**
- Default: `output/`
- Create directory if doesn't exist
- Keep previous digests (don't overwrite)

---

## Key Differentiators (Make it STUNNING)

1. **Microinteractions**: Every hover, click, scroll should feel smooth and intentional
2. **Typography excellence**: Perfect font hierarchy, spacing that breathes
3. **Whitespace mastery**: Never cramped, always room to breathe
4. **Sophisticated colors**: Gradients that flow, shadows that elevate
5. **Smooth transitions**: 300ms ease on everything interactive
6. **Visual hierarchy**: Eyes flow naturally from important to less important
7. **Premium feel**: Looks like a $100k product, not a script output
8. **Attention to detail**: Pixel-perfect alignment, consistent spacing everywhere

---

## Success Criteria

The final product should make people say **"Wow, this is beautiful!"** when they open it. It should feel like a premium, professionally-designed magazine - not a data dump. Every element should be intentional, every animation purposeful.

Make it so stunning that developers want to share it, bookmark it, and come back daily. The design should be THE reason people choose this over reading trends on GitHub directly.

**Think Apple-level polish. Think premium SaaS product. Think magazine-quality layout.**
