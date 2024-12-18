import requests
import json
import dotenv
import os
import time

dotenv.load_dotenv()
scraping_dog_api = os.getenv("scraping_dog_api")

urlscrape = "https://api.scrapingdog.com/zillow"

# Base URL for pagination
base_url = "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A42.74203086508082%2C%22south%22%3A41.55079037904701%2C%22east%22%3A-69.78522723388673%2C%22west%22%3A-72.27088397216798%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22usersSearchTerm%22%3A%22%22%7D"

paginated_url =  "https://www.zillow.com/homes/for_sale/{page}_p/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-72.30308083791229%2C%22east%22%3A-69.81742409963104%2C%22south%22%3A41.60106118211541%2C%22north%22%3A42.79136407089516%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22customRegionId%22%3A%2206d2d67623X1-CR1ro5u3y5uzpse_10hdas%22%7D"

# Initialize an empty list to store all listings
all_listings = []

# Loop through pages 1 to 35
for page in range(1,35):
    # Use base_url for page 1, paginated_url for other pages
    url = base_url if page == 1 else paginated_url.format(page=page)
    
    # Set up the parameters
    params = {"api_key": scraping_dog_api, "url": url}
    
    attempts = 0
    success = False
    
    while attempts < 4 and not success:
        # Make the HTTP GET request
        response = requests.get(urlscrape, params=params)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content
            json_response = response.json()
            
            # Append the listings to the all_listings list
            all_listings.extend(json_response.get("zillow_listings", []))
            success = True
        else:
            print(f"Error on page {page} attempt {attempts + 1}: {response.status_code}")
            print(response.text)
            if attempts < 3:  # Don't sleep on last attempt
                time.sleep(5)
            attempts += 1

# Define the output file path
output_file_path = "zillow_photos_combined.json"
# Write first and last property details to log file
if all_listings:
    with open('log.txt', 'a') as log_file:
        log_file.write("\nFirst property in this run:\n")
        first_property = all_listings[0]
        log_file.write(f"Address: {first_property.get('address', 'N/A')}\n")
        log_file.write(f"Price: {first_property.get('price', 'N/A')}\n") 
        log_file.write(f"Zillow ID: {first_property.get('zpid', 'N/A')}\n\n")
        
        log_file.write("Last property in this run:\n")
        last_property = all_listings[-1]
        log_file.write(f"Address: {last_property.get('address', 'N/A')}\n")
        log_file.write(f"Price: {last_property.get('price', 'N/A')}\n")
        log_file.write(f"Zillow ID: {last_property.get('zpid', 'N/A')}\n\n")


# Dump the combined JSON content to a local file
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump({"zillow_listings": all_listings}, f, indent=2)

print(f"Combined JSON response has been saved to {output_file_path}")