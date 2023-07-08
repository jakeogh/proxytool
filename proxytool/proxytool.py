#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement

from __future__ import annotations

import os
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
from asserttool import ic
from asserttool import icp
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from globalverbose import gvd
from pathtool import read_file_bytes

signal(SIGPIPE, SIG_DFL)


def construct_proxy_dict(
    verbose: bool | int | float = False,
):
    try:
        proxy_config = (
            read_file_bytes("/etc/portage/proxy.conf").decode("utf8").split("\n")
        )
    except FileNotFoundError as e:
        icp(e)
        return {}
    ic(proxy_config)
    proxy_dict = {}
    for line in proxy_config:
        ic(line)
        scheme = line.split("=")[0].split("_")[0]
        line = line.split("=")[-1]
        line = line.strip('"')
        ic(scheme)
        proxy_dict[scheme] = line
    ic(proxy_dict)
    return proxy_dict


def add_proxy_to_enviroment():
    # source /home/cfg/net/proxy/setup_proxy_client
    # source /etc/portage/proxy.conf
    with open("/etc/portage/proxy.conf", "r", encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            line = "".join(line.split('"'))
            line = "".join(line.split("#"))
            if line:
                ic(line)
                key = line.split("=")[0]
                value = line.split("=")[1]
                os.environ[key] = value


@click.group(no_args_is_help=True, cls=AHGroup)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool | int | float = False,
) -> None:
    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )
    if not verbose:
        ic.disable()
    else:
        ic.enable()

    if verbose_inf:
        gvd.enable()


@cli.command("add-proxy-to-enviroment")
@click_add_options(click_global_options)
@click.pass_context
def _add_proxy_to_enviroment(
    ctx,
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool | int | float = False,
) -> None:
    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )
    if not verbose:
        ic.disable()
    else:
        ic.enable()

    if verbose_inf:
        gvd.enable()

    add_proxy_to_enviroment()
