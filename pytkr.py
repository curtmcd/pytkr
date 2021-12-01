#!/usr/bin/env python3

import sys
import datetime
import getopt

from tkinter import *
from tkinter import font

#import qs_yahoo_bs as quote_service
import qs_yahoo_js as quote_service

#NAMES_DEFAULT = ['^DJI', '^IXIC', 'PSTG', 'DNP', 'AAL']
NAMES_DEFAULT = ['^DJI', 'GOOG', 'VIAC', 'HD', 'AAL', 'CCL']

# Update interval is pretty long by default.
# Careful when speeding it up, lest the quote service cuts us off.

UPDATE_INTERVAL_SEC = 5 * 60
UPDATE_INTERVAL_MSEC = UPDATE_INTERVAL_SEC * 1000

MARGIN_VERT = 20
MARGIN_HORZ = 20

SPACING_NAME_LAST = 20
SPACING_LAST_ARROW = 20
SPACING_ARROW_CHANGE = 10
SPACING_CHANGE_PCT = 40

FONT_FAMILY = 'helvetica'
FONT_SIZE = 24
FONT_WEIGHT = 'bold'

# Days of week and hours of day during which market should be polled

MONITOR_START_DAY = 0           # Monday
MONITOR_END_DAY = 4             # Friday

MONITOR_START_HOUR = 6.5        # Fixme: express in EST
MONITOR_END_HOUR = 13.3

# Columns are Name, Last, Arrow, Change, Percent Change

FORMAT_NAME = '%s'
FORMAT_LAST = '%.2f '
FORMAT_ARROW = '%s'
FORMAT_CHANGE = '%.2f'
FORMAT_PCT = '%.1f%%'

WIDEST_NAME = 'WWWW'
WIDEST_LAST = 99999.99
WIDEST_ARROW = 'W'
WIDEST_CHANGE = -99.99
WIDEST_PCT = -99.9

COLOR_BG = '#000032'
COLOR_NAME = '#3c3cff'
COLOR_LAST = '#ff5a14'
COLOR_UP = '#00ff00'
COLOR_DOWN = '#ff0000'

def in_monitor_window():
    now = datetime.datetime.now()
    wday = now.weekday()
    hour = now.hour + now.minute / 60 + now.second / 3600
    return (wday >= MONITOR_START_DAY and wday <= MONITOR_END_DAY and
            hour >= MONITOR_START_HOUR and hour <= MONITOR_END_HOUR)

class Symbol:
    def __init__(self, name):
        self.name = name
        self.last = 0
        self.change = 0
        self.pct = 0
    def update(self):
        print('update %s' % self.name)
        self.last, self.change, self.pct = quote_service.quote(self.name)

class App:
    def __init__(self, symbols, titlebar=True):
        self.symbols = symbols
        self.force_update = True

        self.root = Tk()
        self.root.geometry("-0+30")
        self.root.bind("<Key>", self.key_event)
        self.root.title('TkTicker')
        self.titlebar = titlebar
        self.set_titlebar(titlebar)

        # Note: can't get font until after Tk()
        #print(font.families())
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE, weight=FONT_WEIGHT)

        self.canvas = Canvas(self.root, highlightthickness=0)

        self.w_name, self.h_name = self.text_size(FORMAT_NAME % WIDEST_NAME)
        self.w_last, self.h_last = self.text_size(FORMAT_LAST % WIDEST_LAST)
        self.w_arrow, self.h_arrow = self.text_size(FORMAT_ARROW % WIDEST_ARROW)
        self.w_change, self.h_change = self.text_size(FORMAT_CHANGE % WIDEST_CHANGE)
        self.w_pct, self.h_pct = self.text_size(FORMAT_PCT % WIDEST_PCT)

        self.x_name = MARGIN_HORZ
        self.x_last = self.x_name + self.w_name + SPACING_NAME_LAST
        self.x_arrow = self.x_last + self.w_last + SPACING_LAST_ARROW
        self.x_change = self.x_arrow + self.w_arrow + SPACING_ARROW_CHANGE
        self.x_pct = self.x_change + self.w_change + SPACING_CHANGE_PCT

        self.y_row = lambda row: MARGIN_VERT + row * self.h_name

        self.w_win = self.x_pct + self.w_pct + MARGIN_HORZ
        self.h_win = MARGIN_VERT + len(self.symbols) * self.h_name + MARGIN_VERT

        self.canvas.config(width=self.w_win, height=self.h_win, background=COLOR_BG)
        self.canvas.pack()

        self.timer = None
        self.update()

    def text_size(self, text):
        item = self.canvas.create_text((0, 0), font=self.font, text=text)
        x0, y0, x1, y1 = self.canvas.bbox(item)
        size = (x1 - x0, y1 - y0)
        self.canvas.delete(item)
        return size

    def set_titlebar(self, titlebar):
        self.titlebar = titlebar
        if self.titlebar:
            self.root.wm_attributes('-type', 'normal')
        else:
            self.root.wm_attributes('-type', 'splash')

    def key_event(self, event):
        if len(event.char) > 0:
            lc = event.char.lower()
            if lc == 'q' or ord(lc) == 3:               # Quit
                self.root.destroy()
            elif lc == ' ' or ord(lc) == 13:            # Refresh quotes
                self.root.after_cancel(self.timer)
                self.timer = None
                self.update()
            elif lc == 'w':                             # Toggle titlebar
                self.set_titlebar(not self.titlebar)

    def run(self):
        self.root.mainloop()

    # Update function sets a timer to be called again after update interval
    def update(self):
        if self.force_update or in_monitor_window():
            for sym in self.symbols:
                sym.update()
            self.force_update = False

        self.canvas.delete("all")

        for row, sym in enumerate(self.symbols):
            def ct(x_col, anchor, color, text):
                self.canvas.create_text((x_col, self.y_row(row)),
                                        anchor=anchor, fill=color,
                                        font=self.font, text=text)

            color_chg = COLOR_UP if sym.change >= 0 else COLOR_DOWN
            arr_text = u'\u2b61' if sym.change >= 0 else u'\u2b63'

            ct(self.x_name, NW, COLOR_NAME, FORMAT_NAME % sym.name)
            ct(self.x_last + self.w_last, NE, COLOR_LAST, FORMAT_LAST % sym.last)
            ct(self.x_arrow, NW, color_chg, FORMAT_ARROW % arr_text)
            ct(self.x_change, NW, color_chg, FORMAT_CHANGE % sym.change)
            ct(self.x_pct, NW, color_chg, FORMAT_PCT % sym.pct)

        self.timer = self.root.after(UPDATE_INTERVAL_MSEC, self.update)

def usage():
    print("""Usage: pytkr [-h] [-w] [<sym> ...]
   -h       help
   -w       exclude titlebar (press 'w' to toggle)
Key controls:
   w        toggle titlebar
   <space>  update
   q        quit""", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1 :], 'hw', ['help'])
    except getopt.GetoptError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    titlebar = True

    for o, a in opts:
        if o in ['-h', '--help']:
            usage()
        if o == '-w':
            titlebar = False

    names = args if len(args) > 0 else NAMES_DEFAULT
    symbols = [Symbol(name) for name in names]

    App(symbols, titlebar=titlebar).run()
