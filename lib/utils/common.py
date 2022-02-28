# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Mauro Soria

import pickle as _pickle

from ipaddress import IPv4Network, IPv6Network
from urllib.parse import quote

from lib.core.settings import (
    INVALID_CHARS_FOR_WINDOWS_FILENAME, INVALID_FILENAME_CHAR_REPLACEMENT,
    SAFE_BUILTINS, TEXT_CHARS, URL_SAFE_CHARS
)


def safequote(string_):
    return quote(string_, safe=URL_SAFE_CHARS)


def uniq(string_list, filt=False):
    if not string_list:
        return string_list

    return list(filter(None, dict.fromkeys(string_list)))


# Some characters are denied in file name by Windows
def get_valid_filename(string):
    for char in INVALID_CHARS_FOR_WINDOWS_FILENAME:
        string = string.replace(char, INVALID_FILENAME_CHAR_REPLACEMENT)

    return string


def human_size(num):
    base = 1024
    for x in ["B ", "KB", "MB", "GB"]:
        if num < base and num > -base:
            return "%3.0f%s" % (num, x)
        num /= base
    return "%3.0f %s" % (num, "TB")


def is_ipv6(ip):
    return False if ip.count(":") < 2 else True


def iprange(subnet):
    network = IPv4Network(subnet)
    if is_ipv6(subnet):
        network = IPv6Network(subnet)

    return [str(ip) for ip in network]


def is_binary(bytes):
    return bool(bytes.translate(None, TEXT_CHARS))


# Reference: https://docs.python.org/3.4/library/pickle.html#restricting-globals
class RestrictedUnpickler(_pickle.Unpickler):
    def find_class(self, module, name):
        if module.startswith(("lib.", "thirdparty.")) or (
            module == "builtins" and name in SAFE_BUILTINS
        ) or module == "collections":
            return super(RestrictedUnpickler, self).find_class(module, name)

        raise _pickle.UnpicklingError()


def unpickle(*args, **kwargs):
    return RestrictedUnpickler(*args, **kwargs).load()


def pickle(obj, *args, **kwargs):
    return _pickle.Pickler(*args, **kwargs).dump(obj)
