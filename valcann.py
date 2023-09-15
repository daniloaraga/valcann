import os
import shutil
import datetime

def list_files_info(path, log_file):
    with open(log_file, 'w') as log:
        for root, dirs, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    # Get file size in bytes
                    file_size = os.path.getsize(file_path)

                    # Get date of last modification
                    modification_time = os.path.getmtime(file_path)
                    modified_date = datetime.datetime.fromtimestamp(modification_time)

                    # Get date of creation (may not be available on all platforms)
                    try:
                        creation_time = os.path.getctime(file_path)
                        created_date = datetime.datetime.fromtimestamp(creation_time)
                    except OSError:
                        created_date = "N/A"

                    # Print file information and write to the log file
                    log.write(f"File: {file_name}\n")
                    log.write(f"Size: {file_size} bytes\n")
                    log.write(f"Date of Creation: {created_date}\n")
                    log.write(f"Date of Last Modification: {modified_date}\n")
                    log.write("=" * 30 + "\n")

                except FileNotFoundError:
                    log.write(f"File not found: {file_path}\n")
                except Exception as e:
                    log.write(f"An error occurred while processing {file_path}: {e}\n")

def remove_old_files(path, days_to_keep):
    current_time = datetime.datetime.now()
    for root, dirs, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Get date of creation (may not be available on all platforms)
                creation_time = os.path.getctime(file_path)
                created_date = datetime.datetime.fromtimestamp(creation_time)

                # Calculate the difference in days
                days_difference = (current_time - created_date).days

                if days_difference > days_to_keep:
                    os.remove(file_path)

            except OSError:
                pass

def copy_recent_files(src_path, dest_path, days_to_keep):
    current_time = datetime.datetime.now()
    for root, dirs, files in os.walk(src_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Get date of creation (may not be available on all platforms)
                creation_time = os.path.getctime(file_path)
                created_date = datetime.datetime.fromtimestamp(creation_time)

                # Calculate the difference in days
                days_difference = (current_time - created_date).days

                if days_difference <= days_to_keep:
                    shutil.copy2(file_path, dest_path)

            except OSError:
                pass

if __name__ == "__main__":
    backups_from_path = "home/valcann/backupsFrom"
    backups_to_path = "home/valcann/backupsTo"
    backups_from_log = "home/valcann/backupsFrom.log"
    backups_to_log = "home/valcann/backupsTo.log"
    days_to_keep = 3

    # Create or open backupsFrom.log for writing
    with open(backups_from_log, 'w') as log_file:
        pass

    # Create or open backupsTo.log for writing
    with open(backups_to_log, 'w') as log_file:
        pass

    # List files' info and save to backupsFrom.log
    list_files_info(backups_from_path, backups_from_log)

    # Remove old files from backupsFrom
    remove_old_files(backups_from_path, days_to_keep)

    # Copy recent files to backupsTo
    copy_recent_files(backups_from_path, backups_to_path, days_to_keep)

    # List copied files' info and save to backupsTo.log
    list_files_info(backups_to_path, backups_to_log)
