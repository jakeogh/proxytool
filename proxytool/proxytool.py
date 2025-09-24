#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4


from __future__ import annotations

import os
from pathlib import Path
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

signal(SIGPIPE, SIG_DFL)


def construct_proxy_dict():
    try:
        proxy_config = (
            Path("/etc/portage/proxy.conf").read_bytes().decode("utf8").split("\n")
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
    verbose: bool = False,
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
    verbose: bool = False,
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
