"""
    Discord Bot to control your physical room
    Copyright (C) 2020 MorgVerd

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import argparse
import shlex


class DefaultArguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)


class Arguments:
    def __init__(self, posix: bool = False, allow_abbrev: bool = False, **kwargs):
        self.parser = DefaultArguments(allow_abbrev=allow_abbrev, add_help=False, **kwargs)
        self.posix = posix

    def add_argument(self, *inputs, **kwargs):
        """ Shortcut to argparse.add_argument """
        self.parser.add_argument(*inputs, **kwargs)

    def parse_args(self, text):
        """ Shortcut to argparse.parse_args with shlex implemented """
        try:
            args = self.parser.parse_args(
                shlex.split(text if text else "", posix=self.posix)
            )
        except Exception as e:
            return (f"ArgumentError: {e}", False)

        return (args, True)