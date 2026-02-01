# Job Market Intelligence Platform

A web application that analyzes job market trends, identifies in-demand skills, and provides personalized career recommendations.

## Live Demo

**[Click here to try the app](https://job-market-analyzer-jpgmzhdm5ntkjmw8ti5gvg.streamlit.app/)**

## Features

### Market Overview
- Total job postings and company statistics
- Top job titles and hiring companies
- Experience level distribution

### Skills Analysis
- Top 15 in-demand tech skills
- Top 15 in-demand soft skills
- Visual charts showing skill demand

### Salary Insights
- Average and median salaries
- Highest paying tech skills
- Salary comparison across skills

### Job Recommendations
- Enter your skills
- Get matched with relevant jobs
- See matching score and job details

### Skills Gap Analysis
- Input your current skills
- Set your target job title
- Discover skills you need to learn
- See which of your skills are valuable

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend language |
| Streamlit | Web application framework |
| Pandas | Data manipulation |
| Plotly | Interactive visualizations |
| NLP | Skill extraction from job descriptions |

## Dataset

- **Source:** LinkedIn Job Postings (Kaggle)
- **Size:** 20,000 job postings
- **Features:** Job titles, descriptions, salaries, locations, experience levels

## How It Works

1. **Data Loading:** Loads job posting data from CSV
2. **Skill Extraction:** Uses NLP to extract tech and soft skills from job descriptions
3. **Analysis:** Calculates skill demand, salary correlations, and job matches
4. **Visualization:** Displays insights through interactive Plotly charts

## Run Locally

```bash
# Clone the repository
git clone https://github.com/yashsingh05/job-market-analyzer.git
cd job-market-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Project Structure

```
job-market-analyzer/
├── app.py                 # Main Streamlit application
├── postings_small.csv     # Job postings dataset
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Sample Insights

### Top Tech Skills in Demand
1. AI
2. Excel
3. SQL
4. Python
5. AWS

### Top Soft Skills in Demand
1. Communication
2. Leadership
3. Problem Solving
4. Teamwork
5. Analytical

## Future Enhancements

- Add real-time job data via APIs
- Include more job sources
- Add AI-powered career advice chatbot
- Trend analysis over time
- Resume skill matching
- Email alerts for matching jobs

## Disclaimer

This application is for **educational purposes only**. Job market data is from a point-in-time dataset and may not reflect current market conditions.

## Author

**Yash Singh**

- GitHub: [@yashsingh05](https://github.com/yashsingh05)

## Related Projects

- [AI-Powered Financial Analyzer](https://github.com/yashsingh05/financial-analyzer) - Stock and crypto analysis with forecasting

## License

This project is open source and available under the MIT License.
