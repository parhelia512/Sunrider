label initStore:  
    python:
        store_items = []

        store_items.append(NewWarhead())
        store_items.append(RocketUpgrade())
        store_items.append(NewRepairDrone())
        store_items.append(ContractAllianceCruiser())
        store_items.append(ContractUnionFrigate())
        
    return

screen store_union:
    modal True
    tag storyscreen

    use store_info

    imagebutton: #return button
        xpos 0.05 ypos 0.8
        action [ Hide('store_union') , SetField(BM,'hovered',None) , Jump("dispatch") ]
        idle "Menu/return.jpg"
        hover "Menu/return_hover.jpg"

    frame:
        xmaximum 800
        xpos 10
        ypos 270
        background None
        vbox:
            spacing 20
            for item in store_items:
                if item.isVisible():
                    imagebutton:
                        action If(BM.money >= item.cost and (eval(item.variable_name) is None or eval(item.variable_name) < item.max_amt),item,NullAction())
                        idle "Menu/store_item.png"
                        hover "Menu/store_item_hover.png"
                        hovered SetField(BM,'hovered',item.id)
                        unhovered SetField(BM,'hovered',None)
        vbox:
            for item in store_items:
                if item.isVisible():
                    text item.display_name + ("    [[owned:{!s}]".format(eval(item.variable_name)) if item.variable_name != None else "") font "Font/sui generis rg.ttf" size 30 first_indent 50 line_spacing 38 color "#0a0a0a"
        vbox:
            for item in store_items:
                if item.isVisible():
                    text str(item.cost) font "Font/sui generis rg.ttf" size 30 first_indent 710 line_spacing 38 color "#0a0a0a"

    text '{!s}$'.format(BM.money):
        size 50
        xpos 0.15
        ypos 0.7
        color '090'
        outlines [(1,'000',0,0)]

screen store_info:
    zorder 10

    frame:
        xmaximum 600
        background None
        xpos 0.5
        ypos 0.2
        
        for item in store_items:
            if BM.hovered == item.id:
                text item.display_name xpos 50 ypos 50 size 35 font "Font/sui generis rg.ttf" color '000'
                text item.tooltip xpos 50 ypos 150 size 20 font "Font/GOTHIC.TTF" color '000'



# screen store_missile:
    # add "Menu/unionstore_missiles.png" xpos 1170 ypos 200

# screen store_rocket:
    # add "Menu/unionstore_rocket.png" xpos 1170 ypos 200