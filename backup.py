import glob
import os
import shutil
import zipfile


def CreateBackup():
    #create a backup folder
    count = 1
    backup_folder = ""
    while True:
        backup_folder = "Backup_" + str(count) 
        if not os.path.exists(backup_folder) and not os.path.exists(backup_folder + ".zip"):
            os.makedirs(backup_folder)
            break
        count += 1

    #copy files to backup folder
    files_to_backup = ["private_key.pem", "public_key.pem", "FitnessPlus"]
    for file_name in files_to_backup:
            file_path = os.path.join(os.getcwd(), file_name)
            backup_path = os.path.join(os.getcwd(), backup_folder, file_name)
            if os.path.isfile(file_path):
                shutil.copy2(file_path, backup_path)

    #zip the folder
    zip_file_name = backup_folder + ".zip"
    try:
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, backup_folder))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Delete the backup folder
    shutil.rmtree(backup_folder)

def RestoreBackUp():
    # Find the latest backup folder
    backup_files = sorted(glob.glob("Backup_*.zip"))
    if len(backup_files) == 0:
        print("No backup folder found.")
        return
    latest_backup_file = backup_files[-1]

    # Create a directory for extracting the backup files
    extraction_path = os.path.splitext(latest_backup_file)[0]
    os.makedirs(extraction_path, exist_ok=True)

    # unzip it
    try:
        with zipfile.ZipFile(latest_backup_file, 'r') as zipf:
            zipf.extractall(extraction_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
     
    # Restore files from the backup folder
    for root,file, files in os.walk(extraction_path):
        for file in files:
            file_path = os.path.join(root, file)
            destination_path = os.path.join(os.getcwd(), file)
            shutil.copy2(file_path, destination_path)

    # delete extracted folder
    shutil.rmtree(extraction_path)
