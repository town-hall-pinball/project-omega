# Copyright (c) 2014 - 2015 townhallpinball.org
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from copy import deepcopy
import fractions


def to_list(value):
    return value if isinstance(value, list) or isinstance(value, tuple) else [value]

# dict_merge from
# http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts
def dict_merge(target, *args):
    """
    Merges two dictionaries. From:
    http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts
    Example::
        >>> a = { "foo": 1 }
        >>> b = { "bar": 2 }
        >>> util.dict_merge(a, b)
        { "foo": 1, "bar": 2 }
    """

    # Merge multiple dicts
    if len(args) > 1:
        for obj in args:
            dict_merge(target, obj)
        return target

    # Recursively merge dicts and set non-dict values
    obj = args[0]
    if not isinstance(obj, dict):
        return obj
    for k, v in obj.iteritems():
        if k in target and isinstance(target[k], dict):
            dict_merge(target[k], v)
        else:
            target[k] = deepcopy(v)
    return target


def fraction(value):
    """
    Converts the floating point `value` into a human-readable fraction.
    Example::
        >>> util.fraction(2)
        "2"
        >>> util.fraction(2.5)
        "2 1/2"
    """
    fraction = fractions.Fraction(value).limit_denominator(4)
    if fraction.numerator == 0:
        return "0"
    if fraction.numerator < fraction.denominator:
        return str(fraction.numerator) + "/" + str(fraction.denominator)
    whole = fraction.numerator / fraction.denominator
    if fraction.denominator == 1:
        return str(whole)
    numerator = fraction.numerator - (whole * fraction.denominator)
    return str(whole) + " " + str(numerator) + "/" + str(fraction.denominator)

