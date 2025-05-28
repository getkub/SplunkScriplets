import argparse
from splunk_common import *

def handle_macros(file_path, action_flag, dry_run, log, headers, baseUrl, owner, app):
    conf_data = parse_splunk_conf(file_path)
    for stanza, data in conf_data.items():
        name = stanza
        payload = {k: v for k, v in data.items() if v.strip()}
        url = f"{baseUrl}/servicesNS/{owner}/{app}/configs/conf-macros/{name}"
        exists = splunk_request('GET', url, headers).status_code == 200

        if action_flag == 'DELETE':
            if exists:
                log.info("🗑️ Deleting macro: %s", name)
                if not dry_run:
                    r = splunk_request('DELETE', url, headers)
                    if r.ok:
                        log.info("✅ Deleted macro: %s", name)
                    else:
                        log.info("❌ Failed to delete macro %s: %s", name, r.text)
        elif action_flag == 'UPDATE':
            if exists:
                log.info("✏️ Updating macro: %s", name)
                if not dry_run:
                    r = splunk_request('POST', url, headers, data=payload)
                    if r.ok:
                        log.info("✅ Updated macro: %s", name)
                    else:
                        log.info("❌ Failed to update macro %s: %s", name, r.text)
            else:
                log.info("📄 Creating macro: %s", name)
                if not dry_run:
                    payload['name'] = name
                    create_url = f"{baseUrl}/servicesNS/{owner}/{app}/configs/conf-macros"
                    r = splunk_request('POST', create_url, headers, data=payload)
                    if r.ok:
                        log.info("✅ Created macro: %s", name)
                    else:
                        log.info("❌ Failed to create macro %s: %s", name, r.text)

def handle_savedsearches(file_path, action_flag, dry_run, log, headers, baseUrl, owner, app):
    conf_data = parse_splunk_conf(file_path)
    for name, data in conf_data.items():
        payload = {k: v for k, v in data.items() if v.strip()}
        url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches/{name}"
        exists = splunk_request('GET', url, headers).status_code == 200

        if action_flag == 'DELETE':
            if exists:
                log.info("🗑️ Deleting saved search: %s", name)
                if not dry_run:
                    r = splunk_request('DELETE', url, headers)
                    if r.ok:
                        log.info("✅ Deleted saved search: %s", name)
                    else:
                        log.info("❌ Failed to delete saved search %s: %s", name, r.text)
        elif action_flag == 'UPDATE':
            if exists:
                log.info("✏️ Updating saved search: %s", name)
                if not dry_run:
                    r = splunk_request('POST', url, headers, data=payload)
                    if r.ok:
                        log.info("✅ Updated saved search: %s", name)
                    else:
                        log.info("❌ Failed to update saved search %s: %s", name, r.text)
            else:
                log.info("📄 Creating saved search: %s", name)
                if not dry_run:
                    payload['name'] = name
                    create_url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches"
                    r = splunk_request('POST', create_url, headers, data=payload)
                    if r.ok:
                        log.info("✅ Created saved search: %s", name)
                    else:
                        log.info("❌ Failed to create saved search %s: %s", name, r.text)

def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    add_common_args(parent_parser)

    parser = argparse.ArgumentParser(description="Update or delete Splunk macros or saved searches.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    macro_parser = subparsers.add_parser('macro', parents=[parent_parser])
    macro_parser.add_argument('--file-path', required=True)
    macro_parser.add_argument('--action-flag', choices=['update', 'delete'])

    search_parser = subparsers.add_parser('savedsearch', parents=[parent_parser])
    search_parser.add_argument('--file-path', required=True)
    search_parser.add_argument('--action-flag', choices=['update', 'delete'])

    args = parser.parse_args()
    app, dry_run, log_level = extract_common_args(args)
    log = init_logger(log_level)

    token, baseUrl = load_auth_settings()
    _, owner = load_app_config()
    headers = {'Authorization': f'Bearer {token}'}

    if args.command == 'macro':
        action = args.action_flag.upper() if args.action_flag else "CHECK"
        if args.action_flag is None:
            dry_run = True
        log.info("🔧 Macro mode: %s (%s)", action, "DRY-RUN" if dry_run else "EXECUTE")
        handle_macros(args.file_path, action, dry_run, log, headers, baseUrl, owner, app)

    elif args.command == 'savedsearch':
        action = args.action_flag.upper() if args.action_flag else "CHECK"
        if args.action_flag is None:
            dry_run = True
        log.info("🔧 SavedSearch mode: %s (%s)", action, "DRY-RUN" if dry_run else "EXECUTE")
        handle_savedsearches(args.file_path, action, dry_run, log, headers, baseUrl, owner, app)

if __name__ == '__main__':
    main()
