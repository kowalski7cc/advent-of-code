#!/bin/env python3
import textwrap
import datetime
import argparse
import logging
import os

import dotenv
import html2text
import requests
from lxml import html

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

package_json = """{
    "name": "aoc-2022",
    "version": "1.0.0",
    "description": "",
    "main": "solution.js",
    "scripts": {
        "build": "tsc",
        "start": "node solution.js"
    },
    "keywords": [],
    "devDependencies": {
    "@types/node": "^20.10.1"
  }
}"""

tsconfig_json = """{
    "compilerOptions": {
        "types": [
            "node"
        ]
    },
}"""


def main():
    dotenv.load_dotenv()
    dateparser = argparse.ArgumentParser(add_help=False)
    today = datetime.datetime.today()
    dateparser.add_argument("-y", "--year", type=int)
    deciding_args, _ = dateparser.parse_known_args()
    args = argparse.ArgumentParser(parents=[dateparser])
    args.add_argument("-d", "--day", default=today.day, required=deciding_args.year)
    dateparser.set_defaults(year=today.year)
    args.add_argument("-l", "--language", default="python")
    opts = args.parse_args()

    year: int = opts.year
    day: int = opts.day

    log.info("Getting infos for day %s of year %s", day, year)
    if "AOC_SESSION" not in os.environ:
        log.error("AOC_SESSION not found in environment variables")
        exit(1)
    session = os.environ["AOC_SESSION"]
    aoc_root = os.path.curdir
    # Check folder day
    day_root = os.path.join(aoc_root, str(year), str(day).zfill(1))
    if not os.path.isdir(day_root):
        os.makedirs(day_root)

    desc_req = requests.get(f"https://adventofcode.com/{year}/day/{day}", timeout=10)
    try:
        desc_req.raise_for_status()
    except requests.exceptions.HTTPError:
        if desc_req.status_code == 404:
            log.error("Day/Year not found")
            exit(1)
    tree = html.fromstring(desc_req.text)
    article: html.HtmlElement = tree.xpath("//html/body/main/article")
    day_desc_path = os.path.join(day_root, "day-desc.txt")
    if not os.path.exists(day_desc_path):
        with open(
            os.path.join(day_root, "day-desc.txt"), "w", encoding="utf-8"
        ) as file:
            file.write(html2text.html2text(str(html.tostring(article[0]))))
            log.info("Day description downloaded")

    code_blocks = tree.xpath("//html/body/main/article/pre/code")
    for index, code in enumerate(code_blocks):
        with open(
            os.path.join(day_root, f"sample-{index+1}.txt"), "w", encoding="utf-8"
        ) as file:
            if code.text:
                file.write(code.text)
        log.info("Saved code block sample %s", index + 1)

    input_req = requests.get(
        f"https://adventofcode.com/2022/day/{day}/input",
        cookies={"session": session},
        timeout=10,
    )

    input_req.raise_for_status()
    with open(os.path.join(day_root, "input.txt"), "wb") as file:
        for chunk in input_req.iter_content():
            file.write(chunk)
        log.info("Input downloaded")

    if opts.language in ["python", "py", "py3", "p"]:
        import nbformat as nbf

        notebook_path = os.path.join(day_root, "solution.ipynb")
        if not os.path.exists(notebook_path):
            new_nb = nbf.v4.new_notebook()
            new_nb["cells"] = [
                nbf.v4.new_code_cell(
                    'with open("sample-1.txt") as f:\n\traw = f.read().splitlines()'
                ),
                nbf.v4.new_code_cell(""),
            ]
            nbf.write(new_nb, notebook_path)

    if opts.language in ["typescript", "ts", "t"]:
        # # create package.json
        # with open(
        #     os.path.join(day_root, "package.json"), "w", encoding="utf-8"
        # ) as file:
        #     file.write(package_json)

        import subprocess

        subprocess.run(["npm", "install" , "-D", "@types/node"], cwd=day_root)

        # create tsconfig.json
        with open(
            os.path.join(day_root, "tsconfig.json"), "w", encoding="utf-8"
        ) as file:
            file.write(tsconfig_json)

        with open(os.path.join(day_root, "solution.ts"), "w", encoding="utf-8") as file:
            file.write(textwrap.dedent(
                """\
                import * as fs from 'fs';
                import * as path from 'path';
                import * as util from 'util';

                const input = fs.readFileSync(path.join(__dirname, 'input.txt'), 'utf-8');"""
            ))


if __name__ == "__main__":
    main()
