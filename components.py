from cadquery import *

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
    #is_shell_cutter = True

    eps = 1e-4
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
        .edges("|Y").fillet((h + h_cutter_margin)/2-eps)
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
        pcb_offset += 1
        h += 0.4
        h_cutter_margin = 1.3

    rv = (
        Workplane("XY")
        .box(w, l, h + h_cutter_margin)
        .translate((0, pcb_offset-l/2, (h - h_cutter_margin)/2))
        .val()
    )
    return rv