<h1 align="center">📰 Real-Time News Intelligence Chatbot</h1>

<p align="center">
  <b>Production-Ready Generative AI System | Conversational RAG | Cloud Deployed</b>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  </a>
  <a href="https://streamlit.io/">
    <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit" />
  </a>
  <a href="https://ai.google.dev/">
    <img src="https://img.shields.io/badge/Gemini-GenAI-4285F4?style=for-the-badge&logo=google" />
  </a>
  <a href="https://aws.amazon.com/ec2/">
    <img src="https://img.shields.io/badge/AWS-EC2-orange?style=for-the-badge&logo=amazon-aws" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Architecture-RAG-green?style=for-the-badge" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Prompt_Engineering-Advanced-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Multi--Turn_Memory-Enabled-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/JSON_Output-Controlled-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Hallucination-Prevention-critical?style=flat-square" />
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1E3C72,100:2A5298&height=120&section=header"/>
</p>

<h3 align="center">
⚡ Conversational AI that delivers real-time, structured, and context-aware news intelligence.
</h3>

<hr/>

<h2 align="center">🔥 Why This Project Stands Out</h2>

<ul align="center" style="list-style: none;">
  <li>✔ <b>Production-Grade Clean Architecture</b> - Modular design with separation of concerns</li>
  <li>✔ <b>Retrieval-Augmented Generation (RAG)</b> - Real-time news + LLM intelligence</li>
  <li>✔ <b>Multi-Turn Conversational Memory</b> - Context-aware follow-up handling</li>
  <li>✔ <b>Structured JSON Output Control</b> - Consistent, parseable responses</li>
  <li>✔ <b>Hallucination Prevention Strategy</b> - Grounded in real news data only</li>
  <li>✔ <b>AWS Cloud Deployment Ready</b> - Complete EC2 deployment guide</li>
  <li>✔ <b>Token-Optimized Prompt Engineering</b> - Efficient API usage</li>
  <li>✔ <b>Multi-Source News APIs</b> - GNews + NewsAPI with intelligent fallback</li>
</ul>

<hr/>

<h2 align="center">🚀 Live Demo</h2>

<p align="center">
  🌐 <b>Deployed on AWS EC2</b><br/><br/>
  👉 <a href="http://18.60.212.35:8501/" target="_blank">
  <img src="https://img.shields.io/badge/🚀_Try_Live_Demo-10B981?style=for-the-badge&logo=rocket" />
  </a>
</p>

<p align="center">
  <i>Live at: <code>http://18.60.212.35:8501/</code></i>
</p>

<hr/>

<h2 align="center">🎯 Project Overview</h2>

<table>
<tr>
<td width="50%">

### 📊 Domain & Purpose
- **Domain:** Real-Time News Intelligence
- **Type:** Domain-Specific Conversational AI
- **Core Function:** Answers user questions using live news data from multiple sources
- **Architecture:** Retrieval-Augmented Generation (RAG) Pipeline

### 🎯 Target Use Cases
- Breaking news queries
- Topic-specific news summaries
- Follow-up questions with context memory
- Multi-turn news conversations

</td>
<td width="50%">

### 🏗️ Technical Stack
| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM Engine | Google Gemini GenAI |
| News APIs | GNews API, NewsAPI |
| Language | Python 3.10+ |
| Deployment | AWS EC2 |
| Architecture | RAG + Prompt Engineering |

</td>
</tr>
</table>

<hr/>

<h2 align="center">✨ Key Features</h2>

<table>
<tr>
<td width="33%" valign="top">

### 🤖 AI Capabilities
- **Multi-Turn Memory** - Context-aware conversations
- **Follow-Up Detection** - Smart article reuse
- **Structured Output** - JSON-controlled responses
- **Hallucination Prevention** - Grounded in real data
- **Prompt Engineering** - Optimized token usage

</td>
<td width="33%" valign="top">

### 📰 News Intelligence
- **Real-Time Fetching** - Live news from GNews + NewsAPI
- **Intelligent Fallback** - Auto-switching between APIs
- **Source Citations** - Clickable article links
- **Breaking News Mode** - Prioritizes recent updates
- **Query Enhancement** - Optimized search terms

</td>
<td width="33%" valign="top">

