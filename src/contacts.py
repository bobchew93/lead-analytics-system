import os
# Delete existing database
if os.path.exists('mock_contacts.db'):
    os.remove('mock_contacts.db')

from faker import Faker
import json
import time
from datetime import datetime
import sqlite3
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

class MockHubSpotContactManager:
    def __init__(self):
        self.fake = Faker()
        self.db_file = 'mock_contacts.db'
        self.setup_database()

    def setup_database(self):
        """Create a SQLite database with enhanced fields"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS contacts
            (id INTEGER PRIMARY KEY,
             email TEXT UNIQUE,
             firstname TEXT,
             lastname TEXT,
             phone TEXT,
             company TEXT,
             industry TEXT,
             job_level TEXT,
             lead_source TEXT,
             lead_score INTEGER,
             created_at DATETIME)
        ''')
        conn.commit()
        conn.close()

    def generate_fake_contact(self):
        """Generate realistic-looking contact data with more variety"""
        companies = [
            'TechCorp', 'Digital Solutions', 'Marketing Pro', 'Data Systems', 'Cloud Nine',
            'Innovation Labs', 'Growth Metrics', 'Future Tech', 'Smart Analytics', 'Digital Edge',
            'Tech Giants', 'Marketing Masters', 'Data Driven Co', 'Cloud Solutions', 'AI Systems'
        ]
        
        industries = [
            'Technology', 'Marketing', 'Healthcare', 'Finance', 'Education',
            'Retail', 'Manufacturing', 'Consulting', 'Real Estate', 'Entertainment'
        ]
        
        job_levels = [
            'Entry Level', 'Mid Level', 'Senior', 'Manager', 'Director',
            'VP', 'C-Level', 'Partner', 'Consultant', 'Associate'
        ]

        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        company = self.fake.random_element(companies)
        domain = company.lower().replace(' ', '') + '.com'
        email = f"{first_name.lower()}.{last_name.lower()}@{domain}"

        return {
            "id": self.fake.random_number(digits=8),
            "properties": {
                "email": email,
                "firstname": first_name,
                "lastname": last_name,
                "phone": self.fake.phone_number(),
                "company": company,
                "industry": self.fake.random_element(industries),
                "job_level": self.fake.random_element(job_levels),
                "created_at": self.fake.date_time_between(start_date='-30d', end_date='now').strftime("%Y-%m-%d %H:%M:%S"),
                "lead_source": self.fake.random_element(['Website', 'LinkedIn', 'Referral', 'Conference', 'Email Campaign']),
                "lead_score": self.fake.random_int(min=0, max=100)
            }
        }

    def create_contact(self, contact_data):
        """Store contact with enhanced fields"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            props = contact_data['properties']
            
            c.execute('''
                INSERT INTO contacts 
                (email, firstname, lastname, phone, company, industry, 
                 job_level, lead_source, lead_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                props['email'],
                props['firstname'],
                props['lastname'],
                props['phone'],
                props['company'],
                props['industry'],
                props['job_level'],
                props['lead_source'],
                props['lead_score'],
                props['created_at']
            ))
            
            conn.commit()
            if (c.lastrowid % 100) == 0:  # Show progress every 100 contacts
                print(f"Created {c.lastrowid} contacts...")
            return True
            
        except sqlite3.IntegrityError:
            print(f"Contact already exists with email: {props['email']}")
            return False
        except Exception as e:
            print(f"Error creating contact: {e}")
            return False
        finally:
            conn.close()

    def create_multiple_contacts(self, number_of_contacts):
        """Create multiple fake contacts"""
        print(f"Creating {number_of_contacts} fake contacts...")
        successful_contacts = 0
        
        for i in range(number_of_contacts):
            contact_data = self.generate_fake_contact()
            if self.create_contact(contact_data):
                successful_contacts += 1
            
        print(f"\nCreated {successful_contacts} out of {number_of_contacts} contacts")

    def analyze_contacts(self):
        """Generate comprehensive contact analytics"""
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query("SELECT * FROM contacts", conn)
        conn.close()

        print("\n=== Contact Analytics Report ===")
        
        # Basic Stats
        print(f"\nTotal Contacts: {len(df)}")
        
        # Company Analysis
        print("\n🏢 Top Companies:")
        company_stats = df['company'].value_counts().head()
        for company, count in company_stats.items():
            print(f"{company}: {count} contacts ({count/len(df)*100:.1f}%)")

        # Industry Analysis
        print("\n🏭 Industry Distribution:")
        industry_stats = df['industry'].value_counts()
        for industry, count in industry_stats.items():
            print(f"{industry}: {count} contacts ({count/len(df)*100:.1f}%)")

        # Job Level Analysis
        print("\n👔 Job Level Distribution:")
        job_stats = df['job_level'].value_counts()
        for level, count in job_stats.items():
            print(f"{level}: {count} contacts ({count/len(df)*100:.1f}%)")

        # Lead Source Analysis
        print("\n📈 Lead Source Distribution:")
        source_stats = df['lead_source'].value_counts()
        for source, count in source_stats.items():
            print(f"{source}: {count} contacts ({count/len(df)*100:.1f}%)")

        # Lead Score Analysis
        print("\n🎯 Lead Score Analysis:")
        print(f"Average Lead Score: {df['lead_score'].mean():.1f}")
        print(f"High Value Leads (Score > 75): {len(df[df['lead_score'] > 75])}")
        
        # Generate visualizations
        self._generate_visualizations(df)

    def _generate_visualizations(self, df):
        """Create detailed visualizations of the contact data"""
        plt.style.use('seaborn')
        fig = plt.figure(figsize=(20, 10))
        
        # Industry Distribution
        plt.subplot(2, 2, 1)
        df['industry'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Industry Distribution')
        
        # Job Level Distribution
        plt.subplot(2, 2, 2)
        df['job_level'].value_counts().plot(kind='bar')
        plt.title('Job Level Distribution')
        plt.xticks(rotation=45)
        
        # Lead Source Distribution
        plt.subplot(2, 2, 3)
        df['lead_source'].value_counts().plot(kind='bar')
        plt.title('Lead Source Distribution')
        plt.xticks(rotation=45)
        
        # Lead Score Distribution
        plt.subplot(2, 2, 4)
        df['lead_score'].hist(bins=20)
        plt.title('Lead Score Distribution')
        
        plt.tight_layout()
        plt.savefig('contact_analytics.png')
        print("\n📊 Analytics visualizations saved as 'contact_analytics.png'")

    def export_contacts_csv(self):
        """Export contacts to CSV file"""
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query("SELECT * FROM contacts", conn)
        conn.close()
        
        filename = f'hubspot_contacts_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(filename, index=False)
        print(f"\n📁 Contacts exported to {filename}")

def main():
    manager = MockHubSpotContactManager()
    
    # Ask user for input
    if input("Create new test contacts? (y/n): ").lower() == 'y':
        try:
            num_contacts = int(input("How many contacts to create?: "))
            # Create contacts
            manager.create_multiple_contacts(num_contacts)
            
            # Generate analytics
            manager.analyze_contacts()
            
            # Export to CSV
            manager.export_contacts_csv()
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
