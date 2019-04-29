# Jamboree17 boarding card generator

This tool creates Jamboree17 checkin documents.

## Usage

First run the python script, then render the generated xeLaTeX-files to pdfs (there's even a shellscript for this!). Do
with them what you like. Perhaps use mr Hellgren's checking system.

## Requirements

* An activity in [Scoutnet](https://scoutnet.se) with group registration
* Python 2
* Everything in requirements.txt (can be installed with `pip install -r requirements.txt`
* xelatex (you probably want [texlive](https://tug.org/texlive/) or one of its relatives

## What you need to do to make this useful

(It isn't necessarily useful at all...)

Patches that generalize these things are welcome!

- [ ] Replace the activity ID for Jamboree17 (183) with your own  
- [ ] Get API keys for your Scoutnet activity, and put them in environment variables SCOUTNET_GROUP_KEY and SCOUTNET_PARTICIPANT_KEY
- [ ] Replace some logos and texts in template.tex
