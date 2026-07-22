from cadquery import *

def make_usb_a():
    w = 14.5
    l = 17.7
    h = 15.6
    step = 3
    rv = (
        Workplane("XY")
        .box(w,l,h)
        .faces(">Y")
        .workplane()
        .center(0,4).rect(12, 4.5).extrude(-15, "cut")
        .center(0,-8).rect(12, 4.5).extrude(-15, "cut")
        .translate((0,step-(l/2),(h/2)))
    )
    return rv

def make_ethernet():
    w = 16.25
    l = 21.25
    h = 13.5
    step = 3
    rv = (
        Workplane("XY")
        .box(w,l,h)
        .faces(">Y")
        .workplane()
        .rect(w-4, h-4)
        .extrude(-15, "cut")
        .translate((0,step-(l/2),(h/2)))
    )
    return rv

def make_usb_c():
    eps = 1e-4
    w = 9
    l = 9
    h = 3.25
    step = 1.2
    rv = (
        Workplane("XY")
        .box(w,l,h)
        .edges("|Y").fillet(h/2-eps)
        .translate((0,step-l/2,h/2))
    )
    return rv

def make_hdmi_mini():
    w = 7.2
    l = 7
    h = 4.75
    step = 1.5
    rv = (
        Workplane("XY")
        .box(w,l,h)
        .translate((0,step-l/2,h/2))
    )
    return rv

def make_sd():
    w = 11
    l = 13
    h = 1.5
    step = 2.5
    rv = (
        Workplane("XY")
        .box(w,l,h)
        .translate((0,step-l/2,h/2))
    )
    return rv