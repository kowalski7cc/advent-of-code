#!/bin/env python3
import argparse
import os
import dotenv
import html2text
import requests
import nbformat as nbf
import logging
from lxml import html

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    dotenv.load_dotenv()
    args = argparse.ArgumentParser()
    args.add_argument("day")
    opts = args.parse_args()
    log.info(f"Getting infos for day {opts.day}")
    session = os.environ["AOC_SESSION"]
    aoc_root = os.path.curdir
    # Check folder day
    day_root = os.path.join(aoc_root, opts.day)
    if not os.path.isdir(day_root):
        os.makedirs(day_root)

    desc_req = requests.get(f"https://adventofcode.com/2022/day/{opts.day}")
    desc_req.raise_for_status()
    tree = html.fromstring(desc_req.text)
    article = tree.xpath("//html/body/main/article")
    day_desc_path = os.path.join(day_root, "day-desc.txt")
    if not os.path.exists(day_desc_path):
        with open(os.path.join(day_root, "day-desc.txt"), "w") as f:
            f.write(html2text.html2text(html.tostring(
                article[0], encoding="utf-8").decode("utf-8")))
            log.info("Day description downloaded")

    code_blocks = tree.xpath("//html/body/main/article/pre/code")
    for index, code in enumerate(code_blocks):
        with open(os.path.join(day_root, f"sample-{index+1}.txt"), "w") as f:
            if code.text:
                f.write(code.text)
        log.info(f"Saved code block sample {index+1}")

    input_req = requests.get(
        f"https://adventofcode.com/2022/day/{opts.day}/input",
        cookies={"session": session}
    )
    input_req.raise_for_status()
    with open(os.path.join(day_root, "input.txt"), "wb") as f:
        for chunk in input_req.iter_content():
            f.write(chunk)
        log.info("Input downloaded")

    notebook_path = os.path.join(day_root, "solution.ipynb")
    if not os.path.exists(notebook_path):
        nb = nbf.v4.new_notebook()
        nb['cells'] = [
            nbf.v4.new_code_cell(
                'with open("sample-1.txt") as f:\n\traw = f.read().splitlines()'
            ),
            nbf.v4.new_code_cell('')
        ]
        nbf.write(nb, notebook_path)


if __name__ == "__main__":
    main()
