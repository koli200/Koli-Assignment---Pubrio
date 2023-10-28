from bs4 import BeautifulSoup
import requests
import json

def extract_job_info(job_url):
    # Send an HTTP GET request to the job URL
    response = requests.get(job_url)
    if response.status_code == 200:
        # Parse the HTML content of the job posting
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract company name
        company_name_elem = soup.find('a', class_='topcard__org-name-link')
        company_name = company_name_elem.text.strip() if company_name_elem else None

        # Extract job position
        position_elem = soup.find('h1', class_='topcard__title')
        position = position_elem.text.strip() if position_elem else None

        # Extract job location
        location_elem = soup.find('span', class_='topcard__flavor')
        location = location_elem.text.strip() if location_elem else None

        # Extract job technologies
        technologies = []
        skills_section = soup.find('section', class_='description__skills')
        if skills_section:
            skill_tags = skills_section.find_all('span', class_='job-criteria__text')
            for tag in skill_tags:
                technologies.append(tag.text.strip())

        # Create a dictionary for the job posting
        job_info = {
            "company_name": company_name,
            "position": position,
            "location": location,
            "technologies": technologies
        }

        return job_info
    else:
        return None

# List of LinkedIn job posting URLs
job_urls = [
    "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3737301869",
    "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=2592651955",
    "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3603589097"
]

# Initialize an empty list to store the extracted job information
job_info_list = []

for job_url in job_urls:
    job_info = extract_job_info(job_url)
    if job_info:
        job_info_list.append(job_info)

# Output the job information in JSON format
output_json = json.dumps(job_info_list, indent=4)
print(output_json)
