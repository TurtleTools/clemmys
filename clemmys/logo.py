from collections import Counter

import numpy as np

from clemmys.colors import COLOR_SCHEME_AA
from clemmys.glyph import Glyph

"""
Code adapted from https://github.com/jbkinney/logomaker"
"""


class SequenceLogo:
    """
    class to make sequence logos (displaying percentage of occurrence of amino acids)
    """

    def __init__(self, alignment: dict, positions=None, keys=None, color_scheme: dict = COLOR_SCHEME_AA,
                 gap_character='X', space_between_glyphs=1, glyph_width=1):
        """
        Parameters
        ----------
        alignment
            dict of keys to aligned sequences
        positions
            give a list to restrict positions (None => all positions)
        keys
            give a list to restrict keys (None => all keys used)
        color_scheme
            dict of amino acid one letter code to color ('-' colors gaps)
        gap_character
            character to represent gaps
        space_between_glyphs
        glyph_width
        """
        self.alignment = alignment
        if keys is None:
            self.keys = list(alignment.keys())
        else:
            self.keys = keys
        self.alignment_length = len(self.alignment[self.keys[0]])
        self.num_keys = len(self.keys)
        if positions is None:
            self.positions = list(range(self.alignment_length))
        else:
            self.positions = list(positions)
        self.color_scheme = color_scheme
        self.gap_character = gap_character
        self.space_between_glyphs = space_between_glyphs
        self.glyph_width = glyph_width
        self.counters = self.get_counters()

    def get_counters(self):
        counters = []
        for p in self.positions:
            counters.append(Counter([self.alignment[key][p].upper().replace('-', self.gap_character) for key in self.keys]))
        return counters

    def make_patches(self) -> list:
        """
        get patches for matplotlib plotting

        Returns
        -------
        list of patches
        """
        patches = []
        for x, counter in enumerate(self.counters):
            y1 = 1
            for c, n in counter.most_common():
                y0 = y1 - n / self.num_keys
                glyph = Glyph(c, self.space_between_glyphs * x, y0, y1,
                              width=self.glyph_width, color=self.color_scheme[c])
                patches.append(glyph.make_patch())
        return patches

    def get_xticks_labels(self):
        """
        Labels positions

        Returns
        -------
        xticks, xticklabels
        """
        xticks = np.arange(-1, self.space_between_glyphs * len(self.positions))
        xticklabels = [' ']
        for p in self.positions:
            xticklabels.append(str(p))
            xticklabels += [' '] * self.space_between_glyphs
        return xticks, xticklabels


class CoevolutionLogo:
    """
    class to make co-evolution logos (displaying percentage of occurrence of pairs of amino acids)
    """

    def __init__(self, alignment: dict, coevolving_positions: list, keys=None,
                 color_scheme: dict = COLOR_SCHEME_AA, gap_character='X',
                 space_between_glyphs=1, glyph_width=1):
        """
        Parameters
        ----------
        alignment
            dict of keys to aligned sequences
        coevolving_positions
            give a list of tuples to restrict positions
        keys
            give a list to restrict keys (None => all keys used)
        color_scheme
            dict of amino acid one letter code to color ('-' colors gaps)
        gap_character
            character to represent gaps
        space_between_glyphs
        glyph_width
        """
        self.alignment = alignment
        if keys is None:
            self.keys = list(alignment.keys())
        else:
            self.keys = [k for k in keys if k in alignment]
        self.alignment_length = len(self.alignment[self.keys[0]])
        self.num_keys = len(self.keys)
        self.coevolving_positions = coevolving_positions
        self.color_scheme = color_scheme
        self.gap_character = gap_character
        self.space_between_glyphs = space_between_glyphs
        self.glyph_width = glyph_width
        self.counters = self.get_counters()

    def get_counters(self):
        counters = []
        for p1, p2 in self.coevolving_positions:
            counters.append(
                Counter([f"{self.alignment[key][p1]}{self.alignment[key][p2]}".upper().replace('-', self.gap_character) for key in self.keys]))
        return counters

    def make_patches(self):
        """
        get patches for matplotlib plotting

        Returns
        -------
        list of patches
        """
        patches = []
        for x, counter in enumerate(self.counters):
            y1 = 1
            for c, n in counter.most_common():
                y0 = y1 - n / self.num_keys
                glyph_1 = Glyph(c[0], 2 * self.space_between_glyphs * x, y0, y1,
                                width=self.glyph_width, color=self.color_scheme[c[0]])
                glyph_2 = Glyph(c[1], 2 * self.space_between_glyphs * x + 1, y0, y1,
                                width=self.glyph_width, color=self.color_scheme[c[1]])
                patches.append(glyph_1.make_patch())
                patches.append(glyph_2.make_patch())
        return patches

    def get_xticks_labels(self):
        """
        Labels positions

        Returns
        -------
        xticks, xticklabels
        """
        xticks = np.arange(-1, self.space_between_glyphs * len(self.coevolving_positions) * 3)
        xticklabels = [' ']
        for p1, p2 in self.coevolving_positions:
            xticklabels += [str(p1), ' ', str(p2)] + [' '] * self.space_between_glyphs
        return xticks, xticklabels
