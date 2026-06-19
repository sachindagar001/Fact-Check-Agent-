To make the video play directly inside the GitHub README (instead of just showing a link), you need to use the Markdown image syntax `![Alt text](video_url)`. GitHub will automatically detect that it's a video file and convert it into an embedded video player.

Here is the updated `README.md` file:

```markdown
# 🔍 The Fact-Check Agent

An AI-powered tool that extracts verifiable claims from marketing PDFs, cross-references them against live web data, and flags inaccuracies.

## 📺 Demo Video

![Fact Check Agent Demo Video](https://github.com/sachindagar001/Fact-Check-Agent-/raw/32b85f9fe79f6053c91279bc0518781f65463735/Fact%20check%20agent%20demo%20video.mp4)

---

## ✨ Features

- **In-App PDF Viewer:** Read the uploaded document directly inside the app without needing to open it externally.
- **Intelligent Claim Extraction:** Uses an LLM to identify objective, verifiable claims (statistics, dates, financials) while ignoring marketing fluff.
- **Live Web Verification:** Cross-references extracted claims with real-time web search via Tavily.
- **Clear Verdicts:** Classifies claims as ✅ Verified, ⚠️ Inaccurate (with corrections), or ❌ False, complete with source URLs.
- **Exportable Reports:** Download the final fact-check report as JSON or Markdown.

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **LLM Engine:** OpenRouter (Meta Llama 3.3 70B)
- **Web Search:** Tavily API
- **PDF Parsing:** PyPDF

## 📂 Project Structure

```text
├── app.py          # Main Streamlit UI and application flow
├── config.py       # Environment variables and configuration constants
├── prompts.py      # LLM prompt templates for extraction and verification
├── services.py     # API handlers for OpenRouter and Tavily (with retry logic)
└── helpers.py      # Utility functions (PDF parsing, JSON extraction, Markdown rendering)
```

## 🚀 Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sachindagar001/Fact-Check-Agent-.git
   cd Fact-Check-Agent-
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit requests python-dotenv tavily-python tenacity pypdf
   ```

3. **Configure API Keys**

   Create a `.env` file in the root directory:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
   ```
   *Get a Tavily key at [tavily.com](https://tavily.com) and an OpenRouter key at [openrouter.ai](https://openrouter.ai).*

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📖 How to Use

1. Once the app is running, open your browser and go to `http://localhost:8501`.
2. Click the **"📤 Upload PDF Document"** area or drag and drop your marketing PDF into the box.
3. Click the **"📄 View Uploaded PDF"** dropdown to expand the built-in viewer and read through the document.
4. When you are ready to analyze the document, click the red **"🚀 Start Fact-Checking"** button.
5. Wait a few moments while the AI extracts claims and searches the web. The progress bar will show you the status.
6. Once complete, view the interactive report at the bottom of the page, which displays whether claims are Verified, Inaccurate, or False, along with the evidence.
7. Finally, use the **"⬇️ JSON"** or **"⬇️ Markdown"** buttons to download and save the final fact-check report.
```
