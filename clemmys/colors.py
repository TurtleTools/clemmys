LIGHTGREEN = "#94CD8C"
GREEN = "#B7D885"
DARKGREEN = "#6FB344"
BLUE = "#7FBBE6"
PURPLE = "#999FD0"
DARKBLUE = "#5569B1"
ORANGE = "#F9CC89"
PINK = "#E7BAB9"
RED = "#ED5961"
BLACK = "black"
LIGHTBLUE = "lightsteelblue"
GRAY = "#747274"

COLOR_SCHEME_AA = {'A, G': LIGHTGREEN,
                   'C': GREEN,
                   'D, E, N, Q': DARKGREEN,
                   'I, L, M, V': BLUE,
                   'F, W, Y': PURPLE,
                   'H': DARKBLUE,
                   'K, R': ORANGE,
                   'P': PINK,
                   'S, T': RED,
                   'X': BLACK}
COLOR_SCHEME_AA = {c1: COLOR_SCHEME_AA[c] for c in COLOR_SCHEME_AA for c1 in c.split(', ')}

COLOR_SCHEME_SS = {
    "fc_helix": LIGHTBLUE,
    "fc_sheet": PURPLE,
    "fc_turn": GRAY,
    "fc_coil": GRAY,
}
