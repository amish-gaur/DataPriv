# Privacy Radar

A browser extension that instantly analyzes website privacy policies to help you understand how your data is collected and used. Get clear, actionable insights about privacy risks before you share your information.

## What Privacy Radar Does

Privacy Radar scans any website's privacy policy and gives you a simple risk score (0-99) along with a breakdown of what data is collected, how it's used, and what rights you have. It helps you make informed decisions about which websites to trust with your personal information.

## Key Features

- **Instant Analysis**: Get privacy insights in seconds while browsing
- **Risk Scoring**: Clear 0-99 risk score for easy understanding
- **Data Breakdown**: See exactly what data is collected and why
- **User Rights**: Understand your privacy rights and controls
- **Chrome Extension**: Works directly in your browser
- **Privacy-First**: No data collection, everything runs locally
- **Educational**: Learn about privacy practices and transparency

## How to Use

### For End Users

1. **Install the Chrome Extension**:
   - Download the extension files
   - Open Chrome and go to `chrome://extensions`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the extension folder

2. **Start the Backend** (one-time setup):
   - Run `python3 start_free.py` in the project directory
   - The API will start on `http://localhost:8000`

3. **Analyze Any Website**:
   - Visit any website
   - Click the Privacy Radar extension icon
   - Click "Scan This Site" to get instant privacy analysis
   - Review the risk score and detailed breakdown

### What You'll See

**Risk Score**: A number from 0-99 where:
- 0-30: Low Risk (privacy-friendly)
- 31-60: Medium Risk (some concerns)
- 61-99: High Risk (significant privacy concerns)

**Data Collection**: What personal information the site collects (email, location, browsing history, etc.)

**Purposes**: How your data is used (advertising, analytics, personalization, etc.)

**Data Sharing**: Whether your data is sold or shared with third parties

**Your Rights**: What control you have over your data (delete, opt-out, access, etc.)

**Privacy Insights**: Key concerns and privacy strengths identified by the analysis

## Understanding Your Results

### Low Risk (0-30)
- Clear privacy policy
- Limited data collection
- Strong user rights
- Minimal third-party sharing
- Good transparency

### Medium Risk (31-60)
- Some data collection
- Mixed privacy practices
- Limited user control
- Some third-party sharing
- Moderate transparency

### High Risk (61-99)
- Extensive data collection
- Aggressive tracking
- Limited user rights
- Heavy third-party sharing
- Poor transparency
- No privacy policy found

## Privacy Policy Not Found

If a website doesn't have a privacy policy, Privacy Radar will:
- Assign a high risk score (75+)
- Explain why this is concerning
- Provide recommendations for protecting your privacy
- Suggest using privacy tools and limiting data sharing

## Why Privacy Matters

Websites collect vast amounts of personal data, often without clear disclosure. Privacy Radar helps you:

- **Make Informed Decisions**: Know what you're agreeing to before sharing data
- **Protect Your Privacy**: Identify risky websites and practices
- **Understand Your Rights**: Learn about data protection and user rights
- **Stay Informed**: Keep up with changing privacy practices

## Privacy-First Design

Privacy Radar is designed with your privacy in mind:

- **No Data Collection**: We don't collect or store your browsing data
- **Local Processing**: Analysis happens on your device
- **Open Source**: Transparent code you can review
- **No Tracking**: No analytics or user tracking
- **Educational**: Helps you learn about privacy, not exploit it

## Getting Started

1. **Download Privacy Radar** from the repository
2. **Set up the backend** by running the free version
3. **Install the Chrome extension**
4. **Start browsing** and analyzing websites
5. **Learn about privacy** through the detailed insights

## Support and Learning

- **Privacy Education**: Each analysis includes educational content about privacy practices
- **Clear Explanations**: Technical privacy concepts explained in simple terms
- **Actionable Insights**: Specific recommendations for protecting your privacy
- **Community Data**: Enhanced analysis using community-validated privacy information

## For Developers

If you're interested in the technical implementation, see the [Technical Documentation](DEPLOYMENT.md) for setup instructions, API details, and development information.

## License

This project is open source and available under the MIT License. Privacy analysis data is provided by PrivacySpy under Creative Commons BY license.

---

**Privacy Radar helps you take control of your digital privacy by making website privacy practices transparent and understandable.**