#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Exception Module

"""
from typing import Optional


class Error(Exception):
    """Base class for package exceptions.

    :Attributes:

    - **expression**: *str* input expression in which the error occurred
    - **message**: *str* explanation of the error
    """

    def __init__(
        self,
        expression: Optional[str] = None,
        message: Optional[str] = None,
    ):
        self.expression = expression
        self.message = message


class InputError(Error):
    """Exception raised for errors in the input."""
