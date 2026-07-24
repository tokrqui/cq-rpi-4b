from cadquery import *

eps = 1e-4

def make_usb_a(is_shell_cutter):
    w = 14.5
    l = 17.7
    h = 15.6
    h_cutter_margin = 0
    l_cutter_margin = 0
    pcb_offset = 3

    if(is_shell_cutter):
        w += 0.4
        h += 0.2
        h_cutter_margin = 0.2
        l_cutter_margin = 3

    pcb_offset += l_cutter_margin
    l += l_cutter_margin

    rv = (
        Workplane("XY")
        .box(w, l, h + h_cutter_margin)
    )

    if(not is_shell_cutter):
        rv = (
            rv
                .faces(">Y")
                .workplane()
                .center(0,4).rect(12, 4.5).extrude(-15, "cut")
                .center(0,-8).rect(12, 4.5).extrude(-15, "cut")
        )

    rv = (
        rv
            .translate((0, pcb_offset-l/2, (h - h_cutter_margin)/2))
            .val()
    )

    return rv

def make_ethernet(is_shell_cutter):
    w = 16.25
    l = 21.25
    h = 13.5
    h_cutter_margin = 0
    l_cutter_margin = 0
    pcb_offset = 3

    if(is_shell_cutter):
        w += 0.4
        h += 0.2
        h_cutter_margin = 0.2
        l_cutter_margin = 3

    pcb_offset += l_cutter_margin
    l += l_cutter_margin

    rv = (
        Workplane("XY")
        .box(w, l, h + h_cutter_margin)
    )

    if(not is_shell_cutter):
        rv = (
            rv
                .faces(">Y")
                .workplane()
                .rect(w-4, h-4)
                .extrude(-15, "cut")
        )

    rv = (
        rv
            .translate((0, pcb_offset-l/2, (h - h_cutter_margin)/2))
            .val()
    )

    return rv

def make_usb_c(is_shell_cutter):
    w = 9
    l = 9
    h = 3.25
    h_cutter_margin = 0
    pcb_offset = 1.2
    plug_shell_distance = 2

    if(is_shell_cutter):
        w += 0.4
        h += 0.2
        h_cutter_margin = 0.2
        pcb_offset += plug_shell_distance
    
    rv = (
        Workplane("XY")
        .box(w, l, h + h_cutter_margin)
        .edges("|Y")
        .fillet((h + h_cutter_margin)/2-eps)
    )

    if(is_shell_cutter):
        cut_box_h = 1.8
        rv = rv + (
            Workplane("XY")
                .box(w, l, cut_box_h)
                .translate((0 ,-1.3, -cut_box_h/2))
        )

    rv = (
        rv
            .translate((0, pcb_offset-l/2, (h - h_cutter_margin)/2))
            .val()
        )

    return rv

def make_hdmi_mini(is_shell_cutter):
    w = 7.2
    l = 7
    h = 4.75
    pcb_offset = 1.5
    h_cutter_margin = 0

    if(is_shell_cutter):
        w += 0.4
        h += 0.2
        h_cutter_margin = 0.2
        pcb_offset += 3

    rv = (
        Workplane("XY")
        .box(w, l, h + h_cutter_margin)
        .translate((0, pcb_offset-l/2, (h - h_cutter_margin)/2))
        .val()
    )
    return rv

def make_sd(is_shell_cutter):
    w = 11
    l = 13
    h = 1.5
    h_cutter_margin = 0
    pcb_offset = 2.5

    if(is_shell_cutter):
        w += 2
        h += 0.4
        h_cutter_margin = 1.3

        l_cutter_margin_front = 1
        l_cutter_margin_back = 1
        pcb_offset += l_cutter_margin_front
        l += (l_cutter_margin_front + l_cutter_margin_back)

    rv = (
        Workplane("XY")
        .box(w, l, h + h_cutter_margin)
        .translate((0, pcb_offset-l/2, (h - h_cutter_margin)/2))
        .val()
    )
    return rv

def make_jack(is_shell_cutter):
    d = 6.05
    d_cutter_margin = 0
    l = 2.6
    l_cutter_margin = 0
    pcb_offset = 2.35

    if(is_shell_cutter):
        d_cutter_margin = 0.5
        l_cutter_margin = 0.2

    l += l_cutter_margin
    pcb_offset += l_cutter_margin
    
    rv = (
        Workplane("YZ")
        .cylinder((d + d_cutter_margin)/2, 2.6)
        .translate((pcb_offset-l/2, 0, (d)/2))
        .val()
    )

    if(not is_shell_cutter):
        rv = (
            Workplane("YZ")
            .cylinder((d + d_cutter_margin)/2, 2.6)
            .translate((pcb_offset-l/2, 0, (d)/2))
            .val()
        )
    else:
        rv = (
            Workplane("XY")
            .box(l + l_cutter_margin, d + d_cutter_margin, d + d_cutter_margin)
            #.box(10,10,10)
            .translate((pcb_offset-l/2, 0, (d)/2))
            .val()
        )
    return rv    