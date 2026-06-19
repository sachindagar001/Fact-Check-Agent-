Here is a clean, professional `README.md` file for your project. I've included a placeholder at the top for your video. 

If your video is on YouTube, you can replace the placeholder line with:
`[![Watch the video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://youtu.be/YOUR_VIDEO_ID)`

***

```markdown
# 🔍 The Fact-Check Agent

Upload a marketing PDF to automatically extract verifiable claims, cross-reference them against live web data, and flag inaccuracies. 

## 📺 Demo

<!-- EMBED YOUR VIDEO HERE -->
https://github.com/user-attachments/assets/your-video-id-here

*(Replace the link above with your video embed or YouTube link)*

---

## ✨ Features

- **In-App PDF Viewer:** Read the uploaded document directly inside the app without needing to open it externally.
- **Smart Claim Extraction:** Uses an LLM to identify only objective, verifiable claims (statistics, dates, financials), ignoring subjective marketing fluff.
- **Live Web Verification:** Cross-references extracted claims with real-time web searches via Tavily.
- **Clear Verdicts:** Classifies claims as ✅ Verified, ⚠️ Inaccurate (with corrections), or ❌ False, complete with source URLs.
- **Export Reports:** Download the final fact-check report as JSON or Markdown.

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **LLM Engine:** OpenRouter (Default: Meta Llama 3.3 70B)
- **Web Search:** Tavily API
- **PDF Parsing:** PyPDF

## 📂 Project Structure

The application is modularized for easy maintenance:

- `app.py` - Main Streamlit UI and application flow.
- `config.py` - Environment variables and configuration constants.
- `prompts.py` - LLM prompt templates for extraction and verification.
- `services.py` - API handlers for OpenRouter and Tavily (with retry logic).
- `helpers.py` - Utility functions (PDF parsing, JSON extraction, Markdown rendering).

## 🚀 Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fact-check-agent.git
   cd fact-check-agent
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit requests python-dotenv tavily-python tenacity pypdf
   ```

3. **Configure API Keys**
   
   Create a `.env` file in the root directory and add your keys:
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

1. Open the app in your browser (usually `http://localhost:8501`).
2. Upload a marketing PDF using the file uploader.
3. Expand the **"View Uploaded PDF"** section to read the document in-app.
4. Click **"🚀 Start Fact-Checking"**.
5. View the interactive report and download the results as JSON or Markdown.
```
