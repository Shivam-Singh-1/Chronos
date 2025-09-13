# Chronos - Web Search & Summary Tool

A streamlined web search application that provides comprehensive summaries from multiple sources using DuckDuckGo search results.

## Features

- **Smart Search**: Search the web using DuckDuckGo with up to 50 results
- **Intelligent Summaries**: Generate 2000-word summaries from top search results
- **Content Extraction**: Scrapes and analyzes content from multiple web sources
- **Search History**: Keep track of previous searches with easy re-search functionality
- **Responsive Design**: Clean, modern UI with gradient styling and smooth animations

## How It Works

1. Enter your search query in the search box
2. Chronos fetches up to 50 search results from DuckDuckGo
3. Extracts content from the top 10 results for analysis
4. Generates a comprehensive summary with:
   - Overview section with key findings
   - Important details highlighted in italics
   - Query terms emphasized with underlines
   - Organized bullet points for easy reading
5. Displays all search results with direct links

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chronos-search.git
cd chronos-search
```

2. Install required dependencies:
```bash
pip install streamlit requests beautifulsoup4 pandas
```

3. Run the application:
```bash
streamlit run search_app.py
```

## Dependencies

- `streamlit` - Web app framework
- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing and content extraction
- `pandas` - Data manipulation (imported but not actively used)
- `re` - Regular expressions for text processing

## Usage

1. Open the app in your browser (typically `http://localhost:8501`)
2. Enter your search query in the input field
3. Click "🔍 Search" or press Enter
4. View the generated summary and browse search results
5. Access previous searches from the sidebar history

## Technical Details

- **Search Engine**: DuckDuckGo HTML interface
- **Content Processing**: Extracts meaningful content from paragraphs, filters navigation elements
- **Summary Generation**: Uses extractive summarization with keyword emphasis
- **UI Framework**: Streamlit with custom CSS styling
- **Icons**: Flag Icons library for branding

## Limitations

- Depends on DuckDuckGo's HTML interface availability
- Summary quality depends on source content accessibility
- Some websites may block automated content extraction
- Limited to text-based content analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.