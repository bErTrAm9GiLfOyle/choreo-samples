import os
import yaml
import json
import shutil

REPO_BASE_DIR = '..'  # One level up from the .azure directory to get to the repo root
BUILD_STAGING_DIRECTORY = os.environ['BUILD_STAGINGDIRECTORY']

def collect_metadata_and_thumbnails():
    collected_data = []
    print("Starting to collect metadata and thumbnails...")

    # Iterate through directories and collect metadata from metadata.yaml
    for directory in os.listdir(REPO_BASE_DIR):
        dir_path = os.path.join(REPO_BASE_DIR, directory)
        metadata_file = os.path.join(dir_path, 'metadata.yaml')

        print(f"Checking directory: {directory}")
        
        if os.path.isdir(dir_path) and os.path.exists(metadata_file):
            print(f"Found metadata.yaml in directory: {directory}")
            with open(metadata_file, 'r') as f:
                data = yaml.safe_load(f)
                collected_data.append(data)

            # Copy thumbnail to staging directory while preserving folder name
            thumbnail_src = os.path.join(dir_path, data.get('thumbnailPath').split('/')[-1])
            thumbnail_dest_folder = os.path.join(BUILD_STAGING_DIRECTORY, directory)
            os.makedirs(thumbnail_dest_folder, exist_ok=True)
            if os.path.exists(thumbnail_src):
                print(f"Copying thumbnail for {directory}")
                shutil.copy(thumbnail_src, thumbnail_dest_folder)
            else:
                print(f"Thumbnail not found for {directory}")

    return collected_data

def generate_index_json(data):
    # Create index.json structure
    index_data = {
        "samples": data,
        "count": len(data)
    }

    with open(os.path.join(BUILD_STAGING_DIRECTORY, 'index.json'), 'w') as f:
        json.dump(index_data, f, indent=2)
    print("Generated index.json")

def main():
    metadata_data = collect_metadata_and_thumbnails()
    if metadata_data:
        print(f"Collected data for {len(metadata_data)} samples.")
    else:
        print("No metadata collected!")
    generate_index_json(metadata_data)

if __name__ == '__main__':
    main()