import json
import streamlit as st
import config
import prompts
import services
import helpers  # Changed from utils to helpers

st.set_page_config(page_title="Fact-Check Agent", page_icon="🔍", layout="wide")
st.title("🔍 The Fact-Check Agent")
st.write("Upload a marketing PDF to extract claims, cross-reference against live web data, and flag inaccuracies.")
st.divider()

# Check for missing API keys
_missing = [k for k, v in [("TAVILY_API_KEY", config.TAVILY_API_KEY), ("OPENROUTER_API_KEY", config.OPENROUTER_API_KEY)] 
            if not v or v.startswith("YOUR_") or v == "TAVILY_API_KEY"]
if _missing:
    st.error(f"Missing API key(s): {', '.join(_missing)}. Configure them in your `.env` file.")
    st.info("Get a Tavily key at https://tavily.com and an OpenRouter key at https://openrouter.ai")
    st.stop()

uploaded_file = st.file_uploader("📤 Upload PDF Document", type="pdf")

if uploaded_file is not None:
    pdf_hash = helpers.file_hash(uploaded_file)  # Changed to helpers
    cache_key = f"report::{pdf_hash}::{config.OPENROUTER_MODEL}"
    
    with st.sidebar:
        st.header("Run config")
        st.code(f"model: {config.OPENROUTER_MODEL}\nmax_claims: {config.MAX_CLAIMS}\n"
                f"context_chars: {config.MAX_CONTEXT_CHARS}\nsearch_results/claim: {config.MAX_SEARCH_RESULTS}", 
                language="yaml")
        st.caption(f"PDF hash: `{pdf_hash[:12]}…`")

    if st.button("🚀 Start Fact-Checking", type="primary"):
        with st.spinner("Reading PDF…"):
            text = helpers.extract_text_from_pdf(uploaded_file)  # Changed to helpers
            
        if not text.strip():
            st.error("Could not extract text from this PDF (scanned / image-only?).")
            st.stop()
        st.caption(f"Extracted {len(text):,} characters from the PDF.")

        with st.spinner("Extracting claims with LLM…"):
            try:
                llm_resp = services.call_llm(prompts.EXTRACTION_PROMPT.format(text=text[:config.MAX_CONTEXT_CHARS]))
                claims_data = helpers.extract_json_object(llm_resp)  # Changed to helpers
                claims = claims_data.get("claims", [])
                if isinstance(claims, str): claims = [claims]
                if not isinstance(claims, list): claims = []
                claims = claims[:config.MAX_CLAIMS]
            except Exception as e:
                st.error(f"Error extracting claims: {e}")
                st.stop()

        if not claims:
            st.warning("No checkable claims found in this document.")
            st.stop()

        st.success(f"Found {len(claims)} critical claim(s) to verify.")
        st.divider()

        results = []
        progress = st.progress(0.0, text="Starting verification…")
        
        for i, claim in enumerate(claims):
            progress.progress(i / len(claims), text=f"Verifying {i + 1}/{len(claims)}: {claim[:60]}…")
            try:
                sr = services.search_web(claim)
                parts = [f"URL: {r.get('url')}\nContent: {r.get('content', '')}" for r in sr.get("results", [])[:config.MAX_SEARCH_RESULTS]]
                ctx = "\n\n".join(parts) or "(no search results returned)"
                
                vd = helpers.extract_json_object(services.call_llm(prompts.VERIFICATION_PROMPT.format(claim=claim, search_context=ctx)))  # Changed to helpers
                vd["original_claim"] = claim
                v = str(vd.get("verdict", "Error")).strip()
                vd["verdict"] = v if v in config.VERDICT_BADGE else "Error"
                results.append(vd)
            except Exception as e:
                results.append({"original_claim": claim, "verdict": "Error", "correct_fact": "", "evidence": str(e), "sources": []})
                
        progress.progress(1.0, text="Done.")
        progress.empty()
        st.session_state[cache_key] = results

    if cache_key in st.session_state:
        results = st.session_state[cache_key]
        st.header("📊 Fact-Check Report")
        
        counts = {k: 0 for k in config.VERDICT_BADGE}
        for r in results: 
            counts[r.get("verdict", "Error")] = counts.get(r.get("verdict", "Error"), 0) + 1
            
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("✅ Verified", counts.get("Verified", 0))
        c2.metric("⚠️ Inaccurate", counts.get("Inaccurate", 0))
        c3.metric("❌ False", counts.get("False", 0))
        c4.metric("🚫 Errors", counts.get("Error", 0))

        col_json, col_md, _ = st.columns([1, 1, 4])
        with col_json:
            st.download_button("⬇️ JSON", data=json.dumps(results, indent=2), file_name="fact_check_report.json", mime="application/json", use_container_width=True)
        with col_md:
            st.download_button("⬇️ Markdown", data=helpers.render_markdown_report(results, uploaded_file.name, config.OPENROUTER_MODEL), file_name="fact_check_report.md", mime="text/markdown", use_container_width=True)  # Changed to helpers

        st.divider()
        for r in results:
            v = r.get("verdict", "Error")
            badge = config.VERDICT_BADGE.get(v, "❓")
            with st.container(border=True):
                st.subheader(f"{badge} {v}")
                st.write(f"**Original Claim:** {r.get('original_claim')}")
                if v == "Inaccurate" and r.get("correct_fact"): 
                    st.write(f"**Correct Fact:** {r.get('correct_fact')}")
                if r.get("evidence"): 
                    st.write(f"**Evidence:** {r.get('evidence')}")
                srcs = [s for s in r.get("sources", []) if s]
                if srcs:
                    st.write("**Sources:**")
                    for url in srcs: 
                        st.markdown(f"- [{url}]({url})")