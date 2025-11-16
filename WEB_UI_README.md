# 🎨 NewsFeed Web UI

Beautiful, modern web interface for browsing AI/ML news from GitHub and Hugging Face.

## Features

### 🎯 Key Features
- ✨ **Clean, Modern Design** - Apple-inspired interface
- 📱 **Responsive Layout** - Works on desktop, tablet, and mobile
- 🔍 **Real-time Search** - Search through all news items
- 🏷️ **Smart Filtering** - Filter by source type (Repos, Papers, Spaces)
- ⏱️ **Time Ranges** - View Daily, Weekly, or Monthly trends
- 📊 **Quick Stats** - See counts and metrics at a glance
- 🎨 **Beautiful Cards** - News displayed in engaging cards
- ⚡ **Fast & Lightweight** - No build process, pure HTML/CSS/JS

## Layout

### Top Bar
- **Logo** - NewsFeed branding
- **Search** - Real-time search across all news
- **Notifications** - Alert bell icon
- **User Avatar** - Profile access

### Left Sidebar
- **Navigation Menu**
  - Home (all items)
  - GitHub Repos
  - Papers
  - Spaces
  - Bookmarks (coming soon)
  - Settings (coming soon)

### Center Feed
- **Time Range Tabs** - Daily, Weekly, Monthly
- **News Cards** - Each card shows:
  - Source icon and name
  - Post time (relative)
  - Title (clickable link)
  - Description
  - Tags (language, topics, SDK)
  - Stats (stars, upvotes, likes, score)
  - Actions (Like, Share, Save)

### Right Sidebar
- **Suggested Topics** - Quick topic navigation
- **Quick Stats** - Real-time counts

## Usage

### Local Development

1. **Start the API:**
   ```bash
   ./run_api.sh
   ```

2. **Open in browser:**
   ```
   http://localhost:5000/
   ```

### Vercel Deployment

The UI automatically deploys with your Vercel project:
```
https://your-app.vercel.app/
```

## How It Works

### API Integration

The UI calls these API endpoints:

- `GET /api/news?range=daily&limit=50` - Fetch news items
- Automatically detects if running locally or on Vercel
- CORS enabled for cross-origin requests

### Filtering

**By Source Type:**
- Click nav items to filter by GitHub, Papers, or Spaces
- "Home" shows all items

**By Time Range:**
- Click tabs to switch between Daily, Weekly, Monthly
- Automatically refetches data

**By Search:**
- Type in search box to filter by title or description
- Real-time filtering as you type

### Features

**News Cards:**
- Click title to open source (GitHub/HuggingFace)
- Tags show language and topics
- Stats show popularity metrics
- Actions for future interactivity

**Responsive Design:**
- Desktop: Full 3-column layout
- Tablet: 2-column (hides right sidebar)
- Mobile: Single column (hides both sidebars)

## Customization

### Colors

Edit the CSS in `index.html`:

```css
/* Primary color */
color: #0066cc;

/* Background */
background: #f5f5f7;

/* Cards */
background: white;
```

### Layout

Adjust widths in CSS:

```css
.left-sidebar { width: 220px; }
.center-feed { max-width: 600px; }
.right-sidebar { width: 240px; }
```

### Content

Modify HTML sections:
- Logo text: `.logo`
- Navigation items: `.nav-item`
- Topics: `.topic-item`

## Tech Stack

- **Frontend**: Vanilla JavaScript (no frameworks!)
- **Styling**: Pure CSS with Flexbox
- **API**: Flask backend
- **Icons**: Emoji (no icon fonts needed)

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## Performance

- **Initial Load**: ~1-2s (depends on API)
- **Search**: Instant (client-side)
- **Filter**: Instant (no API call)
- **Range Switch**: ~1-2s (new API call)

## Future Enhancements

- [ ] Bookmarks (save favorites)
- [ ] Settings (customize view)
- [ ] Dark mode
- [ ] Infinite scroll
- [ ] Share functionality
- [ ] Real like/save actions
- [ ] User authentication
- [ ] Comments/discussions

## Files

- `index.html` - Complete web UI (HTML/CSS/JS)
- `api.py` - Flask backend with CORS
- `api/index.py` - Vercel entry point

## Troubleshooting

### UI not loading?
- Check if API is running: `http://localhost:5000/api/health`
- Check browser console for errors

### No data showing?
- Verify API is returning data: `http://localhost:5000/api/news`
- Check CORS headers are present

### Search not working?
- Make sure items have loaded first
- Check browser console for errors

## Support

- GitHub: https://github.com/delevski/feed-news
- Issues: Report on GitHub

---

**Enjoy your beautiful AI news feed!** 🎉

