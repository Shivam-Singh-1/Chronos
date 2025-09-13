import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import pandas as pd
import re

# Page configuration
st.set_page_config(page_title="Chronos", layout="wide", initial_sidebar_state="expanded")

# Initialize session state for search history
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Enhanced CSS styling
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@6.6.6/css/flag-icons.min.css" />
<style>
.main-header {
    text-align: center;
    color: #2c3e50;
    font-size: 3.5rem;
    font-weight: bold;
    margin-bottom: 2rem;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
}
.result-card {
    background: white;
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 10px;
    border-left: 4px solid #e74c3c;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}
.result-title {
    color: #2c3e50;
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.result-url {
    color: #27ae60;
    font-size: 0.9rem;
    word-break: break-all;
}
.result-number {
    background: #e74c3c;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 50%;
    font-weight: bold;
    font-size: 0.8rem;
}
.stats-container {
    background: #ecf0f1;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    text-align: center;
    color: #2c3e50;
    font-weight: 600;
}
.summary-container {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #3498db;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.summary-title {
    color: #2c3e50;
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 1rem;
}
.sidebar-header {
    color: #2c3e50;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    text-align: center;
}
.history-item {
    background: #f8f9fa;
    padding: 0.5rem;
    margin: 0.3rem 0;
    border-radius: 5px;
    border-left: 3px solid #e74c3c;
    cursor: pointer;
    transition: background 0.2s;
}
.history-item:hover {
    background: #e9ecef;
}
</style>
""", unsafe_allow_html=True)

# Sidebar for search history
with st.sidebar:
    st.markdown('<div class="sidebar-header">📚 Search History</div>', unsafe_allow_html=True)
    
    if st.session_state.search_history:
        for i, hist_query in enumerate(reversed(st.session_state.search_history[-10:])):
            # Truncate long queries for display
            display_query = hist_query[:30] + "..." if len(hist_query) > 30 else hist_query
            if st.button(f"🔍 {display_query}", key=f"hist_{i}", use_container_width=True, help=hist_query):
                st.session_state.selected_query = hist_query
                st.session_state.force_search = True
                st.rerun()
    else:
        st.markdown('<p style="color: #7f8c8d; font-style: italic; text-align: center; padding: 1rem;">No search history yet</p>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.search_history = []
        st.rerun()

# Header
st.markdown('<h1 class="main-header"><i class="fi fi-brands-freepik"></i> Chronos</h1>', unsafe_allow_html=True)

# Search input
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    # Check if query was selected from history
    default_query = st.session_state.get('selected_query', '')
    if default_query:
        st.session_state.selected_query = ''
    
    query = st.text_input("Search Query", value=default_query, placeholder="Enter your search query...", label_visibility="collapsed", key="search_input")
    search_clicked = st.button("🔍 Search", use_container_width=True, type="primary")
    
    # Trigger search on Enter key or query change
    if query and (query != st.session_state.get('last_query', '') or st.session_state.get('force_search', False)):
        search_clicked = True
        st.session_state.last_query = query
        st.session_state.force_search = False

def scrape_content(url):
    """Scrape meaningful text content from a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=8)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside", "menu"]):
            element.decompose()
        
        # Focus on main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|main|article'))
        if not main_content:
            main_content = soup
        
        # Get paragraphs for better content
        paragraphs = main_content.find_all('p')
        if paragraphs:
            text = ' '.join([p.get_text().strip() for p in paragraphs[:30]])
        else:
            text = main_content.get_text()
        
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:8000] if text else ""
    except:
        return ""

def format_sentence(sentence, query_words):
    """Format sentence with emphasis on important words."""
    # Highlight query words with italic and underline
    for word in query_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        sentence = pattern.sub(f'<i><u>{word}</u></i>', sentence)
    
    # Emphasize important keywords
    important_words = ['important', 'key', 'main', 'primary', 'essential', 'critical', 'significant', 'major', 'fundamental']
    for word in important_words:
        pattern = re.compile(f'\\b{re.escape(word)}\\b', re.IGNORECASE)
        sentence = pattern.sub(f'<i>{word}</i>', sentence)
    
    return sentence

