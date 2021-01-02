"""
A simple Python API for generating Scalable Vector Graphics (SVG)

See: https://developer.mozilla.org/en-US/docs/Web/SVG

2020-12-31 David A. Riggs <david.a.riggs@gmail.com>
"""

from contextlib import contextmanager
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

__all__ = 'SVG',


def _normalize(d):
    """Normalize Python kwargs to SVG XML attributes"""
    return {k.replace('_','-'):str(v) for k,v in d.items() if v is not None}


class SVG:
    """A Scalable Vector Graphics (SVG) document builder"""

    def __init__(self, width=None, height=None, preserveAspectRatio=None, viewBox:tuple=None, **kwargs):
        attrs = {
            'xmlns': 'http://www.w3.org/2000/svg',
            'xmlns:xlink': "http://www.w3.org/1999/xlink",
            'width': width, 'height': height, 'preserveAspectRatio': preserveAspectRatio,
            'viewBox': ' '.join(str(x) for x in viewBox) if viewBox else None,
            **kwargs,
        }
        self._root = Element('svg', _normalize(attrs))
        self._stack = [self._root]
    
    @property
    def parent(self) -> Element:
        """The current contextual parent element of the XML tree"""
        return self._stack[-1]
    
    def line(self, p1:tuple, p2:tuple, stroke='black', **kwargs):
        """Basic shape used to create a line connecting two points."""
        attrs = {
            'x1': p1[0], 'y1': p1[1],
            'x2': p2[0], 'y2': p2[1],
            'stroke': stroke,
            **kwargs,
        }
        SubElement(self.parent, 'line', _normalize(attrs))

    def rect(self, p:tuple, width=None, height=None, rx=None, ry=None, **kwargs):
        """Basic shape that draws rectangles, defined by their position, width, and height. The rectangles may have their corners rounded."""
        attrs = {
            'x': p[0], 'y': p[1],
            'height': height,'width': width,
            'rx': rx, 'ry': ry,
            **kwargs,
        }
        SubElement(self.parent, 'rect', _normalize(attrs))
    
    def circle(self, c:tuple, r, **kwargs):
        """Basic shape used to draw circles based on a center point and a radius."""
        attrs = {
            'cx': c[0], 'cy': c[1],
            'r': r,
            **kwargs,
        }
        SubElement(self.parent, 'circle', _normalize(attrs))
    
    def ellipse(self, c:tuple, rx=0, ry=0, **kwargs):
        """Basic shape used to create ellipses based on a center coordinate, and both their x and y radius."""
        attrs = {
            'cx': c[0], 'cy': c[1],
            'rx': rx, 'ry': ry,
            **kwargs,
        }
        SubElement(self.parent, 'circle', _normalize(attrs))
    
    def polyline(self, points:list[tuple], **kwargs):
        """Basic shape that creates straight lines connecting several points."""
        attrs = {
            'points': ', '.join(('%s %s' % (x,y)) for (x,y) in points),
            **kwargs,
        }
        SubElement(self.parent, 'polyline', _normalize(attrs))

    def polygon(self, points:list[tuple], **kwargs):
        """Basic closed shape consisting of a set of connected straight line segments. The last point is connected to the first point."""
        attrs = {
            'points': ', '.join(('%s %s' % (x,y)) for (x,y) in points),
            **kwargs,
        }
        SubElement(self.parent, 'polygon', _normalize(attrs))

    def text(self, txt:str, p:tuple, **kwargs):
        """Graphics element consisting of text."""
        attrs = {
            'x': p[0], 'y': p[1],
            **kwargs,
        }
        elem = SubElement(self.parent, 'text', _normalize(attrs))
        elem.text = txt

    def path(self, d:str, **kwargs):
        """Generic element to define a shape. TODO."""
        attrs = {
            'd': d,
            **kwargs,
        }
        SubElement(self.parent, 'path', _normalize(attrs))        
    
    def use(self, p:tuple, id:str, transform=None, **kwargs):
        """Takes nodes from within the SVG document, and duplicates them somewhere else."""
        attrs = {
            'x': p[0], 'y': p[1], 'transform': transform,
            'xlink:href': id if '://' in id else id if id.startswith('#') else '#'+id,
            **kwargs,
        }
        SubElement(self.parent, 'use', _normalize(attrs))

    def style(self, d:dict, **kwargs):
        elem = SubElement(self.parent, 'style', _normalize(kwargs))
        def pretty(d, indent='  '):
            lines = []
            lines.append('')
            for key, value in d.items():
                lines.append(indent + str(key) + ' {')
                if isinstance(value, dict):
                    for key2, value2 in value.items():
                        lines.append(indent*2 + '%s: %s;' % (key2, value2))
                else:
                    lines.append(indent*2 + str(value))
                lines.append(indent + '}')
            lines.append('')
            return '\n'.join(lines)
        elem.text = pretty(d)
    
    def comment(self, txt:str):
        """Inserts an XML comment into the SVG document."""
        self.parent.append(Comment(' %s ' % txt))
    
    @contextmanager
    def defs(self, **kwargs):
        """Used to store graphical objects that will be used at a later time."""
        try:
            yield self._stack.append(SubElement(self.parent, 'defs', _normalize(kwargs)))
        finally:
            self._stack.pop()
    
    @contextmanager
    def group(self, id:str, title:str=None, desc:str=None, **kwargs):
        """Container used to group other SVG elements."""
        attrs = {
            'id': id, 'title': title, 'desc': desc,
            **kwargs,
        }
        try:
            yield self._stack.append(SubElement(self.parent, 'g', _normalize(attrs)))
        finally:
            self._stack.pop()

    @contextmanager
    def symbol(self, id:str, width=None, height=None, viewBox:tuple=None, **kwargs):
        """Container used to define graphical template objects which can be instantiated by a <use> element."""
        attrs = {
            'id': id, 'width': width, 'height': height,
            'viewBox': ' '.join(str(x) for x in viewBox) if viewBox else None,
            **kwargs,
        }
        try:
            yield self._stack.append(SubElement(self.parent, 'symbol', _normalize(attrs)))
        finally:
            self._stack.pop()

    def __str__(self):
        return str(ElementTree.tostring(self._root, 'utf-8'), 'utf-8')


