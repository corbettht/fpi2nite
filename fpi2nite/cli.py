#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: fpi2nite.cli
.. moduleauthor:: hank corbett <htc@unc.edu>
"""
import logging
import threading
import datetime
import time

import click

from . import voevent as voe
from . import get_logger
from .__init__ import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0
        self.ndays: int = 7


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.command()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.option("--asassn", "-a", is_flag=True, help="Include ASAS-SN targets.")
@click.option("--fermi", "-f", is_flag=True, help="Include Fermi targets.")
@click.option("--swift", "-s", is_flag=True, help="Include Swift targets.")
@click.option("--ndays", "-n", type=int, default=7,
              help="Number of days to search.")
@click.option("--outcsv", "-o", type=click.Path(exists=False), 
              help="Output CSV filename.")
@pass_info
def cli(info: Info, verbose: int, 
        asassn: bool, fermi: bool, swift: bool,
        ndays: int, outcsv: str):
    """Run fpi2nite. 
    
    Default option loads events from the past seven days from all available 
    sources. Alternately, you can select individual data streams using flags.

    Output will be a CSV-formatted list with four columns:
    ISOT-EPOCH, RA, DEC, IDENTIFIER     
    """
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose

    log = get_logger(__name__)

    output_dicts = []

    # if using flags
    if asassn or fermi or swift:
        if asassn:
            if log.isEnabledFor(logging.INFO):
                log.info(f'Searching for ASASSN events from past {ndays} days.')
            asassn_events = voe.get_asassn(ndays=ndays)
            if log.isEnabledFor(logging.INFO):
                log.info(f'Found {len(asassn_events)} ASASSN events.')
            output_dicts.append(asassn_events)
      
        if fermi:
            if log.isEnabledFor(logging.INFO):
                log.info(f'Searching for Fermi-GBM events from past {ndays} days.')
            fermi_events = voe.get_fermi(ndays=ndays)
            if log.isEnabledFor(logging.INFO):
                log.info(f'Found {len(fermi_events)} Fermi-GBM events.')
            output_dicts.append(fermi_events)

        if swift:
            if log.isEnabledFor(logging.INFO):
                log.info(f'Searching for Swift-BAT events from past {ndays} days.')
            swift_events = voe.get_swift(ndays=ndays)
            if log.isEnabledFor(logging.INFO):
                log.info(f'Found {len(swift_events)} Swift-BAT events.')
            output_dicts.append(swift_events)

    # else do it all
    else:
        if log.isEnabledFor(logging.INFO):
            log.info(f'Searching for ASASSN events from past {ndays} days.')
        asassn_events = voe.get_asassn(ndays=ndays)
        if log.isEnabledFor(logging.INFO):
            log.info(f'Found {len(asassn_events)} ASASSN events.')
        output_dicts.append(asassn_events)

        if log.isEnabledFor(logging.INFO):
            log.info(f'Searching for Fermi-GBM events from past {ndays} days.')
        fermi_events = voe.get_fermi(ndays=ndays)
        if log.isEnabledFor(logging.INFO):
            log.info(f'Found {len(fermi_events)} Fermi-GBM events.')
        output_dicts.append(fermi_events)

        if log.isEnabledFor(logging.INFO):
            log.info(f'Searching for Swift-BAT events from past {ndays} days.')
        swift_events = voe.get_swift(ndays=ndays)
        if log.isEnabledFor(logging.INFO):
            log.info(f'Found {len(swift_events)} Swift-BAT events.')
        output_dicts.append(swift_events)

    # Write output
    if outcsv is None:
        now = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        outcsv = f'fpi2nite_{now}_m{ndays}_day.csv'
    
    with open(outcsv, 'w') as f:
        for obs in output_dicts:
            for event in obs:
                e = obs[event]
                f.write(f'{event}, {e["isot"]}, {e["ra"]}, {e["dec"]}\n')

