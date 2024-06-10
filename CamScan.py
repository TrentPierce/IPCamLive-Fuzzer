import requests
import random
import string
import time

def generate_random_des_hash(length=13):
    """Generates a random string of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def check_video_playable(url):
    """Checks if the page does not contain 'Camera not found'."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if "Camera not found" not in response.text:
                return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

def main():
    base_url = 'https://g1.ipcamlive.com/player/player.php?alias='
    output_file = 'playable_urls.txt'
    checked_hashes = set()
    
    with open(output_file, 'a') as f:
        while True:
            des_hash = generate_random_des_hash()
            
            # Ensure the generated hash is unique
            while des_hash in checked_hashes:
                des_hash = generate_random_des_hash()
            
            checked_hashes.add(des_hash)
            full_url = base_url + des_hash
            print(f"Checking URL: {full_url}")
            
            if check_video_playable(full_url):
                print(f"Playable video found: {full_url}")
                f.write(full_url + '\n')
                f.flush()  # Ensure the URL is written to the file immediately
            else:
                print(f"Camera not found at: {full_url}")
            
            # Random delay between 0 and 1 seconds
            delay = random.uniform(0, 1)
            print(f"Waiting for {delay:.2f} seconds...\n")
            time.sleep(delay)

if __name__ == "__main__":
    main()