"""
Test the keyboard events.
"""
import pygame as pg
from cryptids.keyboard import key_interpreter as ki


def test_key_interpreter_letters():
    """Test the letter presses."""
    assert ki(pg.K_a) == "a"
    assert ki(pg.K_b) == "b"
    assert ki(pg.K_c) == "c"
    assert ki(pg.K_d) == "d"
    assert ki(pg.K_e) == "e"
    assert ki(pg.K_f) == "f"
    assert ki(pg.K_g) == "g"
    assert ki(pg.K_h) == "h"
    assert ki(pg.K_i) == "i"
    assert ki(pg.K_j) == "j"
    assert ki(pg.K_k) == "k"
    assert ki(pg.K_l) == "l"
    assert ki(pg.K_m) == "m"
    assert ki(pg.K_n) == "n"
    assert ki(pg.K_o) == "o"
    assert ki(pg.K_p) == "p"
    assert ki(pg.K_q) == "q"
    assert ki(pg.K_r) == "r"
    assert ki(pg.K_s) == "s"
    assert ki(pg.K_t) == "t"
    assert ki(pg.K_u) == "u"
    assert ki(pg.K_v) == "v"
    assert ki(pg.K_w) == "w"
    assert ki(pg.K_x) == "x"
    assert ki(pg.K_y) == "y"
    assert ki(pg.K_z) == "z"


def test_key_interpreter_numbers():
    """Test the number presses."""
    assert ki(pg.K_0) == str(0)
    assert ki(pg.K_1) == str(1)
    assert ki(pg.K_2) == str(2)
    assert ki(pg.K_3) == str(3)
    assert ki(pg.K_4) == str(4)
    assert ki(pg.K_5) == str(5)
    assert ki(pg.K_6) == str(6)
    assert ki(pg.K_7) == str(7)
    assert ki(pg.K_8) == str(8)
    assert ki(pg.K_9) == str(9)


def test_key_interpreter_other():
    """Test the other presses."""
    assert ki(pg.K_SPACE) == "space"
    assert ki(pg.K_RETURN) == "return"
    assert ki(pg.K_ESCAPE) == "esc"
    assert ki(pg.K_BACKSPACE) == "backspace"
