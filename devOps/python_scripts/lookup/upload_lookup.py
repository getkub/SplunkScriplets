import argparse
import csv
import json
import pathlib
import sys
import time
import requests
import splunk_common
from splunk_common import CERT_PATH  # Import CERT_PATH if needed

# ==========================================
# Constants
# ==========================================
SEARCH_ENDPOINT = "/servicesNS/nobody/{app}/search/jobs"
JOB_STATUS_ENDPOINT = "/services/search/jobs/{job_id}"

# ==========================================
# Wait for Splunk Search Job Completion
# ==========================================
def wait_for_job_completion(job_id, headers, base_url, verify, timeout=30):
    """Wait for a search job to complete with timeout."""
    url = f"{base_url}{JOB_STATUS_ENDPOINT.format(job_id=job_id)}"
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            r = requests.get(url, headers=headers, verify=verify)
            if r.status_code == 200:
                response_text = r.text
                if 'isDone">1' in response_text:
                    return True, "completed"
                elif 'isFailed">1' in response_text:
                    return False, "failed"
                elif 'isFinalized">1' in response_text:
                    return True, "finalized"
            time.sleep(2)
        except Exception as e:
            return False, f"error checking status: {e}"
    
    return False, "timeout"

# ==========================================
# Verify Lookup Upload
# ==========================================
def verify_lookup_upload(filename, app, headers, base_url, verify, log):
    """Verify the lookup file was uploaded by testing inputlookup."""
    url = f"{base_url}{SEARCH_ENDPOINT.format(app=app)}"
    splunk_common.log_json(log, 'debug', f"Verification endpoint: {url}")
    
    verify_query = f"| inputlookup {filename} | head 1"
    splunk_common.log_json(log, 'debug', f"Verification query: {verify_query}")
    
    search_data = {
        'search': verify_query,
        'output_mode': 'json'
    }
    
    try:
        r = requests.post(url, headers=headers, data=search_data, verify=verify)
        if r.status_code in [200, 201]:
            response_data = r.json()
            verify_job_id = response_data.get('sid', 'unknown')
            
            success, status = wait_for_job_completion(verify_job_id, headers, base_url, verify, timeout=15)
            if success:
                splunk_common.log_json(log, 'info', f"Verification successful: lookup {filename} exists and is accessible")
                return True
            else:
                splunk_common.log_json(log, 'warning', f"Verification job status: {status}")
                return False
        else:
            splunk_common.log_json(log, 'warning', f"Verification request failed: {r.status_code}")
            return False
    except Exception as e:
        splunk_common.log_json(log, 'warning', f"Exception during verification: {e}")
        return False

# ==========================================
# Read CSV Content
# ==========================================
def read_csv_content(filepath, log):
    lookup_content = []
    try:
        with open(filepath, encoding='utf-8', errors='ignore', newline='') as f:
            for row in csv.reader(f):
                lookup_content.append(row)
        return lookup_content
    except Exception as e:
        splunk_common.log_json(log, 'error', f"Error reading file {filepath}: {e}", status='failed')
        sys.exit(1)

# ==========================================
# Upload Lookup File to Splunk
# ==========================================
def upload_lookup(file_path, app, dry_run, log, headers, base_url, verify):
    filename = pathlib.Path(file_path).name
    lookup_name = filename.replace('.csv', '')  # Remove .csv extension
    
    url = f"{base_url}{SEARCH_ENDPOINT.format(app=app)}"
    splunk_common.log_json(log, 'debug', f"Upload endpoint: {url}")
    
    if dry_run:
        splunk_common.log_json(log, 'info', f"[DRY-RUN] Would upload {filename} to app '{app}' using search API at {url}")
        return

    try:
        # Read CSV as raw text
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        
        # Escape quotes for SPL
        csv_escaped = csv_content.replace('"', '\\"')
        
        # SPL query to create or overwrite lookup
        spl_query = f'''| makeresults format=csv data="
{csv_escaped}"
| outputlookup {filename} createinapp=true'''
        
        splunk_common.log_json(log, 'debug', f"Upload SPL query: {spl_query}")
        
        search_data = {
            'search': spl_query,
            'output_mode': 'json'
        }
        
        # Run search job
        r = requests.post(url, headers=headers, data=search_data, verify=verify)
        
        if r.status_code in [200, 201]:
            response_data = r.json()
            job_id = response_data.get('sid', 'unknown')
            splunk_common.log_json(log, 'info', f"Started search job {job_id} to upload lookup file: {filename}")
            
            # Wait for completion
            splunk_common.log_json(log, 'info', f"Waiting for upload job {job_id} to complete...")
            success, status = wait_for_job_completion(job_id, headers, base_url, verify, timeout=30)
            
            if success:
                splunk_common.log_json(log, 'info', f"Upload job completed with status: {status}")
                splunk_common.log_json(log, 'info', "Verifying lookup upload...")
                
                if verify_lookup_upload(filename, app, headers, base_url, verify, log):
                    splunk_common.log_json(log, 'info', f"Successfully uploaded and verified lookup file: {filename} to app: {app}")
                else:
                    splunk_common.log_json(log, 'warning', f"Upload completed but verification failed for {filename}")
            else:
                splunk_common.log_json(log, 'error', f"Upload job failed with status: {status}", status='failed')
        else:
            splunk_common.log_json(log, 'error', f"Upload failed for {filename} - {r.status_code}: {r.text}", status='failed')
            
    except Exception as e:
        splunk_common.log_json(log, 'error', f"Exception during upload: {e}", status='failed')

# ==========================================
# Main Entry Point
# ==========================================
def main():
    parser = argparse.ArgumentParser()
    splunk_common.add_common_args(parser)
    parser.add_argument("--file-path", required=True, help="Path to the lookup CSV file")
    args = parser.parse_args()

    app, dry_run, log_level, token, base_url = splunk_common.extract_common_args(args)
    log = splunk_common.init_logger(log_level)
    headers = {'Authorization': f'Bearer {token}'}
    verify = CERT_PATH if args.use_cert else True

    splunk_common.log_json(log, 'info', f"Uploading lookup: {args.file_path} | App: {app} | DryRun: {dry_run}")
    upload_lookup(args.file_path, app, dry_run, log, headers, base_url, verify)

if __name__ == '__main__':
    main()
