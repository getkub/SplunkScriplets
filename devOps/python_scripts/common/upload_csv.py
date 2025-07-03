import argparse
import csv
import json
import pathlib
import sys
import splunk_common
from splunk_common

LOOKUP_ENDPOINT = "/services/data/lookup_edit/lookup_contents"

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

def upload_lookup(file_path, app, dry_run, log, headers, base_url, verify):
    filename = pathlib.Path(file_path).name
    lookup_data = read_csv_content(file_path, log)

    url = f"{base_url}{LOOKUP_ENDPOINT}"
    payload = {
        "output_mode": "json",
        "namespace": app,
        "lookup_file": filename,
        "contents": json.dumps(lookup_data)
    }

    if dry_run:
        splunk_common.log_json(log, 'info', f"[DRY-RUN] Would upload {filename} to app '{app}' at {url}")
        return

    try:
        r = splunk_common.splunk_request('POST', url, headers, data=payload, verify=verify)
        if r.status_code == 200:
            splunk_common.log_json(log, 'info', f"Uploaded lookup file: {filename} to app: {app}")
        else:
            splunk_common.log_json(log, 'error', f"Upload failed for {filename} - {r.status_code}: {r.text}", status='failed')
    except Exception as e:
        splunk_common.log_json(log, 'error', f"Exception during upload: {e}", status='failed')

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
