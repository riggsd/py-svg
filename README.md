# py-svg

A simple Python module for creating Scalable Vector Graphics (SVG).


# About

Just copy the [svg.py](svg.py) single file module, no need for dependencies,
and you'll probably want to add or tweak the API as this only covers the bits
of SVG that I happened to need.

The API closely follows the SVG spec, so you'll want to follow along with the
SVG Element Reference and SVG Attribute Reference documentation:
    https://developer.mozilla.org/en-US/docs/Web/SVG


# Example

This is an example of using the Python API to generate a bass guitar tablature
image [G_6_Em.svg](G_6_Em.svg):

```py
from svg import SVG

svg = SVG(width=700, height=500 fill='white')

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
svg.text('%s - %s %s - %s' % ('G', 'vi', 'Em', 'E, G, B'), (350,50), font_size='166%', text_anchor='middle', alignment_baseline='middle')

def fret(string, position):
    """Converts (string,fret) notation into (x,y) user coordinates"""
    x = (position + 1) * 100
    y = (4 - string) * 100
    return (x,y)

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
```

Produces this SVG document [G_6_Em.svg](G_6_Em.svg):

```xml
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="700" height="500" fill="white">
  <style>text { font-family: Helvetica, Arial, sans-serif; stroke: black; fill: black; }</style>
  <defs>
    <!-- NOTE MARKERS -->
    <g id="note_E">
      <circle cx="0" cy="0" r="20" fill="cyan" stroke="black" stroke-width="1" stroke-opacity="50%" />
      <text x="0" y="0" text-anchor="middle" alignment-baseline="middle">E</text>
    </g>
    <g id="note_G">
      <circle cx="0" cy="0" r="20" fill="magenta" stroke="black" stroke-width="1" stroke-opacity="50%" />
      <text x="0" y="0" text-anchor="middle" alignment-baseline="middle">G</text>
    </g>
    <g id="note_B">
      <circle cx="0" cy="0" r="20" fill="yellow" stroke="black" stroke-width="1" stroke-opacity="50%" />
      <text x="0" y="0" text-anchor="middle" alignment-baseline="middle">B</text>
    </g>
  </defs>
  <!-- TITLE -->
  <text x="350" y="50" font-size="166%" text-anchor="middle" alignment-baseline="middle">G - vi - Em - E, G, B</text>
  <g id="frets">
    <!-- FRETS -->
    <line x1="100" y1="100" x2="100" y2="400" stroke="darkgrey" stroke-width="2" id="fret_1" />
    <line x1="200" y1="100" x2="200" y2="400" stroke="darkgrey" stroke-width="2" id="fret_2" />
    <line x1="300" y1="100" x2="300" y2="400" stroke="darkgrey" stroke-width="2" id="fret_3" />
    <line x1="400" y1="100" x2="400" y2="400" stroke="darkgrey" stroke-width="4" id="fret_4" />
    <line x1="500" y1="100" x2="500" y2="400" stroke="darkgrey" stroke-width="2" id="fret_5" />
    <line x1="600" y1="100" x2="600" y2="400" stroke="darkgrey" stroke-width="4" id="fret_6" />
  </g>
  <g id="dots">
    <!-- DOTS -->
    <circle cx="350" cy="250" r="20" stroke="none" fill="lightgrey" id="dot_3" />
    <circle cx="550" cy="250" r="20" stroke="none" fill="lightgrey" id="dot_5" />
  </g>
  <!-- NUT -->
  <line x1="100" y1="97" x2="100" y2="403" stroke="black" stroke-width="16" id="nut" />
  <g id="strings">
    <!-- STRINGS -->
    <text x="25" y="100" font-size="133%" font-weight="bold" text-anchor="middle" alignment-baseline="middle">G</text>
    <line x1="100" y1="100" x2="700" y2="100" stroke="black" stroke-width="6" id="string_G" />
    <text x="25" y="200" font-size="133%" font-weight="bold" text-anchor="middle" alignment-baseline="middle">D</text>
    <line x1="100" y1="200" x2="700" y2="200" stroke="black" stroke-width="6" id="string_D" />
    <text x="25" y="300" font-size="133%" font-weight="bold" text-anchor="middle" alignment-baseline="middle">A</text>
    <line x1="100" y1="300" x2="700" y2="300" stroke="black" stroke-width="6" id="string_A" />
    <text x="25" y="400" font-size="133%" font-weight="bold" text-anchor="middle" alignment-baseline="middle">E</text>
    <line x1="100" y1="400" x2="700" y2="400" stroke="black" stroke-width="6" id="string_E" />
  </g>
  <g id="arpeggio">
    <!-- ARPEGGIO -->
    <use x="100" y="400" xlink:href="#note_E" />
    <use x="400" y="400" xlink:href="#note_G" />
    <use x="300" y="300" xlink:href="#note_B" />
    <use x="300" y="200" xlink:href="#note_E" />
    <use x="600" y="200" xlink:href="#note_G" />
    <use x="100" y="100" xlink:href="#note_G" />
    <use x="500" y="100" xlink:href="#note_B" />
  </g>
</svg>
```

![Rendered SVG Image](G_6_Em.svg?raw=true "G_6_Em.svg")
