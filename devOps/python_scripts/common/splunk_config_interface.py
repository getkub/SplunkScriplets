import argparse
from splunk_common import CERT_PATH, add_common_args, extract_common_args, init_logger, load_app_config, parse_splunk_conf, splunk_request, log_json

def handle_macros(file_path, action_flag, dry_run, log, headers, baseUrl, owner, app, verify):
    conf_data = parse_splunk_conf(file_path)
    for stanza, data in conf_data.items():
        name = stanza
        payload = {k: v for k, v in data.items() if v.strip()}
        url = f"{baseUrl}/servicesNS/{owner}/{app}/configs/conf-macros/{name}"
        exists = splunk_request('GET', url, headers, verify=verify).status_code == 200

        log_json(log, 'info', f"Macro: {name} | Exists: {exists} | Action: {action_flag} | DryRun: {dry_run}")

        if action_flag == 'DELETE' and exists:
            log_json(log, 'info', f"Deleting macro: {name}")
            if not dry_run:
                r = splunk_request('DELETE', url, headers, verify=verify)
                log_json(log, 'info' if r.ok else 'error',
                         f"{'Deleted' if r.ok else 'Failed to delete'} macro {name}: {r.text}",
                         status='success' if r.ok else 'failed')

        elif action_flag == 'UPDATE':
            if exists:
                log_json(log, 'info', f"Updating macro: {name}")
                if not dry_run:
                    r = splunk_request('POST', url, headers, data=payload, verify=verify)
                    log_json(log, 'info' if r.ok else 'error',
                             f"{'Updated' if r.ok else 'Failed to update'} macro {name}: {r.text}",
                             status='success' if r.ok else 'failed')
            else:
                log_json(log, 'info', f"Creating macro: {name}")
                if not dry_run:
                    payload['name'] = name
                    create_url = f"{baseUrl}/servicesNS/{owner}/{app}/configs/conf-macros"
                    r = splunk_request('POST', create_url, headers, data=payload, verify=verify)
                    log_json(log, 'info' if r.ok else 'error',
                             f"{'Created' if r.ok else 'Failed to create'} macro {name}: {r.text}",
                             status='success' if r.ok else 'failed')


def handle_savedsearches(file_path, action_flag, dry_run, log, headers, baseUrl, owner, app, verify):
    conf_data = parse_splunk_conf(file_path)
    for name, data in conf_data.items():
        payload = {k: v for k, v in data.items() if v.strip()}
        url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches/{name}"
        exists = splunk_request('GET', url, headers, verify=verify).status_code == 200

        log_json(log, 'info', f"SavedSearch: {name} | Exists: {exists} | Action: {action_flag} | DryRun: {dry_run}")

        if action_flag == 'DELETE' and exists:
            log_json(log, 'info', f"Deleting saved search: {name}")
            if not dry_run:
                r = splunk_request('DELETE', url, headers, verify=verify)
                log_json(log, 'info' if r.ok else 'error',
                         f"{'Deleted' if r.ok else 'Failed to delete'} saved search {name}: {r.text}",
                         status='success' if r.ok else 'failed')

        elif action_flag == 'UPDATE':
            if exists:
                log_json(log, 'info', f"Updating saved search: {name}")
                if not dry_run:
                    r = splunk_request('POST', url, headers, data=payload, verify=verify)
                    log_json(log, 'info' if r.ok else 'error',
                             f"{'Updated' if r.ok else 'Failed to update'} saved search {name}: {r.text}",
                             status='success' if r.ok else 'failed')
            else:
                log_json(log, 'info', f"Creating saved search: {name}")
                if not dry_run:
                    payload['name'] = name
                    create_url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches"
                    r = splunk_request('POST', create_url, headers, data=payload, verify=verify)
                    log_json(log, 'info' if r.ok else 'error',
                             f"{'Created' if r.ok else 'Failed to create'} saved search {name}: {r.text}",
                             status='success' if r.ok else 'failed')


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
    app, dry_run, log_level, token, baseUrl = extract_common_args(args)
    log = init_logger(log_level)
    _, owner = load_app_config()
    headers = {'Authorization': f'Bearer {token}'}

    verify = CERT_PATH if args.use_cert else True

    action = args.action_flag.upper() if args.action_flag else "CHECK"
    if args.action_flag is None:
        dry_run = True

    if args.command == 'macro':
        log_json(log, 'info', f"Macro mode: {action} ({'DRY-RUN' if dry_run else 'EXECUTE'})")
        handle_macros(args.file_path, action, dry_run, log, headers, baseUrl, owner, app, verify)

    elif args.command == 'savedsearch':
        log_json(log, 'info', f"SavedSearch mode: {action} ({'DRY-RUN' if dry_run else 'EXECUTE'})")
        handle_savedsearches(args.file_path, action, dry_run, log, headers, baseUrl, owner, app, verify)


if __name__ == '__main__':
    main()
