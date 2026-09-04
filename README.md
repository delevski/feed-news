# AI Trends News Feed

A configurable news-intelligence pipeline that collects AI and developer content, ranks it, adds optional AI summaries, and publishes the result as a web feed, HTML digest, or JSON API.

It brings GitHub repositories, Hugging Face activity, research papers, and developer news into one filterable view instead of requiring separate monitoring tools.

## Features

- Multi-source collection for AI, ML, and developer news
- Configurable relevance and popularity ranking
- Optional summaries through Cohere or Anthropic
- Responsive web feed with search and source filters
- Daily, weekly, monthly, and custom-range HTML digests
- Flask API with health, combined-news, repository, paper, and Space endpoints
- CLI, cron, Windows Task Scheduler, and GitHub Actions workflows
- Vercel deployment configuration

## Stack

- Python
- Flask
- Requests and Beautiful Soup
- Jinja2
- Hugging Face Hub
- Cohere or Anthropic for optional summaries
- HTML, CSS, and vanilla JavaScript

## Run locally

```bash
git clone https://github.com/delevski/feed-news.git
cd feed-news
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Generate a digest:

```bash
python main.py
python main.py --range weekly --limit 30
python main.py --disable-ai
```

Start the API and web interface:

```bash
python api.py
```

Then open `http://localhost:5000`.

## API

| Endpoint | Purpose |
| --- | --- |
| `/api/health` | Health check |
| `/api/news` | Combined ranked feed |
| `/api/news/repos` | GitHub repositories |
| `/api/news/papers` | Research papers |
| `/api/news/spaces` | Hugging Face Spaces |

Example:

```bash
curl "http://localhost:5000/api/news?range=daily&limit=20"
```

## Configuration

Edit `config.py` to tune sources and scoring. Add `COHERE_API_KEY` or `ANTHROPIC_API_KEY` to `.env` only if AI summaries are needed. The pipeline works without an AI provider by using extracted descriptions.

See [API_README.md](API_README.md), [AUTOMATION.md](AUTOMATION.md), and [DEPLOYMENT.md](DEPLOYMENT.md) for extended setup.
