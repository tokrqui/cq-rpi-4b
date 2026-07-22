from cadquery import *
from components import make_ethernet, make_usb_a, make_usb_c, make_sd, make_hdmi_mini

pcb_w = 56
pcb_l = 85
pcb_h = 1.5
pcb_hole_padding = 3.5

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
)

show_object(rpi)