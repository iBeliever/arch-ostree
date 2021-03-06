#! /usr/bin/env python3

# arch-ostree config.yml master 32

import sys

from arch_ostree import OSTree
from arch_ostree.utils import load_yaml

os_release_template = '''NAME="{long_name}"
ID={name}
PRETTY_NAME="{long_name}"
ANSI_COLOR="{ansi_color}"
HOME_URL="{home_url}"
SUPPORT_URL="{support_url}"
BUG_REPORT_URL="{bug_report_url}"
'''

if __name__ == '__main__':
    config = load_yaml(sys.argv[1])

    branch = sys.argv[2]
    build_number = sys.argv[3]
    repo_dir = sys.argv[4] if len(sys.argv) > 4 else 'ostree'

    ostree = OSTree(config['name'], 'pacstrap', 'x86_64')
    ostree.create(config['packages'])
    ostree.install_release(os_release_template.format(**config))
    ostree.install_aur(config.get('aur_packages', []))
    ostree.enable_sudo_access()
    for service in config.get('enabled_services', []):
        ostree.enable_service(service)
    for service in config.get('disabled_services', []):
        ostree.disable_service(service)
    ostree.prepare()
    ostree.commit(repo_dir, branch, config['channel'], build_number)
