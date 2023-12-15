from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib3

WebScrapingTool = Flask(__name__)

def simple_web_scraper(url, scrape_option):
    try:
        # Create a PoolManager with urllib3 to handle SSL
        http = urllib3.PoolManager()

        # Send an HTTP request
        response = http.request('GET', url)

        # Check if the request was successful (status code 200)
        if response.status == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.data, 'html.parser')

            # Extract information from the HTML based on user's choice
            if scrape_option == 'data':
                # Extract all text content from the page
                all_text = soup.get_text()

                # Prepare data for the table (split text by lines)
                table_data = [{'Data': line.strip()} for line in all_text.split('\n') if line.strip()]

                return table_data
            elif scrape_option == 'links':
                # Example: Extract all the links on the page
                links = soup.find_all('a')

                # Prepare data for the table
                table_data = [{'Links': link.get('href')} for link in links]

                return table_data
            else:
                return [{'Error': 'Invalid scrape option. Please choose "data" or "links".'}]
        else:
            return [{'Error': f'Error: {response.status}'}]

    except Exception as e:
        return [{'Error': f'An error occurred: {e}'}]

@WebScrapingTool.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website_url = request.form['website_url']
        scrape_option = request.form['scrape_option']
        result = simple_web_scraper(website_url, scrape_option)
        return render_template('WebScrapingTool.html', result=result)

    return render_template('WebScrapingTool.html', result=[])

if __name__ == '__main__':
    WebScrapingTool.run(debug=True)
