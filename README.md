# PyTkr

> Python program to update and display stock quotes every few minutes

## Description

This is a Python tkinter application that creates a window that displays
stock quotes. It can be left open in the corner of the screen all the
time for general non-distracting quote availability.

## Quote source

Currently, quotes are obtained by scraping the finance.yahoo.com web
pages. This is obviously fragile. Information may be delayed.  Moreover,
making too many requests might result in being blocked by Yahoo; for
that reason, the quote update rate is set to once per 5 minutes (with 5
quotes that amounts to one page load per minute).

It wouldn't be too hard to switch to an alternative source or paid
provider with an API. For example, AlphaVantage has an API that would be
worth a few bucks a month.  Unfortunately, it doesn't support index
tickers (^DJIA, ^IXIC), making it basically useless here.

## Running

If you have python3 with the packages in `requirements.txt` already
installed on your system, you can just run `./pytkr.py`.

If not, you might benefit from running it in a virtual environment.  To
do that, run `make` to create the virtual environment and use the
`./pytkr.sh` script to run it. Use `make clean` to get rid of it.

## Usage

A default list of symbols is built into the program. To use an alternate
set of symbols, list them on the command line.

Use the `-h` option to get help.

Use the `-w` option to start the program without a titlebar. You can
also toggle the titlebar off or on by pressing `w`.

Pressing `SPACE` or `ENTER` causes the program to update the quotes
immediately.

Pressing `q` or `CTRL+C` quits the program.

## Release History

* 0.1
    * Initial version

## To Do

## Meta

Curt McDowell \<coder#fishlet,com\>

Source: https://github.com/curtmcd/pytkr
