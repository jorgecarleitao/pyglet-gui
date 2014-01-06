
VALIGN_TOP = 1
VALIGN_CENTER = 0
VALIGN_BOTTOM = -1

HALIGN_LEFT = -1
HALIGN_CENTER = 0
HALIGN_RIGHT = 1

ANCHOR_TOP_LEFT = (VALIGN_TOP, HALIGN_LEFT)
ANCHOR_TOP = (VALIGN_TOP, HALIGN_CENTER)
ANCHOR_TOP_RIGHT = (VALIGN_TOP, HALIGN_RIGHT)
ANCHOR_LEFT = (VALIGN_CENTER, HALIGN_LEFT)
ANCHOR_CENTER = (VALIGN_CENTER, HALIGN_CENTER)
ANCHOR_RIGHT = (VALIGN_CENTER, HALIGN_RIGHT)
ANCHOR_BOTTOM_LEFT = (VALIGN_BOTTOM, HALIGN_LEFT)
ANCHOR_BOTTOM = (VALIGN_BOTTOM, HALIGN_CENTER)
ANCHOR_BOTTOM_RIGHT = (VALIGN_BOTTOM, HALIGN_RIGHT)


def GetRelativePoint(parent, parent_anchor, child, child_anchor, offset):
    valign, halign = parent_anchor or ANCHOR_CENTER

    if valign == VALIGN_TOP:
        y = parent.y + parent.height
    elif valign == VALIGN_CENTER:
        y = parent.y + parent.height // 2
    else:  # VALIGN_BOTTOM
        y = parent.y

    if halign == HALIGN_LEFT:
        x = parent.x
    elif halign == HALIGN_CENTER:
        x = parent.x + parent.width // 2
    else:  # HALIGN_RIGHT
        x = parent.x + parent.width

    valign, halign = child_anchor or (valign, halign)
    offset_x, offset_y = offset

    if valign == VALIGN_TOP:
        y += offset_y - child.height
    elif valign == VALIGN_CENTER:
        y += offset_y - child.height // 2
    else:  # VALIGN_BOTTOM
        y += offset_y

    if halign == HALIGN_LEFT:
        x += offset_x
    elif halign == HALIGN_CENTER:
        x += offset_x - child.width // 2
    else:  # HALIGN_RIGHT
        x += offset_x - child.width

    return x, y
