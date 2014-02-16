
from optparse import OptionParser


class svgClass:
    def __init__(self, thickness_mm=5, material_width_mm = 320, material_height_mm = 600, pixel_ratio = 10, spacer_p = 64):
        self.thickness_mm = thickness_mm
        self.material_width_mm = material_width_mm
        self.material_height_mm = material_height_mm
        self.pixel_ratio = pixel_ratio
        pixel_h = material_height_mm * pixel_ratio
        pixel_w = material_width_mm * pixel_ratio 
        self.svg = '<svg xmlns="http://www.w3.org/2000/svg" baseProfile="full" '
        self.svg += 'height="' + str(material_height_mm) + 'mm" width="' + str(material_width_mm)
        self.svg += 'mm" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" '
        self.svg +=  'viewBox="0 0 ' + str(pixel_w) + ' ' + str(pixel_h) + '">'
        self.current_offset_width = spacer_p
        self.current_offset_height = spacer_p
        self.spacer_p = spacer_p
        self.stroke = 'stroke="blue" stroke-width="1mm" fill="none"'

    def append(self, svgtxt):
        self.svg += svgtxt
    def dump(self):
        return self.svg + "\n</svg>"

    def path(self, points, direction = "stet"):
        line_start = '<path ' + self.stroke + ' id="h" d="'
        line_end = ' " />\n'
        max_x = 0
        max_y = 0

        self.svg += line_start
        (first_point_x, first_point_y) = points.pop(0)
        self.svg += 'M ' + str((first_point_x*self.pixel_ratio)+self.current_offset_width) + ' ' + str((first_point_y*self.pixel_ratio)+self.current_offset_height)
        for point in points:
            (x,y) = point
            if x>max_x:
                max_x = x
            if y>max_y:
                max_y = y
            self.svg += 'L ' + str((x*self.pixel_ratio) +self.current_offset_width) + ' ' + str((y*self.pixel_ratio)+self.current_offset_height)
        self.svg += line_end
        if direction == "right":
            self.current_offset_width += max_x*self.pixel_ratio + self.spacer_p
        if direction == "right_and_a_bit":
            self.current_offset_width += max_x*self.pixel_ratio + self.spacer_p + self.thickness_mm*self.pixel_ratio
        if direction == "down":
            self.current_offset_height += max_y*self.pixel_ratio + self.spacer_p
        if direction == "down_and_zero":
            self.current_offset_height += max_y*self.pixel_ratio + self.spacer_p
            self.current_offset_width = self.spacer_p

    def circle(self, x, y, diameter_mm):
        r = diameter_mm * self.pixel_ratio / 2 
        self.svg += '<circle cx="' + str((x*self.pixel_ratio)+self.current_offset_width+r) + '" cy="' + str((y*self.pixel_ratio)+self.current_offset_height+r) + '" r="' + str(r) + '" ' + self.stroke + '/>'


def flip_points(points):
    flip = []
    for point in points:
        (x,y) = point
        flip.append((y,x))
    return flip

def mirror_points(points, mirror):
    flip = []
    (m_x, m_y) = mirror
    if m_y == 0:
        for point in points:
            (x,y) = point
            flip.append((m_x - x, y))
    else:
        if m_x == 0:
            for point in points:
                (x,y) = point
                flip.append((x, m_y - y))
        else:
            for point in points:
                (x,y) = point
                flip.append((x, m_y - y))
    return flip

def bolt_hole(svg, offset_in_from_edge = 0, offset_along_from_edge = 0, along = False):
    if along:
        svg.circle(svg.thickness_mm*2+offset_in_from_edge, offset_along_from_edge-float(svg.thickness_mm)/2, svg.thickness_mm)
    else:
        svg.circle(offset_along_from_edge-float(svg.thickness_mm)/2, svg.thickness_mm*2+offset_in_from_edge, svg.thickness_mm)

def bolt_hold(svg, offset_in_from_edge = 0, offset_along_from_edge = 0, length = 100, along = False, mirror = (0,0) ):
    t = svg.thickness_mm
    offset_along_from_edge = offset_along_from_edge-float(svg.thickness_mm)/2 
    path = []
    path.append((offset_along_from_edge+t*0,offset_in_from_edge+t*0))
    path.append((offset_along_from_edge+t*0,offset_in_from_edge+t*2))
    path.append((offset_along_from_edge+t*-2,offset_in_from_edge+t*2))
    path.append((offset_along_from_edge+t*-2,offset_in_from_edge+t*4))
    path.append((offset_along_from_edge+t*-1,offset_in_from_edge+t*4))
    path.append((offset_along_from_edge+t*-1,offset_in_from_edge+t*3))
    path.append((offset_along_from_edge+t*0,offset_in_from_edge+t*3))
    path.append((offset_along_from_edge+t*0,offset_in_from_edge+t*5))
    path.append((offset_along_from_edge+t*1,offset_in_from_edge+t*5))
    path.append((offset_along_from_edge+t*1,offset_in_from_edge+t*3))
    path.append((offset_along_from_edge+t*2,offset_in_from_edge+t*3))
    path.append((offset_along_from_edge+t*2,offset_in_from_edge+t*4))
    path.append((offset_along_from_edge+t*3,offset_in_from_edge+t*4))
    path.append((offset_along_from_edge+t*3,offset_in_from_edge+t*2))
    path.append((offset_along_from_edge+t*1,offset_in_from_edge+t*2))
    path.append((offset_along_from_edge+t*1,offset_in_from_edge+t*0))
    path.append((offset_along_from_edge+t*0,offset_in_from_edge+t*0))
    if along:
        path = flip_points(path)
    if mirror <> (0,0) :
        path = mirror_points(path, mirror)
    svg.path(path)