if __name__ == '__main__':

    #
    # This example renders an SVG bass guitar tablature
    #

    def fret(string, position):
        """Converts (string,fret) notation into (x,y) user coordinates"""
        x = (position + 1) * 100
        y = (4 - string) * 100
        return (x,y)
    
    svg = SVG(width=700, height=500, fill='white')

    svg.style({
        'text': {
            'font-family': 'Helvetica, Arial, sans-serif',
            'stroke': 'black',
            'fill': 'black',
        },
    })

    with svg.defs():
        svg.comment('NOTE MARKERS')
        with svg.group('note_E'):
            svg.circle((0,0), r=20, fill='cyan', stroke='black', stroke_width='1', stroke_opacity='50%')
            svg.text('E', (0,0), text_anchor='middle', alignment_baseline='middle')
        with svg.group('note_G'):
            svg.circle((0,0), r=20, fill='magenta', stroke='black', stroke_width='1', stroke_opacity='50%')
            svg.text('G', (0,0), text_anchor='middle', alignment_baseline='middle')
        with svg.group('note_B'):
            svg.circle((0,0), r=20, fill='yellow', stroke='black', stroke_width='1', stroke_opacity='50%')
            svg.text('B', (0,0), text_anchor='middle', alignment_baseline='middle')

    svg.comment('TITLE')
    svg.text('%s - %s - %s - %s' % ('G', 'vi', 'Em', 'E, G, B'), (350,50), font_size='166%', text_anchor='middle', alignment_baseline='middle')

    with svg.group('frets'):
        svg.comment('FRETS')
        for i in range(1,7):
            svg.line((i*100,100), (i*100,400), stroke='darkgrey', stroke_width=4 if i in {4,6} else 2, id='fret_%d'%i)

    with svg.group('dots'):
        svg.comment('DOTS')
        svg.circle((350, 250), 20, stroke='none', fill='lightgrey', id='dot_3')
        svg.circle((550, 250), 20, stroke='none', fill='lightgrey', id='dot_5')

    svg.comment('NUT')
    svg.line((100,100-3), (100,400+3), stroke_width=16, id='nut')

    with svg.group('strings'):
        svg.comment('STRINGS')
        for i, note in enumerate(reversed(['E', 'A', 'D', 'G'])):
            svg.text(note, (25,(i+1)*100), font_size='133%', font_weight='bold', text_anchor='middle', alignment_baseline='middle')
            svg.line((100,(i+1)*100), (700,(i+1)*100), stroke_width=6, id='string_'+note)

    with svg.group('arpeggio'):
        svg.comment('ARPEGGIO')
        svg.use(fret(0,0), 'note_E')
        svg.use(fret(0,3), 'note_G')
        svg.use(fret(1,2), 'note_B')
        svg.use(fret(2,2), 'note_E')
        svg.use(fret(2,5), 'note_G')
        svg.use(fret(3,0), 'note_G')
        svg.use(fret(3,4), 'note_B')

    print(svg)
