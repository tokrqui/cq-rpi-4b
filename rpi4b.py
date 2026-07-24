from cadquery import *
from cadquery.func import *
from components import make_ethernet, make_usb_a, make_usb_c, make_sd, make_hdmi_mini

pcb_w = 56
pcb_l = 85
pcb_h = 1.5
pcb_hole_padding = 3.5

usb_h = 15.6

shell_margin = 0.2
shell_wall_h_ext = 1
wall_thicknes = 3

usb_c_y = pcb_hole_padding+7.7
hdmi_mini_left_y = usb_c_y + 14.8
hdmi_mini_right_y = hdmi_mini_left_y + 13.5

def make_pcb():
    pcb_fillet_r = 3
    pcb_hole_d = 2.7
    pcb_hole_to_hole_y = 58
    rv = (
        Workplane("XY")
        .box(pcb_w, pcb_l, pcb_h)
        .edges("|Z").fillet(pcb_fillet_r)
        .faces(">Z").workplane(origin=(-pcb_w/2, -pcb_l/2))
        .pushPoints([
            (pcb_hole_padding,pcb_hole_padding),
            (pcb_w-pcb_hole_padding,pcb_hole_padding),
            (pcb_hole_padding,pcb_hole_padding+pcb_hole_to_hole_y),
            (pcb_w-pcb_hole_padding,pcb_hole_padding+pcb_hole_to_hole_y)
        ])
        .hole(pcb_hole_d)
        .translate((pcb_w/2,pcb_l/2,-pcb_h/2))
    )
    return rv

def make_shell():
    wall_height = usb_h + wall_thicknes + shell_margin
    inner_w = pcb_w + shell_margin
    inner_l = pcb_l + shell_margin
    outer_w = inner_w + wall_thicknes*2
    outer_l = inner_l + wall_thicknes*2

    bottom_walls_part_h = wall_thicknes+pcb_h+1.5+shell_margin


    walls_face = face(
        rect(outer_w, outer_l),
        rect(inner_w, inner_l),
    )

    walls = extrude(walls_face, (0,0,wall_height + bottom_walls_part_h)).translate((0,0,-bottom_walls_part_h))

    top = extrude(plane(inner_w, inner_l), (0,0,wall_thicknes)).translate((0,0,wall_height-wall_thicknes))
    bottom = extrude(plane(inner_w, inner_l), (0,0,wall_thicknes)).translate((0,0,-bottom_walls_part_h))

    rv = walls + top + bottom
    #rv = base_inner_face

    return rv.rotate((0, 0, 0), (0, 1, 0), 0).translate((pcb_w/2, pcb_l/2, 0))

def make_splitter(h, w, l, distance, leap_w, thickness):
    z_step = h / 5
    y_step = w / 3

    edge = (
        Workplane("ZX")
        .moveTo(0, 0)
        .lineTo(0*z_step, distance/2 + 0*y_step)
        .spline([
            (1*z_step, distance/2 + 1*y_step),
            (2*z_step, distance/2 + 0*y_step),
            (3*z_step, distance/2 + -1*y_step),
            (4*z_step, distance/2 + 0*y_step),
        ], includeCurrent=True) # fix tangents
        .lineTo(4*z_step, distance/2 + leap_w)
        .wire().val()
    )

    edge2 = edge.translate((0, l, 0))
    shell = Face.makeRuledSurface(edge, edge2)
    thick = offset(shell, thickness/2, both=True)
    thick2 = thick.mirror("YZ")
    return thick + thick2

def split_shell(part):
    # make splitter
    splitter = make_splitter(3,0.5,110,pcb_w + wall_thicknes, 10, 0.1).translate((pcb_w/2,-10,0))
    #return splitter + part

    # split
    parts = split(part, splitter).Solids()
    top = parts[2]
    bottom = parts[0]

    return top

rpi = (
    Assembly()
    .add(
        make_pcb(), 
        name="pcb", 
        color=Color("darkseagreen")
    )
    .add(
        make_ethernet(), 
        name="ethernet", 
        color=Color("gray70"),
        loc=Location(Vector(pcb_w-45.75,pcb_l,0))
    )
    .add(
        make_usb_a(), 
        name="usb-mid", 
        color=Color("gray70"),
        loc=Location(Vector(pcb_w-27,pcb_l,0))
    )
    .add(
        make_usb_a(), 
        name="usb-left", 
        color=Color("gray70"),
        loc=Location(Vector(pcb_w-9,pcb_l,0))
    )    
    .add(
        make_usb_c(), 
        name="usb-c", 
        color=Color("gray70"),
        loc=Location((pcb_w,usb_c_y, 0), (0,0,-90))
    )    
    .add(
        make_hdmi_mini(), 
        name="hdmi-mini-left", 
        color=Color("gray70"),
        loc=Location((pcb_w, hdmi_mini_left_y, 0), (0,0,-90))
    )       
    .add(
        make_hdmi_mini(), 
        name="hdmi-mini-right", 
        color=Color("gray70"),
        loc=Location((pcb_w, hdmi_mini_right_y, 0), (0,0,-90))
    )
    .add(
        make_sd(), 
        name="sd", 
        color=Color("gray70"),
        loc=Location((pcb_w/2, 0, -pcb_h), (180,0,0))
    )
    .add(
        split_shell(make_shell()),
        name="shell",
        color=Color("blue"),
        #loc=Location((pcb_w/2, 0, -pcb_h), (180,0,0))
    )
)

show_object(rpi)