### 🎨 User Experience
- **ChatGPT-Style UI** - Modern dark theme
- **Streaming Responses** - Real-time word-by-word
- **Source Display** - Expandable citations
- **Chat History** - Persistent conversation memory
- **Responsive Design** - Desktop optimized

</td>
</tr>
</table>

<hr/>

<h2 align="center">🏗️ System Architecture</h2>

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                     (Streamlit Web App)                         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Session    │  │   Prompt     │  │   News Engine        │   │
│  │   Manager    │  │   Builder    │  │   • GNews API        │   │
│  └──────────────┘  └──────────────┘  │   • NewsAPI            │   │
│                                     │   • Smart Fallback     │   │
│                                     └──────────────────────┘   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GEMINI GENAI API                             │
│              (Response Generation Engine)                       │
└─────────────────────────────────────────────────────────────────┘
```

### 🔄 Data Flow
1. **User Input** → Query analysis & follow-up detection
2. **News Retrieval** → Fetch from APIs (cached + fallback)
3. **Prompt Engineering** → Build structured RAG prompt
4. **LLM Processing** → Gemini generates response
5. **Response Streaming** → Real-time display to user
6. **Source Attribution** → Show clickable article links

<hr/>

<h2 align="center">🛠️ Technical Requirements</h2>

### Required APIs

| API | Purpose | Free Tier |
|-----|---------|-----------|
| **Google Gemini GenAI** | LLM Response Generation | 60 requests/minute |
| **GNews API** | Primary News Source | 100 requests/day |
| **NewsAPI** | Fallback News Source | 100 requests/day |

### System Requirements
- **Python:** 3.10 or higher
- **RAM:** 2GB minimum
- **Network:** Internet connection for API calls
- **OS:** Windows/Linux/macOS

<hr/>

<h2 align="center">📦 Installation & Setup</h2>

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd samvaad-gpt
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create `.env` file in root directory:

```env
# Required: Google API Key (Get from https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=your_gemini_api_key_here

# Required: News APIs (Get free tier from these services)
GNEWS_API_KEY=your_gnews_api_key_here
NEWSAPI_KEY=your_newsapi_key_here

# Gemini Configuration
GEMINI_MODEL=gemini-2.0-flash
MAX_OUTPUT_TOKENS=1500
TEMPERATURE=0.7

# App Settings
CONTEXT_MESSAGE_LIMIT=5
NEWS_FETCH_LIMIT=5
STREAM_DELAY_SECONDS=0.02
USE_SQLITE=false
```

### Step 5: Run Locally

```bash
streamlit run app/ui/app.py
```

Visit: `http://localhost:8501`

<hr/>

<h2 align="center">☁️ AWS EC2 Deployment (Amazon Linux 2023)</h2>

<h3>🖥 Step 1: Launch EC2 Instance</h3>

1. Go to <b>AWS Console → EC2 → Launch Instance</b>  
2. Configure:

| Setting | Value |
|----------|--------|
| AMI | Amazon Linux 2023 |
| Instance Type | t2.micro (Free Tier) |
| Key Pair | Create new (.pem) |
| Storage | 8GB+ |

<h3>🔐 Step 2: Configure Security Group (VERY IMPORTANT)</h3>

Add these Inbound Rules:

| Type | Port | Source |
|------|------|--------|
| SSH | 22 | Your IP |
| Custom TCP | 8501 | 0.0.0.0/0 |

⚠️ Without opening port 8501, the app will NOT be accessible.

---

<h3>🔌 Step 3: Connect to EC2</h3>

```bash
chmod 400 your-key.pem
ssh -i "your-key.pem" ec2-user@<EC2-PUBLIC-IP>
```

<h3>📦 Step 4: Install Dependencies (Amazon Linux)</h3>

```bash
sudo yum update -y

sudo yum install python3 -y
sudo yum install python3-pip -y
sudo yum install git -y

python3 --version
```

<h3>📥 Step 5: Clone Project</h3>

```bash
git clone https://github.com/Krishnakant73/Real-Time-Production-Chatbot-Gemini-API.git
cd Real-Time-Production-Chatbot-Gemini-API
```

<h3>🧪 Step 6: Setup Virtual Environment</h3>

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

<h3>🔐 Step 7: Configure Environment Variables</h3>

```bash
nano .env
```

Paste:

