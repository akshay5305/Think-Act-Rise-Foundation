# Think-Act-Rise-Foundation
# Court Data Fetcher & Mini-Dashboard

## 📹 Demo Video
[**Watch the complete demo video here**](https://youtu.be/U2A_ZQR4USo)  
*5-minute screen recording showing the end-to-end functionality*

---

## 🏛️ Court Target
**Delhi High Court** - https://delhihighcourt.nic.in/

This application fetches case metadata and latest orders/judgments from the Delhi High Court's official website.

---

## ✨ Features

- **Simple Web Interface**: Clean, responsive form for case search
- **Real-time Case Fetching**: Programmatic scraping of Delhi High Court data
- **Comprehensive Case Details**: Extracts parties' names, filing dates, hearing dates, and order PDFs
- **Order Management**: Displays all available case orders with direct PDF download links
- **Error Handling**: User-friendly messages for invalid cases or site downtime
- **Automated Browser Navigation**: Handles complex web forms and dynamic content

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Chrome browser (for Selenium WebDriver)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/court-data-fetcher.git
   cd court-data-fetcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver**
   ```bash
   # On macOS
   brew install chromedriver
   
   # On Ubuntu/Debian
   sudo apt-get install chromium-chromedriver
   
   # Or download from: https://chromedriver.chromium.org/
   ```

4. **Set up case types (optional)**
   ```bash
   # The app includes a case_types.json file with common case types
   # You can modify this file to add/remove case types as needed
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the web interface**
   ```
   Open your browser and navigate to: http://localhost:5000
   ```

---

## 🛠️ Technical Architecture

### Backend Stack
- **Framework**: Flask (Python)
- **Web Scraping**: Selenium WebDriver
- **Browser**: Chrome (headless mode)
- **Data Processing**: JSON, Python built-ins

### Frontend Stack
- **HTML/CSS**: Responsive design with gradient styling
- **JavaScript**: Async form submission and dynamic content rendering
- **UI Components**: Loading spinners, error/success messages

### File Structure
```
court-data-fetcher/
├── app.py                  # Main Flask application
├── selenium_helpers.py     # Selenium automation functions
├── templates/
│   └── index.html         # Web interface template
├── case_types.json        # Configurable case types
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set custom Chrome binary path
CHROME_BINARY_PATH=/path/to/chrome

# Optional: Set custom ChromeDriver path  
CHROMEDRIVER_PATH=/path/to/chromedriver
```

### Case Types Configuration
Edit `case_types.json` to customize available case types:
```json
[
  "BAIL APPLN.",
  "CRIMINAL APPEAL", 
  "CIVIL SUIT",
  "WRIT PETITION",
  "REVIEW PETITION"
]
```

---

## 🎯 CAPTCHA & Anti-Bot Strategy

### Current Approach
- **Headless Browser**: Uses Chrome in headless mode to appear as regular browser traffic
- **Human-like Timing**: Implements realistic delays between actions (2-3 seconds)
- **Dynamic Waiting**: Waits for elements to load naturally rather than fixed delays
- **User-Agent Rotation**: Can be configured to rotate user agents

### Site Navigation Strategy
1. **Direct URL Access**: Opens case status page directly
2. **Form Population**: Fills case type, number, and year programmatically  
3. **Dynamic Waiting**: Waits for search results to load completely
4. **Data Extraction**: Parses results and follows order links
5. **PDF Link Extraction**: Collects all available order PDF URLs

### Reliability Features
- **Timeout Handling**: Configurable timeouts for each operation
- **Error Recovery**: Graceful handling of missing elements or failed requests
- **Browser Cleanup**: Ensures browser resources are properly released

---

## 📊 Data Extraction

### Case Information Extracted
- **Case Details**: Type, number, filing year
- **Party Information**: Petitioner and respondent names
- **Important Dates**: Filing date, next hearing date
- **Case Status**: Current status and stage
- **Orders & Judgments**: Complete list with dates and PDF links

### Data Format Example
```json
{
  "status": "success",
  "message": "Found 5 orders", 
  "orders": [
    {
      "date": "15/01/2024",
      "name": "Order on Bail Application",
      "link": "https://delhihighcourt.nic.in/orders/xyz.pdf"
    }
  ]
}
```

---

## 🔍 Usage Examples

### Basic Case Search
1. Select case type from dropdown (e.g., "BAIL APPLN.")
2. Enter case number (e.g., "1234")
3. Select filing year (e.g., "2024")
4. Click "Search Case"

### Response Scenarios
- **✅ Success**: Displays all case orders with PDF download links
- **❌ No Data**: Shows "No data found" message for invalid case details
- **⚠️ No Orders**: Case found but no orders available yet
- **🚫 Error**: Network issues or site downtime

---

## 🛡️ Error Handling

### User-Friendly Messages
- Invalid case numbers or combinations
- Network connectivity issues  
- Court website downtime
- Missing or corrupted data

### Technical Error Handling
- Selenium timeouts and element not found errors
- HTTP request failures and network issues
- JSON parsing errors for malformed data
- Browser crash recovery

---

## 🚧 Known Limitations

1. **Site Dependency**: Functionality depends on Delhi High Court website structure
2. **Rate Limiting**: No built-in rate limiting (add delays between requests)
3. **CAPTCHA**: Currently bypasses simple anti-bot measures
4. **Browser Requirement**: Needs Chrome/Chromium installed

---

## 🔮 Future Enhancements

### Planned Features
- [ ] **Database Storage**: SQLite/PostgreSQL logging of queries and responses
- [ ] **Multiple Courts**: Support for district courts via eCourts portal
- [ ] **API Endpoints**: RESTful API for programmatic access
- [ ] **Caching**: Redis caching for frequently accessed cases
- [ ] **Notifications**: Email alerts for case updates
- [ ] **Bulk Search**: CSV upload for multiple case queries

---

## 📦 Dependencies

### Core Requirements
```
Flask==2.3.3
selenium==4.15.0
webdriver-manager==4.0.1
beautifulsoup4==4.12.2
requests==2.31.0
```

### Development Requirements
```
pytest==7.4.0
black==23.0.0
flake8==6.0.0
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Feel free to use, modify, and distribute this software.
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚖️ Legal Notice

This tool is designed for educational and research purposes. Users are responsible for:
- Complying with the Delhi High Court's terms of service
- Not overloading the court's servers with excessive requests  
- Using scraped data responsibly and ethically
- Respecting intellectual property rights of court documents

---

## 📞 Support

- **Email**: akshaygarur5305@gmail.com

---

*Built with ❤️ for transparent access to public court information*
