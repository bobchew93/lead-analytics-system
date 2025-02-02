# Lead Analytics System

A Python-based analytics system for B2B lead management and analysis. This system provides data-driven insights into contact distribution, lead scoring, and market segmentation.

## Features

- **Contact Data Management**
  - Contact profile generation and storage
  - Industry and company segmentation
  - Job level categorization

- **Analytics & Insights**
  - Lead score calculation and distribution
  - Industry breakdown analysis
  - Job level distribution
  - Lead source tracking

- **Visualization Dashboard**
  - Contact distribution charts
  - Lead score analysis
  - Company distribution
  - Statistical insights

## Technical Stack

- Python 3.x
- SQLite
- Pandas (Data Analysis)
- Seaborn/Matplotlib (Visualization)
- Faker (Data Generation)

## Mock Data Implementation

This project uses generated mock data to demonstrate B2B lead analytics capabilities:

- Mock data is generated using the Faker library to create realistic contact profiles
- Data includes:
  - Contact information (names, emails)
  - Company details
  - Job titles
  - Industry segments
  - Lead scores

This approach allows:
- Demonstration of analytics capabilities without real customer data
- Testing of data processing functionality
- Showcase of visualization features
- Example of data generation practices

## Contributing
This project uses modern development tools and practices, including AI-assisted documentation. All contributions should maintain similar documentation standards.

## Project Structure
```python
project/
├── src/
│   ├── data_generator.py
│   ├── analytics.py
│   └── visualizations.py
├── tests/
├── requirements.txt
├── README.md
└── .gitignore