```env
GOOGLE_API_KEY=your_key
GNEWS_API_KEY=your_key
NEWSAPI_KEY=your_key
```

Save:
CTRL + O → Enter → CTRL + X

<h3>🚀 Step 8: Run in Background (Recommended Method)</h3>

```bash
nohup streamlit run app/ui/app.py --server.port 8501 --server.address 0.0.0.0 > output.log 2>&1 &
```

Check running:

```bash
ps aux | grep streamlit
```

<h3>🌐 Step 9: Access Application</h3>

Open browser:

```
http://<EC2-PUBLIC-IP>:8501
```

Example:

```
http://18.60.212.35:8501
```

<h3>🔄 Optional: Auto Start on Reboot (Production Mode)</h3>

Create service:

```bash
sudo nano /etc/systemd/system/newsapp.service
```

Paste:

```ini
[Unit]
Description=News Chatbot Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/Real-Time-Production-Chatbot-Gemini-API
ExecStart=/home/ec2-user/Real-Time-Production-Chatbot-Gemini-API/venv/bin/streamlit run app/ui/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable newsapp
sudo systemctl start newsapp
sudo systemctl status newsapp
```

Now your app:

✔ Runs in background
✔ Restarts automatically
✔ Production ready

<hr/>

<h2 align="center">📁 Project Structure</h2>

```
samvaad-gpt/
├── app/
│   ├── ui/
│   │   ├── app.py                 # Main Streamlit application
│   │   └── styles.py              # UI styling & components
│   ├── services/
│   │   ├── gemini_client.py       # Gemini API integration
│   │   ├── news_engine.py         # Multi-source news fetching
│   │   └── response_streamer.py   # Response streaming
│   ├── prompts/
│   │   └── prompt.py              # Prompt engineering & system prompts
│   ├── memory/
│   │   ├── session_manager.py     # Session state management
│   │   ├── sqlite_store.py        # SQLite persistence
│   │   └── context_window.py      # Message history management
│   ├── config/
│   │   └── settings.py            # Configuration management
│   └── utils/
│       ├── helpers.py             # Utility functions
│       └── logger.py              # Logging utilities
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git exclusions
└── README.md                     # This file
```

<hr/>

<h2 align="center">🔧 Configuration Options</h2>

### Sidebar Controls

| Setting | Description | Default |
|---------|-------------|---------|
| Model | Gemini model variant | gemini-2.0-flash |
| Temperature | Response creativity (0.0-1.0) | 0.7 |
| Max Tokens | Response length limit | 1500 |
| Breaking Mode | Real-time urgent news | Off |

### API Rate Limits

| API | Free Tier | Rate Limit |
|-----|-----------|------------|
| GNews | 100 requests/day | 10/hour |
| NewsAPI | 100 requests/day | 10/hour |
| Gemini | Free tier available | 60/minute |

<hr/>

<h2 align="center">📝 Important Notes</h2>

### News Fetching Behavior
- **Best Performance:** 1-day old news (reliable fetching)
- **Recent News:** Breaking news (5min-4hrs) may have fetch delays
- **API Switching:** Automatically switches between GNews and NewsAPI for better coverage

### Message Persistence
- Messages are stored in session state during conversation
- SQLite persistence available (enable `USE_SQLITE=true` in .env)
- Chat history visible in sidebar with topic-based naming

### Source Citations
- Sources shown in expandable "📚 Sources" section
- Clickable links to original articles
- Source names displayed with article titles

<hr/>

<h2 align="center">🐛 Troubleshooting</h2>

### Common Issues

**Import Error: No module named 'X'**
```bash
pip install -r requirements.txt
```

**API Key Error**
- Verify `.env` file exists with correct keys
- Restart the application

**News Not Loading**
- Check API quota limits
- Verify internet connection
- Check API key validity

**Messages Disappearing**
- Enable SQLite persistence: `USE_SQLITE=true`
- Check session state initialization

<hr/>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2A5298,100:1E3C72&height=120&section=footer"/>
</p>

<p align="center">
  <b>Built for Production-Ready GenAI Chatbot Project</b><br>
  <b>Domain:</b> Real-time News Intelligence<br>
  <b>Technologies:</b> Streamlit, Gemini GenAI API, GNews API, NewsAPI
</p>
