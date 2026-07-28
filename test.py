from cadquery import cq, Assembly, Color, Location, exporters
from cadquery.func import Face, offset, split

test = (
        cq.Workplane("XY")
            .box(10, 20, 30)
            .faces("+Z or |Y")
        )

show_object(test)