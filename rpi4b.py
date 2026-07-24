from cadquery import *
from cadquery.func import *
from components import make_ethernet, make_usb_a, make_usb_c, make_sd, make_hdmi_mini, make_jack
from ConnectorItem import ConnectorItem

pcb_w = 56
pcb_l = 85
pcb_h = 1.5
pcb_hole_padding = 3.5

usb_h = 15.6

shell_allowance = 0.4
shell_wall_h_ext = 1
wall_thicknes = 2.8

usb_c_y = pcb_hole_padding+7.7
hdmi_mini_left_y = usb_c_y + 14.8
hdmi_mini_right_y = hdmi_mini_left_y + 13.5
jack_y = hdmi_mini_right_y + 7 + 7.5

pcb_hole_to_hole_y = 58
pcb_holes = [
    (pcb_hole_padding,pcb_hole_padding),
    (pcb_w-pcb_hole_padding,pcb_hole_padding),
    (pcb_hole_padding,pcb_hole_padding+pcb_hole_to_hole_y),
    (pcb_w-pcb_hole_padding,pcb_hole_padding+pcb_hole_to_hole_y)
]
pcb_hole_d = 2.7


def make_pcb():
    pcb_fillet_r = 3
    rv = (
        Workplane("XY")
        .box(pcb_w, pcb_l, pcb_h)
        .edges("|Z").fillet(pcb_fillet_r)
        .faces(">Z").workplane(origin=(-pcb_w/2, -pcb_l/2))
        .pushPoints(pcb_holes)
        .hole(pcb_hole_d)
        .translate((pcb_w/2,pcb_l/2,-pcb_h/2))
    )
    return rv

def make_shell():
    sd_l_margin = 2
    sd_h_margin = 1.5
    inner_w = pcb_w + shell_allowance
    inner_l = pcb_l + sd_l_margin + shell_allowance
    outer_w = inner_w + wall_thicknes*2
    outer_l = inner_l + wall_thicknes*2


    shell_inner_bottom_z =  -pcb_h - sd_h_margin - shell_allowance 
    leg_height = sd_h_margin
    top_inner_z = usb_h + shell_allowance 
    wall_outer_top_z = top_inner_z + wall_thicknes
    wall_outer_bottom_z = -wall_thicknes + shell_inner_bottom_z

    outer_h = wall_outer_top_z - wall_outer_bottom_z
    outer_box = (
        Workplane("XY", origin=(0, 0, 0))
            .box(outer_w, outer_l, outer_h)
            .chamfer(wall_thicknes/2)
            .translate((inner_w/2, inner_l/2-sd_l_margin, outer_h/2 + wall_outer_bottom_z))
            .val()
    )

    inner_h = top_inner_z - shell_inner_bottom_z
    inner_box = (
        Workplane("XY", origin=(0, 0, 0))
            .box(inner_w, inner_l, inner_h)
            #.chamfer(wall_thicknes/2)
            .translate((inner_w/2, inner_l/2-sd_l_margin, top_inner_z - inner_h/2))
            .val()
    )

    shell = outer_box - inner_box

    legs = (
        Workplane("XY", origin=(0, 0, shell_inner_bottom_z))
            .pushPoints(pcb_holes)
            .cylinder(leg_height, pcb_hole_d/2 + 0.5)
            .translate((0, 0, leg_height/2))
            .workplane(offset=leg_height)
            .pushPoints(pcb_holes)
            .cylinder(pcb_h, (pcb_hole_d - shell_allowance)/2)
            .val()
    )

    bar_l = 13
    bar_h = top_inner_z - shell_allowance
    bar = (
        Workplane("XY", origin=(0, 0, 0))
            .box(inner_w, bar_l, bar_h)
            .translate((inner_w/2, inner_l - sd_l_margin - bar_l/2, bar_h/2 + shell_allowance))
            .val()
    )

    rv = shell + bar + legs
    return rv

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
    # return part

    # make splitter
    splitter = (
        make_splitter(3,0.5,110,pcb_w + wall_thicknes, 10, 0.1)
            .translate((pcb_w/2,-10, -0.2))
    )
    #return splitter + part

    # split
    parts = split(part, splitter).Solids()
    top = parts[2]
    bottom = parts[0]

    return (top, bottom)

def cut_shell_openings(shell, cutters):
    result = shell
    for cutter in cutters:
        result = result.cut(cutter[0].moved(Location(cutter[1], cutter[2])))

    return result

connectors = [
    ConnectorItem(
        name="ethernet", 
        make_func=make_ethernet, 
        position=(pcb_w-45.75,pcb_l,0), 
        rotation=(0,0,0)
    ),
    ConnectorItem(
        name="usb-left", 
        make_func=make_usb_a, 
        position=(pcb_w-9,pcb_l,0), 
        rotation=(0,0,0)
    ),
    ConnectorItem(
        name="usb-mid", 
        make_func=make_usb_a, 
        position=(pcb_w-27,pcb_l,0), 
        rotation=(0,0,0)
    ),    
    ConnectorItem(
        name="usb-c", 
        make_func=make_usb_c, 
        position=(pcb_w,usb_c_y, 0), 
        rotation=(0,0,-90)
    ),
    ConnectorItem(
        name="hdmi-mini-left", 
        make_func=make_hdmi_mini, 
        position=(pcb_w, hdmi_mini_left_y, 0), 
        rotation=(0,0,-90)
    ),
    ConnectorItem(
        name="hdmi-mini-right", 
        make_func=make_hdmi_mini, 
        position=(pcb_w, hdmi_mini_right_y, 0), 
        rotation=(0,0,-90)
    ),
    ConnectorItem(
        name="jack", 
        make_func=make_jack,
        position=(pcb_w, jack_y, 0),
        rotation=(0,0,0)
    ),
    ConnectorItem(
        name="sd", 
        make_func=make_sd, 
        position=(pcb_w/2, 0, -pcb_h), 
        rotation=(180,0,0)
    ),
]

rpi = Assembly()

cutters = []

for conn in connectors:
    rpi.add(
        conn.make_func(False),
        name=conn.name,
        color=Color("gray70"),
        loc=Location(conn.position, conn.rotation)
    )

    cutters.append((conn.make_func(True), conn.position, conn.rotation))



show_pcb = False
if(show_pcb):
    rpi.add(
        make_pcb(), 
        name="pcb", 
        color=Color("darkseagreen")
    )

(shell_top, shell_bottom) = split_shell(cut_shell_openings(make_shell(), cutters))

rpi.add(
    shell_top,
    name="shell-top",
    color=Color("lightblue"),
    #loc=Location((pcb_w/2, 0, -pcb_h), (180,0,0))
)

rpi.add(
    shell_bottom,
    name="shell-bottom",
    color=Color("lightblue"),
    #loc=Location((pcb_w/2, 0, -pcb_h), (180,0,0))
)

show_object(rpi)

exporters.export(shell_top, "shell_top.step", exporters.ExportTypes.STEP)
exporters.export(shell_bottom, "shell_bottom.step", exporters.ExportTypes.STEP)