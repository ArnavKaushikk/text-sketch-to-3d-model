import os
import shutil
import time
ASSETS_DIR="assets"
CACHE_DIR=os.path.join(ASSETS_DIR,"cache")
LOGS_DIR=os.path.join(ASSETS_DIR,"logs")
OUTPUTS_DIR=os.path.join(ASSETS_DIR,"outputs")
MAX_OUTPUT_AGE_DAYS=7
MAX_LOG_AGE_DAYS=14
def clear_cache():
    """Completely clears cache folder."""
    if not os.path.exists(CACHE_DIR):
        return
    print("[INFO] Clearing cache...")
    for item in os.listdir(CACHE_DIR):
        path=os.path.join(CACHE_DIR,item)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception as e:
            print(f"[WARN] Could not remove {path}: {e}")
def clean_old_outputs():
    """Removes output folders older than MAX_OUTPUT_AGE_DAYS."""
    if not os.path.exists(OUTPUTS_DIR):
        return
    now=time.time()
    cutoff=MAX_OUTPUT_AGE_DAYS*86400
    print("[INFO] Cleaning old outputs...")

    for folder in os.listdir(OUTPUTS_DIR):
        path=os.path.join(OUTPUTS_DIR,folder)

        if not os.path.isdir(path):
            continue

        last_modified=os.path.getmtime(path)

        if now-last_modified>cutoff:
            try:
                shutil.rmtree(path)
                print(f"[INFO] Deleted old output: {folder}")
            except Exception as e:
                print(f"[WARN] Failed to delete {folder}: {e}")


def clean_old_logs():
    """Removes logs older than MAX_LOG_AGE_DAYS."""

    if not os.path.exists(LOGS_DIR):
        return

    now=time.time()
    cutoff=MAX_LOG_AGE_DAYS*86400
    print("[INFO] Cleaning old logs...")
    for file in os.listdir(LOGS_DIR):
        path=os.path.join(LOGS_DIR,file)
        if not os.path.isfile(path):
            continue
        last_modified=os.path.getmtime(path)
        if now-last_modified>cutoff:
            try:
                os.remove(path)
                print(f"[INFO] Deleted old log: {file}")
            except Exception as e:
                print(f"[WARN] Failed to delete log {file}:\t{e}")
def main():
    print("[INFO] Starting cleanup...")
    clear_cache()
    clean_old_outputs()
    clean_old_logs()
    print("[INFO] Cleanup complete.")
if __name__=="__main__":
    main()