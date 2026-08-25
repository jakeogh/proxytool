#!/usr/bin/env python3

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
from clicktool import tvic

signal(SIGPIPE, SIG_DFL)

PROXY_CONF_PATH = Path("/etc/portage/proxy.conf")


def _proxy_conf_items() -> list[tuple[str, str]]:
    items = []
    with open(PROXY_CONF_PATH, "r", encoding="utf8") as fh:
        for line in fh:
            line = line.strip().replace('"', "").replace("#", "")
            if not line:
                continue
            key, value = line.split("=", maxsplit=1)
            items.append((key, value))
    return items


def construct_proxy_dict() -> dict[str, str]:
    try:
        items = _proxy_conf_items()
    except FileNotFoundError as e:
        icp(e)
        return {}
    proxy_dict = {}
    for key, value in items:
        scheme = key.split("_")[0]
        proxy_dict[scheme] = value
    ic(proxy_dict)
    return proxy_dict


def add_proxy_to_environment() -> None:
    for key, value in _proxy_conf_items():
        ic(key, value)
        os.environ[key] = value


@click.group(no_args_is_help=True, cls=AHGroup)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx: click.Context,
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool = False,
) -> None:
    tty, verbose = tvic(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
        ic=ic,
    )


@cli.command("add-proxy-to-environment")
@click_add_options(click_global_options)
@click.pass_context
def _add_proxy_to_environment(
    ctx: click.Context,
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool = False,
) -> None:
    tty, verbose = tvic(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
        ic=ic,
    )

    add_proxy_to_environment()
