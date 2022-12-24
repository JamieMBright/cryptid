"""
Keyboard press converter
"""
import logging
import pygame as pg

# get the logger
logger = logging.getLogger(__name__)


def key_interpreter(key):
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
        return key
