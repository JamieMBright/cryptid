"""
Keyboard press converter.

To do: !!!
----------
Need a letter/type input.
"""
import logging
import sys

import pygame as pg

import cryptids.settings as get

# get the logger
logger = logging.getLogger(__name__)
if get.VERBOSE:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

"""
pygame
Constant      ASCII   Description
---------------------------------
K_BACKSPACE   \b      backspace
K_TAB         \t      tab
K_CLEAR               clear
K_RETURN      \r      return
K_PAUSE               pause
K_ESCAPE      ^[      escape
K_SPACE               space
K_EXCLAIM     !       exclaim
K_QUOTEDBL    "       quotedbl
K_HASH        #       hash
K_DOLLAR      $       dollar
K_AMPERSAND   &       ampersand
K_QUOTE               quote
K_LEFTPAREN   (       left parenthesis
K_RIGHTPAREN  )       right parenthesis
K_ASTERISK    *       asterisk
K_PLUS        +       plus sign
K_COMMA       ,       comma
K_MINUS       -       minus sign
K_PERIOD      .       period
K_SLASH       /       forward slash
K_0           0       0
K_1           1       1
K_2           2       2
K_3           3       3
K_4           4       4
K_5           5       5
K_6           6       6
K_7           7       7
K_8           8       8
K_9           9       9
K_COLON       :       colon
K_SEMICOLON   ;       semicolon
K_LESS        <       less-than sign
K_EQUALS      =       equals sign
K_GREATER     >       greater-than sign
K_QUESTION    ?       question mark
K_AT          @       at
K_LEFTBRACKET [       left bracket
K_BACKSLASH   \       backslash
K_RIGHTBRACKET ]      right bracket
K_CARET       ^       caret
K_UNDERSCORE  _       underscore
K_BACKQUOTE   `       grave
K_a           a       a
K_b           b       b
K_c           c       c
K_d           d       d
K_e           e       e
K_f           f       f
K_g           g       g
K_h           h       h
K_i           i       i
K_j           j       j
K_k           k       k
K_l           l       l
K_m           m       m
K_n           n       n
K_o           o       o
K_p           p       p
K_q           q       q
K_r           r       r
K_s           s       s
K_t           t       t
K_u           u       u
K_v           v       v
K_w           w       w
K_x           x       x
K_y           y       y
K_z           z       z
K_DELETE              delete
K_KP0                 keypad 0
K_KP1                 keypad 1
K_KP2                 keypad 2
K_KP3                 keypad 3
K_KP4                 keypad 4
K_KP5                 keypad 5
K_KP6                 keypad 6
K_KP7                 keypad 7
K_KP8                 keypad 8
K_KP9                 keypad 9
K_KP_PERIOD   .       keypad period
K_KP_DIVIDE   /       keypad divide
K_KP_MULTIPLY *       keypad multiply
K_KP_MINUS    -       keypad minus
K_KP_PLUS     +       keypad plus
K_KP_ENTER    \r      keypad enter
K_KP_EQUALS   =       keypad equals
K_UP                  up arrow
K_DOWN                down arrow
K_RIGHT               right arrow
K_LEFT                left arrow
K_INSERT              insert
K_HOME                home
K_END                 end
K_PAGEUP              page up
K_PAGEDOWN            page down
K_F1                  F1
K_F2                  F2
K_F3                  F3
K_F4                  F4
K_F5                  F5
K_F6                  F6
K_F7                  F7
K_F8                  F8
K_F9                  F9
K_F10                 F10
K_F11                 F11
K_F12                 F12
K_F13                 F13
K_F14                 F14
K_F15                 F15
K_NUMLOCK             numlock
K_CAPSLOCK            capslock
K_SCROLLOCK           scrollock
K_RSHIFT              right shift
K_LSHIFT              left shift
K_RCTRL               right control
K_LCTRL               left control
K_RALT                right alt
K_LALT                left alt
K_RMETA               right meta
K_LMETA               left meta
K_LSUPER              left Windows key
K_RSUPER              right Windows key
K_MODE                mode shift
K_HELP                help
K_PRINT               print screen
K_SYSREQ              sysrq
K_BREAK               break
K_MENU                menu
K_POWER               power
K_EURO                Euro
K_AC_BACK             Android back button

pygame
Constant      Description
-------------------------
KMOD_NONE     no modifier keys pressed
KMOD_LSHIFT   left shift
KMOD_RSHIFT   right shift
KMOD_SHIFT    left shift or right shift or both
KMOD_LCTRL    left control
KMOD_RCTRL    right control
KMOD_CTRL     left control or right control or both
KMOD_LALT     left alt
KMOD_RALT     right alt
KMOD_ALT      left alt or right alt or both
KMOD_LMETA    left meta
KMOD_RMETA    right meta
KMOD_META     left meta or right meta or both
KMOD_CAPS     caps lock
KMOD_NUM      num lock
KMOD_MODE     AltGr
"""


def key_interpreter(key, mods=None):
    """
    Convert a key press into python interpretable.
    """
    schemer = {
        pg.K_a: "a",
        pg.K_b: "b",
        pg.K_c: "c",
        pg.K_d: "d",
        pg.K_e: "e",
        pg.K_f: "f",
        pg.K_g: "g",
        pg.K_h: "h",
        pg.K_i: "i",
        pg.K_j: "j",
        pg.K_k: "k",
        pg.K_l: "l",
        pg.K_m: "m",
        pg.K_n: "n",
        pg.K_o: "o",
        pg.K_p: "p",
        pg.K_q: "q",
        pg.K_r: "r",
        pg.K_s: "s",
        pg.K_t: "t",
        pg.K_u: "u",
        pg.K_v: "v",
        pg.K_w: "w",
        pg.K_x: "x",
        pg.K_y: "y",
        pg.K_z: "z",
        pg.K_0: str(0),
        pg.K_1: str(1),
        pg.K_2: str(2),
        pg.K_3: str(3),
        pg.K_4: str(4),
        pg.K_5: str(5),
        pg.K_6: str(6),
        pg.K_7: str(7),
        pg.K_8: str(8),
        pg.K_9: str(9),
        pg.K_ESCAPE: "esc",
        pg.K_SPACE: "space",
        pg.K_RETURN: "return",
        pg.K_BACKSPACE: "backspace",
        pg.K_UP: "up",
        pg.K_DOWN: "down",
        pg.K_LEFT: "left",
        pg.K_RIGHT: "right",
    }

    if key in schemer.keys():
        return schemer[key]
    else:
        logger.debug(f"Unrecognised key with pygame code: {key}.")
        return "WTF?!"