def generate_summary(query, contents):
    """Generate a comprehensive summary from scraped contents."""
    if not contents:
        return "No content available for summary."
    
    combined_text = " ".join(contents)
    query_words = [w.lower() for w in query.split() if len(w) > 2]
    
    # Split into sentences and filter
    sentences = re.split(r'[.!?]+', combined_text)
    good_sentences = []
    seen_content = set()
    
    for sentence in sentences:
        sentence = sentence.strip()
        sentence_lower = sentence.lower()
        
        # Filter criteria for quality sentences
        if (len(sentence) > 25 and len(sentence) < 300 and 
            not any(skip in sentence_lower for skip in ['click', 'menu', 'login', 'subscribe', 'cookie', 'privacy policy', 'terms of service', 'contact us']) and
            (any(word in sentence_lower for word in query_words) or len(good_sentences) < 3)):
            
            # Check for uniqueness (avoid duplicate content)
            sentence_key = ' '.join(sentence_lower.split()[:5])  # First 5 words as key
            if sentence_key not in seen_content:
                seen_content.add(sentence_key)
                good_sentences.append(sentence)
    
    # Ensure we have enough content for 2000 words
    if not good_sentences:
        # Fallback to any meaningful sentences
        good_sentences = [s.strip() for s in sentences if len(s.strip()) > 25 and len(s.strip()) < 300][:12]
    
    # Select sentences to reach target word count
    selected_sentences = []
    word_count = 0
    target_words = 2000
    
    for sentence in good_sentences:
        sentence_words = len(sentence.split())
        if word_count + sentence_words <= target_words:
            selected_sentences.append(sentence)
            word_count += sentence_words
        elif word_count < 1500:  # If we haven't reached minimum, add anyway
            selected_sentences.append(sentence)
            word_count += sentence_words
        
        if word_count >= target_words:
            break
    
    # Format with sections and emphasis
    if selected_sentences:
        formatted_summary = f"<h3 style='color: #2c3e50; margin-bottom: 1rem;'>📋 Overview of {query.title()}</h3>\n\n"
        
        # Group sentences into sections
        section_size = len(selected_sentences) // 3
        sections = [
            ("🔍 Key Findings", selected_sentences[:section_size]),
            ("💡 Important Details", selected_sentences[section_size:section_size*2]),
            ("📊 Additional Information", selected_sentences[section_size*2:])
        ]
        
        for section_title, section_sentences in sections:
            if section_sentences:
                formatted_summary += f"<h4 style='color: #34495e; margin: 1.5rem 0 0.5rem 0;'>{section_title}</h4>\n\n"
                for sentence in section_sentences:
                    formatted_sentence = format_sentence(sentence.strip(), query_words)
                    formatted_summary += f"• {formatted_sentence}\n\n"
        
        return formatted_summary
    else:
        return "Limited content available for summary."

def scrape_duckduckgo(query):
    """Scrape DuckDuckGo HTML search results for the given query."""
    if not query:
        return []
    headers = {"User-Agent": "Mozilla/5.0"}
    all_results = []
    
    # Get multiple pages to reach 50 results
    for page in range(5):  # 5 pages should give us 50+ results
        try:
            params = {"q": query}
            if page > 0:
                params["s"] = page * 10
            
            res = requests.get("https://html.duckduckgo.com/html/", params=params, headers=headers, timeout=10)
            res.raise_for_status()
        except Exception as e:
            if page == 0:  # Only raise error if first page fails
                raise RuntimeError(f"Request failed: {e}")
            break

        soup = BeautifulSoup(res.text, 'html.parser')
        anchors = soup.find_all('a', class_='result__a')
        if not anchors:
            anchors = soup.find_all('a', class_='result__url')
        
        if not anchors:  # No more results
            break
            
        for a in anchors:
            title = a.get_text().strip()
            url = a.get('href', '').strip()
            if 'uddg=' in url:
                try:
                    qs = parse_qs(urlparse(url).query)
                    url = qs.get('uddg', [url])[0]
                except Exception:
                    pass
            if not title:
                title = url
            all_results.append((len(all_results) + 1, title, url))
            
            if len(all_results) >= 50:  # Stop at 50 results
                break
        
        if len(all_results) >= 50:
            break
    
    return all_results[:50]

# Perform search when button is clicked or Enter is pressed
if search_clicked and query:
    # Add to search history
    if query not in st.session_state.search_history:
        st.session_state.search_history.append(query)
    
    with st.spinner("🔍 Searching..."):
        try:
            results = scrape_duckduckgo(query)
            if results:
                # Generate summary from top 10 results for more content
                with st.spinner("📝 Generating comprehensive summary..."):
                    top_10_urls = [url for _, _, url in results[:10]]
                    contents = [scrape_content(url) for url in top_10_urls]
                    summary = generate_summary(query, [c for c in contents if c])
                
                # Display summary
                st.markdown(f"""
                <div class="summary-container">
                    <div style="line-height: 1.8; color: #34495e; white-space: pre-line;">{summary}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Stats
                st.markdown(f'<div class="stats-container">Found {len(results)} results for "{query}"</div>', unsafe_allow_html=True)
                
                # Display results as cards
                for idx, title, url in results:
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <span class="result-number">{idx}</span>
                            <div style="flex: 1;">
                                <div class="result-title">{title}</div>
                                <div class="result-url">{url}</div>
                            </div>
                            <a href="{url}" target="_blank" style="text-decoration: none;">
                                <button style="background: #e74c3c; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">Visit</button>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ No results found. Please try a different query.")
        except Exception as e:
            st.error(f"❌ Search failed: {e}")
elif search_clicked:
    st.warning("⚠️ Please enter a search query.")