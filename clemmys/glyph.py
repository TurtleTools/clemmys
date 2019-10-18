import typing
from dataclasses import dataclass

from matplotlib import patches as m_patches
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from matplotlib.transforms import Bbox, Affine2D


@dataclass
class Glyph:
    character: chr
    x: float
    y0: float
    y1: float
    width: float = 0.95
    pad: float = 0.1
    font_name: str = 'sans'
    font_weight: str = 'normal'
    color: str = 'gray'
    edgecolor: str = 'black'
    edgewidth: float = 0.
    dont_stretch_more_than: chr = 'E'
    zorder: typing.Union[None, int] = None
    opacity: float = 1.

    def make_patch(self):
        height = self.y1 - self.y0
        # If height is zero, return None
        if height == 0.0:
            return None

        # Set bounding box for character,
        # leaving requested amount of padding above and below the character
        char_xmin = self.x - self.width / 2.0
        char_ymin = self.y0 + self.pad * height / 2.0
        char_width = self.width
        char_height = height - self.pad * height
        bbox = Bbox.from_bounds(char_xmin,
                                char_ymin,
                                char_width,
                                char_height)

        # Set font properties of Glyph
        font_properties = FontProperties(family=self.font_name,
                                         weight=self.font_weight)

        # Create a path for Glyph that does not yet have the correct
        # position or scaling
        tmp_path = TextPath((0, 0), self.character,
                            size=1,
                            prop=font_properties)

        # Create create a corresponding path for a glyph representing
        # the max stretched character
        msc_path = TextPath((0, 0), self.dont_stretch_more_than, size=1,
                            prop=font_properties)

        # Get bounding box for temporary character and max_stretched_character
        tmp_bbox = tmp_path.get_extents()
        msc_bbox = msc_path.get_extents()

        # Compute horizontal stretch factor needed for tmp_path
        hstretch_tmp = bbox.width / tmp_bbox.width

        # Compute horizontal stretch factor needed for msc_path
        hstretch_msc = bbox.width / msc_bbox.width

        # Choose the MINIMUM of these two horizontal stretch factors.
        # This prevents very narrow characters, such as 'I', from being
        # stretched too much.
        hstretch = min(hstretch_tmp, hstretch_msc)

        # Compute the new character width, accounting for the
        # limit placed on the stretching factor
        char_width = hstretch * tmp_bbox.width

        # Compute how much to horizontally shift the character path
        char_shift = (bbox.width - char_width) / 2.0

        # Compute vertical stetch factor needed for tmp_path
        vstretch = bbox.height / tmp_bbox.height

        # THESE ARE THE ESSENTIAL TRANSFORMATIONS
        # 1. First, translate char path so that lower left corner is at origin
        # 2. Then scale char path to desired width and height
        # 3. Finally, translate char path to desired position
        # char_path is the resulting path used for the Glyph
        transformation = Affine2D() \
            .translate(tx=-tmp_bbox.xmin, ty=-tmp_bbox.ymin) \
            .scale(sx=hstretch, sy=vstretch) \
            .translate(tx=bbox.xmin + char_shift, ty=bbox.ymin)
        char_path = transformation.transform_path(tmp_path)

        # Convert char_path to a patch, which can now be drawn on demand
        return m_patches.PathPatch(char_path,
                                   facecolor=self.color,
                                   zorder=self.zorder,
                                   alpha=self.opacity,
                                   edgecolor=self.edgecolor,
                                   linewidth=self.edgewidth)