def slot(svg, offset_in_from_edge = 0, offset_along_from_edge = 0, length = 100, along = True):
    t = svg.thickness_mm
    offset_along_from_edge = offset_along_from_edge
    length = length # fudge!
    # top corner
    path = []
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+t*0))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+t*0))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+t*1))
    path.append((offset_in_from_edge+t*3,offset_along_from_edge+t*1))
    path.append((offset_in_from_edge+t*3,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+length))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+length))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*2,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*2,offset_along_from_edge+t*1))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+t*1))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+t*0))
    if not along:
        path = flip_points(path)
    svg.path(path)

def tab(svg, offset_in_from_edge = 0, offset_along_from_edge = 0, length = 100, along = True, mirror = (0,0) ):
    t = svg.thickness_mm
    path = []
    path.append((offset_in_from_edge+t*0,offset_along_from_edge+t*0))
    path.append((offset_in_from_edge+t*0,offset_along_from_edge+length+t*0))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+length+t*0))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+t*0))
    path.append((offset_in_from_edge+t*0,offset_along_from_edge+t*0))

    if not along:
        path = flip_points(path)
    if mirror <> (0,0) :
        path = mirror_points(path, mirror)
    svg.path(path)


def set_of_slots(svg, total_length, number_sets = 2, along = True, offset_in_from_edge = 0, offset_along_from_edge = 0):
    gap = float(total_length) / (number_sets*2 + 1)
#    print gap
    # First hole - always
    bolt_hole(svg, offset_along_from_edge=gap*0.5+offset_along_from_edge, along = along, offset_in_from_edge = offset_in_from_edge)

    # per set 
    for s in range (1, number_sets+1):
        slot(svg, offset_along_from_edge=gap*(s*2 - 1)+offset_along_from_edge, length = gap, along = along, offset_in_from_edge = offset_in_from_edge)
        bolt_hole(svg, offset_along_from_edge=gap*(s*2+0.5)+offset_along_from_edge, along = along, offset_in_from_edge = offset_in_from_edge)

def set_of_tabs(svg, total_length, number_sets = 2, along = True, offset_in_from_edge = 0, offset_along_from_edge = 0, mirror = (0,0) ):
    gap = float(total_length) / (number_sets*2 + 1)
#    print gap
    # First hole - always
    bolt_hold(svg, offset_along_from_edge=gap*0.5+offset_along_from_edge, along = along, offset_in_from_edge = offset_in_from_edge+svg.thickness_mm, mirror = mirror)

    # per set 
    for s in range (1, number_sets+1):
        tab(svg, offset_along_from_edge=gap*(s*2 - 1)+offset_along_from_edge, length = gap, along = along, offset_in_from_edge = offset_in_from_edge, mirror = mirror)
        bolt_hold(svg, offset_along_from_edge=gap*(s*2+0.5)+offset_along_from_edge, along = along, offset_in_from_edge = offset_in_from_edge+svg.thickness_mm, mirror = mirror)



def base(svg, direction = ""):
#    length = 300
#    length_back = 200
    length = 150
    length_back = 100
    set_of_slots(svg, length_back, 2, along = True, offset_in_from_edge = 0)
    set_of_slots(svg, length_back, 2, along = True, offset_in_from_edge = length - svg.thickness_mm*5)
    set_of_slots(svg, length_back, 2, along = False, offset_in_from_edge = 0, offset_along_from_edge = (length-length_back)/2)

    # outline
    svg.path( [(0,0), (length,0), (length,length), (0,length), (0,0)], direction = direction )


def side(svg, direction = ""):
    length = 150
    length_back = 100
    set_of_tabs(svg, length_back, 2, along = True, offset_in_from_edge = 0)
    set_of_tabs(svg, length_back, 2, along = True, offset_in_from_edge = 0, mirror = (length,0) )

    svg.path( [(svg.thickness_mm,0), (length-svg.thickness_mm,0), (length-svg.thickness_mm,length_back), (svg.thickness_mm,length_back), (svg.thickness_mm,0)], direction = direction )


def main():
    usage = "usage: %prog [options] %prog --help for all options \n"
    parser = OptionParser(usage, version="%prog ")
    parser.add_option("-t", "--thickness_mms", dest="thickness_mm",
                      help="thickness_mm of material")

    (options, args) = parser.parse_args() 
    if not options.thickness_mm:
        thickness_mm = 3.2
    else:
        thickness_mm = float(options.thickness_mm)


    svg = svgClass(thickness_mm=thickness_mm)
    base(svg, "right")
    base(svg, "down_and_zero")
    side(svg, "right_and_a_bit")
    side(svg, "down_and_zero")
    print svg.dump()



if __name__ == "__main__":
    main()
