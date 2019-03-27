# -*- coding: utf-8 -*-

"""Main module."""

from configparser import ConfigParser
from importlib import resources  # Python 3.7+


def main():
    cfg = ConfigParser()
    cfg.read_string(resources.read_text("brazilian_lottery_tools", "config.txt"))
