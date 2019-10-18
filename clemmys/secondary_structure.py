import numpy as np
from matplotlib import patches as m_patches

from clemmys.colors import COLOR_SCHEME_SS


class SecondaryStructure:
    def __init__(self, ss_labels: list, x=0, y=0, helix_as_wave=True, width=2.,
                 color_scheme=COLOR_SCHEME_SS):
        """
        Plot secondary structure

        Parameters
        ----------
        ss_labels
            list of secondary structure labels to plot (in order)
            H: helix, E: sheet, T: turn, C: coil
        x
            start position on x-axis (default 0)
        y
            height on y-axis (default 0)
        helix_as_wave
            helix can be drawn as a wave (True) or as a rectangle (False)
            (default True)
        width
            width controller for all the elements (default 2)
        color_scheme
            specifies colors for each element
            must have keys: fc_helix, fc_sheet, fc_coil, fc_turn
            (default: see colors.py COLOR_SCHEME_SS)
        """
        self.ss_labels = ss_labels
        self.helix_as_wave = helix_as_wave
        self.ss_dict = {'H': 'H', 'G': 'H', 'I': 'H',
                        'B': 'E', 'E': 'E',
                        'T': 'T', 'S': 'T',
                        'C': 'C'}
        self.ss_blocks = self.get_continuous_ss_blocks()
        self.x = x
        self.y = y
        self.edgecolor = 'none'
        self.width = width  # General width controller
        self.edge_thickness = 1.0
        self.start_theta, self.end_theta = 0, 180

        # HELIX
        self.fc_helix = color_scheme["fc_helix"]

        # HELIX CYLINDER
        # Draw rectangle capped by two ellipses
        # Ellipse width = 1 residue
        self.helix_ellipse_length = self.width / 2  # horizontal diameter
        self.helix_ellipse_height = self.width - 0.001  # vertical axis (slight offset b/c of edge)
        self.helix_rectangle_height = self.width  # rectangle width is fraction of global

        # HELIX WAVE
        # Draw as consecutive elliptical arcs
        self.helix_arc_width = 2.0
        self.helix_arc_height = self.width
        self.helix_arc_length = 0.5

        # SHEET
        self.fc_sheet = color_scheme["fc_sheet"]
        self.sheet_thickness_factor = 2 / 3
        self.sheet_tail_height = self.width * self.sheet_thickness_factor
        self.sheet_head_height = self.width

        # TURN
        self.fc_turn = color_scheme["fc_turn"]
        self.turn_thickness_factor = 1 / 2
        self.turn_height = self.width

        # COIL
        self.fc_coil = color_scheme["fc_coil"]
        self.coil_thickness_factor = 0.8
        self.coil_height = self.width * self.coil_thickness_factor

    def get_continuous_ss_blocks(self):
        """
        Finds continuous stretches of the same ss label

        Returns
        -------
        list of tuples [(ss_label, start, length)]
        """
        ss_blocks = []
        prev_ss = None
        prev_i = 0
        for i, ss in enumerate(self.ss_labels):
            ss = self.ss_dict.get(ss, 'C')
            if prev_ss is None:
                prev_ss = ss
            if ss != prev_ss:
                ss_blocks.append((prev_ss, prev_i, i - 1))
                prev_ss = ss
                prev_i = i
        ss_blocks.append((self.ss_labels[-1], prev_i, len(self.ss_labels) - 1))
        return ss_blocks

    def make_patches(self):
        """
        Makes matplotlib patches for each ss stretch, with x starting at self.x and y at self.y

        Returns
        -------
        list of m_patches
        """
        patches = []
        for i, block in enumerate(self.ss_blocks):
            ss_type, start, end = block
            if ss_type == 'H':
                patches += self.make_helix(start, end)
            elif ss_type == 'E':
                patches.append(self.make_sheet(start, end))
            elif ss_type == 'T':
                patches.append(self.make_turn(start, end))
            elif ss_type == 'C':
                prev_ss, next_ss = None, None
                if i > 0:
                    prev_ss = self.ss_blocks[i - 1][0]
                if i + 1 < len(self.ss_blocks):
                    next_ss = self.ss_blocks[i + 1][0]
                patches.append(self.make_coil(start, end, prev_ss, next_ss))
        return patches

    def make_helix_ellipse(self, origin):
        return m_patches.Ellipse(origin,
                                 self.helix_ellipse_length,
                                 self.helix_ellipse_height,
                                 linewidth=self.edge_thickness,
                                 edgecolor='black',
                                 facecolor=self.fc_helix)

    def make_helix_rectangle(self, length, origin):
        return m_patches.Rectangle(origin, length, self.helix_rectangle_height,
                                   edgecolor='none', facecolor=self.fc_helix)

    def make_helix_arc(self, origin, start_theta, end_theta):
        return m_patches.Arc(origin,
                             self.helix_arc_length,
                             self.helix_arc_height,
                             linewidth=self.helix_arc_width,
                             # Add a bit to each angle to avoid sharp cuts
                             # that show as white lines in plot
                             theta1=start_theta - 1, theta2=end_theta + 1,
                             edgecolor=self.fc_helix)

    def make_helix_wave(self, start, end):
        patches = []
        start_theta, end_theta = self.start_theta, self.end_theta
        for arc_start in np.arange(start, end + 1, self.helix_arc_length):
            origin = (arc_start + 0.25 + self.x, self.helix_arc_height / 2 + self.y)
            patches.append(self.make_helix_arc(origin, start_theta, end_theta))
            start_theta += 180
            end_theta += 180
        return patches

    def make_helix_cylinder(self, start, end):
        patches = []
        # Origin is *center* of ellipse
        origin = (start + self.helix_ellipse_length / 2 + self.x,
                  self.helix_ellipse_height / 2 + self.y)
        # First ellipse
        patches.append(self.make_helix_ellipse(origin))

        # Rectangle(s)
        length = end - start + 1 - self.helix_ellipse_length  # deduct l of the ellipses
        origin = (start + self.helix_ellipse_length / 2 + self.x, self.y)  # origin is lower left: make it v-cntr
        patches.append(self.make_helix_rectangle(length, origin))

        # Second ellipse
        origin = (end + 1 - self.helix_ellipse_length / 2 + self.x, self.helix_ellipse_height / 2 + self.y)
        patches.append(self.make_helix_ellipse(origin))
        return patches

    def make_helix(self, start, end):
        if self.helix_as_wave:
            return self.make_helix_wave(start, end)
        else:
            return self.make_helix_cylinder(start, end)

    def make_sheet_fancy_arrow(self, start, length):
        return m_patches.FancyArrow(start + self.x, self.width / 2 + self.y,  # x, y of tail
                                    length, 0,  # dx, dy=0 -> flat arrow
                                    length_includes_head=True,
                                    head_length=length / 4,
                                    head_width=self.sheet_head_height - 0.001,
                                    width=self.sheet_tail_height,
                                    facecolor=self.fc_sheet,
                                    edgecolor=self.edgecolor,
                                    linewidth=self.edge_thickness)

    def make_sheet(self, start, end):
        length = end - start + 1
        return self.make_sheet_fancy_arrow(start, length)

    def make_turn_arc(self, origin, length):
        return m_patches.Arc(origin,
                             length,
                             self.turn_height,
                             linewidth=self.helix_arc_width,
                             # Add a bit to each angle to avoid sharp cuts
                             # that show as white lines in plot
                             theta1=self.start_theta, theta2=self.end_theta,
                             edgecolor=self.fc_turn)

    def make_turn(self, start, end):
        length = end - start + 1
        origin = (start + length / 2 + self.x, self.turn_height / 2 + self.y)
        return self.make_turn_arc(origin, length)

    def make_coil_connection(self, origin, length):
        return m_patches.ConnectionPatch(origin, (origin[0] + length, origin[1]),
                                         "data", "data",
                                         edgecolor=self.fc_coil,
                                         linewidth=self.coil_height)

    def make_coil(self, start, end, prev_ss, next_ss):
        # TODO: figure out what's going on here
        length = end - start + 1
        if prev_ss in ('H', 'T'):
            start -= 4 / 72
            length += 4 / 72
        elif prev_ss == 'E':
            start -= 0.5
            length += 0.5
        if next_ss in ('H', 'T'):
            length += 4 / 72
        elif next_ss == 'E':
            length += 0.5
        origin = (start + self.x, self.width / 2 + self.y)
        return self.make_coil_connection(origin, length)
