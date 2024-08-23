# scrape_data.py - Scrape data from billease FAQs
# Total - 49
# Account - 19
# Auto Debit - 5
# Pay with Grace - 18
# Limit Boost - 7

import csv
import re
import bs4
import requests

URL = "https://billease.ph/faq/"
page = requests.get(URL)
soup = bs4.BeautifulSoup(page.content, "html.parser")

faqs = soup.select_one(".my-16.mx-6.max-w-2xl.text-gray-800")
headers = faqs.select(".text-header-landing.text-subHeader.text-lg.font-semibold.leading-tight.mt-8.pb-4.border-b.border-black")
questions = faqs.select(".text-subHeader.text-xl.font-semibold")
answers = faqs.find_all("div", class_='pb-6')

# Extract hrefs and text from links within answers
links = []
for answer in answers:
    for link in answer.find_all('a'):
        href = link.get('href')
        text = link.get_text(strip=True)
        if href and href.startswith("http"):
            links.append((href, text))

# Header counts
header_counts = {
    "Account": 19,
    "Auto Debit": 5,
    "Pay with Grace": 18,
    "Limit Boost": 7
}

# Flatten the headers and their counts into a list
header_list = []
for header, count in header_counts.items():
    header_list.extend([header] * count)

# Extract text from all headers
header_texts = [re.sub(r'\s+', ' ', header.get_text(strip=True)) for header in headers]

# Open CSV file for writing
with open('./billease_faq.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Heading', 'Question', 'Answer'])  # Write the header row

    # Iterate over questions and answers with headers
    for i, (question, answer) in enumerate(zip(questions, answers)):
        current_header = header_list[i] if i < len(header_list) else "Unknown"
        question_text = re.sub(r'\s+', ' ', question.text.strip())
        answer_text = re.sub(r'\s+', ' ', answer.text.strip())
        writer.writerow([current_header, question_text, answer_text])  # Write each row