import os
import csv
import requests
import subprocess
from tqdm import tqdm

def download_images_and_update_csv(input_csv, output_csv, repo_url):
    # Create a directory to store the images
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Open the input CSV file
    with open(input_csv, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Create a list to store the updated rows
    updated_data = []

    # Iterate over each row in the data
    for row in tqdm(data, desc="Processing rows"):
        # Get the product handle and create a subdirectory for the images
        product_handle = row["product_handle"]
        product_dir = os.path.join(images_dir, product_handle)
        if not os.path.exists(product_dir):
            os.makedirs(product_dir)

        # Get the image URLs from the "picture_urls" column
        image_urls = row["picture_urls"].split(",")
        total_images = len(image_urls)

        # Create a list to store the downloaded image URLs
        downloaded_image_urls = []

        # Download each image and save it to the subdirectory
        for i, url in enumerate(image_urls, start=1):
            filename = os.path.basename(url)
            image_path = os.path.join(product_dir, filename)
            try:
                response = requests.get(url.strip(), stream=True)
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                downloaded = 0
                with open(image_path, 'wb') as image_file, tqdm(total=total_size, unit='iB', unit_scale=True, unit_divisor=1024, desc=f"Downloading {filename}", leave=False) as progress_bar:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            downloaded += len(chunk)
                            image_file.write(chunk)
                            progress_bar.update(len(chunk))
                downloaded_image_urls.append(f"https://github.com/gsardar/AliTOGit/raw/master/{os.path.relpath(image_path)}")
                print(f"Downloaded image {i}/{total_images} for product handle: {product_handle}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download image {i}/{total_images} for product handle: {product_handle}")
                print(e)

        # Update the row with the downloaded image URLs
        row["downloaded_image_urls"] = ",".join(downloaded_image_urls)
        updated_data.append(row)

    # Write the updated data to the output CSV file
    fieldnames = data[0].keys()
    with open(output_csv, 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_data)

    # Commit the changes to the GitHub repository
    os.chdir(os.path.dirname(__file__))
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Added images"], check=True)
    subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
    subprocess.run(["git", "push", "-u", "origin", "master"], check=True)

    print("Images downloaded, CSV file updated, and changes pushed to the GitHub repository.")

if __name__ == "__main__":
    input_csv = "products.csv"
    output_csv = "output.csv"
    repo_url = "https://github.com/gsardar/AliTOGit.git"
    download_images_and_update_csv(input_csv, output_csv, repo_url)
