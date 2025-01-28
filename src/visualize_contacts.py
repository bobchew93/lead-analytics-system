import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_visualizations():
    # Connect to database and load data
    conn = sqlite3.connect('mock_contacts.db')
    df = pd.read_sql_query("SELECT * FROM contacts", conn)
    conn.close()

    # Set the style
    sns.set_style("whitegrid")
    plt.figure(figsize=(20, 15))

    # 1. Industry Distribution (Pie Chart)
    plt.subplot(2, 2, 1)
    industry_data = df['industry'].value_counts()
    plt.pie(industry_data, labels=industry_data.index, autopct='%1.1f%%')
    plt.title('Industry Distribution', pad=20, size=14)

    # 2. Job Level Distribution (Bar Plot)
    plt.subplot(2, 2, 2)
    sns.countplot(data=df, y='job_level', order=df['job_level'].value_counts().index)
    plt.title('Job Level Distribution', pad=20, size=14)
    plt.xlabel('Number of Contacts')

    # 3. Lead Source Distribution (Bar Plot)
    plt.subplot(2, 2, 3)
    sns.countplot(data=df, x='lead_source')
    plt.xticks(rotation=45)
    plt.title('Lead Source Distribution', pad=20, size=14)
    plt.xlabel('Source')
    plt.ylabel('Number of Contacts')

    # 4. Lead Score Distribution (Histogram)
    plt.subplot(2, 2, 4)
    sns.histplot(data=df, x='lead_score', bins=20)
    plt.title('Lead Score Distribution', pad=20, size=14)
    plt.xlabel('Lead Score')
    plt.ylabel('Count')

    # Adjust layout and save
    plt.tight_layout(pad=3.0)
    plt.savefig('contact_analytics_enhanced.png', dpi=300, bbox_inches='tight')
    print("Visualizations saved as 'contact_analytics_enhanced.png'")

    # Create additional detailed visualizations
    
    # 5. Company Distribution (Top 10)
    plt.figure(figsize=(12, 6))
    company_data = df['company'].value_counts().head(10)
    sns.barplot(x=company_data.values, y=company_data.index)
    plt.title('Top 10 Companies Distribution')
    plt.xlabel('Number of Contacts')
    plt.savefig('top_companies.png', dpi=300, bbox_inches='tight')
    print("Top companies visualization saved as 'top_companies.png'")

    # 6. Lead Score vs Job Level (Box Plot)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='job_level', y='lead_score')
    plt.xticks(rotation=45)
    plt.title('Lead Score Distribution by Job Level')
    plt.savefig('lead_score_by_job.png', dpi=300, bbox_inches='tight')
    print("Lead score analysis saved as 'lead_score_by_job.png'")

    # Print some statistical insights
    print("\n=== Statistical Insights ===")
    print(f"Total Contacts: {len(df)}")
    print(f"\nAverage Lead Score: {df['lead_score'].mean():.2f}")
    print(f"High Value Leads (>75): {len(df[df['lead_score'] > 75])}")
    print(f"\nTop Industry: {df['industry'].mode()[0]}")
    print(f"Most Common Job Level: {df['job_level'].mode()[0]}")
    print(f"Most Common Lead Source: {df['lead_source'].mode()[0]}")

if __name__ == "__main__":
    create_visualizations()
