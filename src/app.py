#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "1.0.0"


import argparse

from gui import Gui
from console import Console


def main():
    parser = argparse.ArgumentParser(
        prog='AVdownloader',
        description='AV Downloader is a lightweight tool to help you download AV and IMG from the sis41')
    parser.add_argument('--version', action='version',
                        version='%(prog)s '+__version__)
    parser.add_argument('-u', '--username',
                        help='choose who\'s project you want to download, one or more', nargs='*')
    parser.add_argument('-d', '--directory', help='output directory')
    parser.add_argument(
        '-t', '--type', choices=['all', 'image', 'video'], default="all", help='what do you what to download, default is all')
    parser.add_argument('-v', '--verbosity', action="count",
                        help="increase output verbosity")
    args = parser.parse_args()

    if args.username:
        if args.directory:
            console = Console()
            console.download_by_usernames(args.username, args.directory, args.type)
        else:
            print("no output directory, please use -d or --directory option to set")
    else:
        app = Gui(version=__version__)
        app.mainloop()  


if __name__ == '__main__':
    main()
