
from optparse import OptionParser


class svgClass:
    def __init__(self, thickness=32, material_width_mm = 320, material_height_mm = 600, pixel_ratio = 10, spacer_p = 150):
        self.thickness = thickness
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

    def append(self, svgtxt):
        self.svg += svgtxt
    def dump(self):
        return self.svg + "\n</svg>"

    def path(self, points, direction = "stet"):
        line_start = '<path stroke="blue" stroke-width="1mm" fill="none" id="h" d="'
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
            self.current_offset_width += max_x + self.spacer_p
        if direction == "down":
            self.current_offset_height += max_y + self.spacer_p

def flip_points(points):
    flip = []
    for point in points:
        (x,y) = point
        flip.append((y,x))
    return flip


def slot(svg, offset_in_from_edge = 0, offset_along_from_edge = 0, length = 100, along = False):
    t = svg.thickness
    length = length + t # fudge!
    # top corner
    path = []
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+t*1))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+t*1))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+t*2))
    path.append((offset_in_from_edge+t*3,offset_along_from_edge+t*2))
    path.append((offset_in_from_edge+t*3,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*4,offset_along_from_edge+length))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+length))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*2,offset_along_from_edge+length-t*1))
    path.append((offset_in_from_edge+t*2,offset_along_from_edge+t*2))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+t*2))
    path.append((offset_in_from_edge+t*1,offset_along_from_edge+t*1))
    if along:
        path = flip_points(path)
    svg.path(path)


def base(svg):
    slot(svg, offset_along_from_edge=100, length = 15)
    slot(svg, offset_along_from_edge=50, length = 50, along = True)

    # outline
    svg.path( [(0,0), (300,0), (300,300), (0,300), (0,0)] )




def main():
    usage = "usage: %prog [options] %prog --help for all options \n"
    parser = OptionParser(usage, version="%prog ")
    parser.add_option("-t", "--thicknesss", dest="thickness",
                      help="Thickness of material")

    (options, args) = parser.parse_args() 
    if not options.thickness:
        thickness = 5
    else:
        thickness = float(options.thickness)


    svg = svgClass(thickness=thickness)
    base(svg)
    print svg.dump()



if __name__ == "__main__":
    main()
