import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def clone_webpage(url, output_dir="cloned_site"):
    """
    Clone a webpage and its assets (CSS, JS, images) to a local directory.
    
    Args:
        url (str): The URL of the webpage to clone.
        output_dir (str): The directory to save the cloned files.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        assets_dir = os.path.join(output_dir, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        # Fetch the webpage
        print(f"Fetching {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Save the HTML
        html_file = os.path.join(output_dir, "index.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print(f"Saved HTML to {html_file}")

        # Download CSS files
        for link in soup.find_all("link"):
            href = link.get("href")
            if href and ("css" in href or "stylesheet" in link.get("rel", [])):
                try:
                    file_url = urljoin(url, href)
                    filename = os.path.basename(href) or "stylesheet.css"
                    file_path = os.path.join(assets_dir, filename)
                    print(f"Downloading CSS: {file_url}")
                    css_data = requests.get(file_url, timeout=10).text
                    with open(file_path, "w", encoding="utf-8") as css_file:
                        css_file.write(css_data)
                except Exception as e:
                    print(f"Failed to download CSS {href}: {e}")

        # Download JavaScript files
        for script in soup.find_all("script"):
            src = script.get("src")
            if src:
                try:
                    file_url = urljoin(url, src)
                    filename = os.path.basename(src) or "script.js"
                    file_path = os.path.join(assets_dir, filename)
                    print(f"Downloading JS: {file_url}")
                    js_data = requests.get(file_url, timeout=10).text
                    with open(file_path, "w", encoding="utf-8") as js_file:
                        js_file.write(js_data)
                except Exception as e:
                    print(f"Failed to download JS {src}: {e}")

        # Download images (optional)
        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                try:
                    file_url = urljoin(url, src)
                    filename = os.path.basename(src) or "image.png"
                    file_path = os.path.join(assets_dir, filename)
                    print(f"Downloading image: {file_url}")
                    img_data = requests.get(file_url, timeout=10).content
                    with open(file_path, "wb") as img_file:
                        img_file.write(img_data)
                except Exception as e:
                    print(f"Failed to download image {src}: {e}")

        print("Cloning completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    target_url = "https://myaccount.safaricom.co.ke/mpesa"
    clone_webpage(target_url)
