#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  # Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement


import os
# import sys
# import time
# from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import Union

import click
import sh
# from asserttool import ic
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv

sh.mv = None  # use sh.busybox('mv'), coreutils ignores stdin read errors

signal(SIGPIPE, SIG_DFL)


def add_proxy_to_enviroment():
    # source /home/cfg/net/proxy/setup_proxy_client
    # source /etc/portage/proxy.conf
    with open("/etc/portage/proxy.conf", "r", encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            line = "".join(line.split('"'))
            line = "".join(line.split("#"))
            if line:
                # ic(line)
                key = line.split("=")[0]
                value = line.split("=")[1]
                os.environ[key] = value


@click.group(no_args_is_help=True, cls=AHGroup)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
) -> None:

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )


@click.command("add-proxy-to-enviroment")
@click_add_options(click_global_options)
@click.pass_context
def _add_proxy_to_enviroment(
    ctx,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
) -> None:

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    add_proxy_to_enviroment()


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()
