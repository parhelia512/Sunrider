## this file is a horrible mishmash of experimental code that often end up used in the game
## many of this stuff should be organized in other files...

#init:
#    image movie = Movie(size=(400, 300), xalign=0.5, yalign=0.5)

image black = Solid((0, 0, 0, 255))

#label no_animation: #defunct
#    scene black with dissolve
#    show work_in_progress
#    pause 0.5
#    return
label testpause:
    python:
        renpy.pause(1)
        
    return

transform shake(time=0.5,repeats=20): #defunct?
    xalign 0.5 yalign 0.5
    pause time
    block:
        ease 0.01 xpos 0.51
        ease 0.02 xpos 0.49
        ease 0.01 xpos 0.5
        repeat repeats

label test_battle:
    python:
        zoomlevel = 1
        enemy_ships = []
        destroyed_ships = []
        BM.mission = 'test'
        
        BM.orders['SHORT RANGE WARP'] = [750,'short_range_warp']

        #create the sunrider. you only have to create a player ship once:
        sunrider_weapons = [SunriderLaser(),SunriderKinetic(),SunriderMissile(),SunriderRocket(),SunriderAssault()]
        sunrider = create_ship(Sunrider(),(8,6),sunrider_weapons)

        blackjack_weapons = [BlackjackMelee(),BlackjackLaser(),BlackjackAssault(),BlackjackMissile(),BlackjackPulse()]
        blackjack = create_ship(BlackJack(),(10,5),blackjack_weapons)

        liberty_weapons = [LibertyLaser(),Repair(),AccUp(),DamageUp(),AccDown()]
        liberty = create_ship(Liberty(),(8,7),liberty_weapons)

        phoenix_weapons = [PhoenixMelee(),Stealth(),GravityGun()]
        phoenix = create_ship(Phoenix(),(10,7),phoenix_weapons)

        create_ship(Havoc(),(13,5),[Melee(),HavocAssault(),HavocMissile(),HavocRocket()])
        enemy_ships[-1].hp = 1
        create_ship(PirateGrunt(),(13,7),[PirateGruntLaser(),PirateGruntMissile(),PirateGruntAssault()])
        create_ship(PirateGrunt(),(13,6),[PirateGruntLaser(),PirateGruntMissile(),PirateGruntAssault()])
        create_ship(PirateGrunt(),(13,8),[PirateGruntLaser(),PirateGruntMissile(),PirateGruntAssault()])
        create_ship(PactCruiser(),(14,8),[])

        create_ship(PirateDestroyer(),(16,5),[PirateDestroyerLaser(),PirateDestroyerKinetic()])
        create_ship(PirateDestroyer(),(16,7),[PirateDestroyerLaser(),PirateDestroyerKinetic()])

        #center the viewport on the sunrider
        BM.xadj.value = 872
        BM.yadj.value = 370

    $ PlayerTurnMusic = "music/Titan.ogg"
    $ EnemyTurnMusic = "music/Dusty_Universe.ogg"

#    $ buy_upgrades() ##testing

    jump battle_start
    return

label missiontest:

    $BM.battle()  #continue the battle

    if BM.battlemode == True:   #whenever this is set to False battle ends.
        jump missiontest #loop back
    else:
        pass #continue down

    # jump dispatch
    return
    
    
label skirmish_battle:
    python:
        store.tempmoney = BM.money
        store.tempcmd = BM.cmd
        enemy_ships = []
        destroyed_ships = []
        BM.mission = 'skirmish'
        BM.xadj.value = 872
        BM.yadj.value = 370 
        store.zoomlevel = 0.65
        BM.phase = 'formation'
        BM.show_grid = False
        battlemode()
        for ship in player_ships:
            ship.location = None

    $ PlayerTurnMusic = "music/Titan.ogg"
    $ EnemyTurnMusic = "music/Dusty_Universe.ogg"
    
    hide screen deck0
    show screen battle_screen
    show screen player_unit_pool_collapsed
    show screen enemy_unit_pool_collapsed
    
    call missionskirmish       
    
    python:
        BM.phase = 'Player'
        BM.mission = 'skirmishbattle'
    
    call battle_start
    
    python:
        BM.cmd = store.tempcmd
        BM.money = store.tempmoney
    jump dispatch
    return
    
label missionskirmishbattle:

    $BM.battle()  #continue the battle

    if BM.battlemode == True:   #whenever this is set to False battle ends.
        jump missionskirmishbattle #loop back
    else:
        pass #continue down

    # jump dispatch
    return    
    
label missionskirmish:
    python:
        result = ui.interact()
        
        if result == True or result == False:
            show_message('wtf is a bool returned?') #had some trouble with this at some point. still not sure what caused it.
            renpy.jump('missionskirmish')
        
        elif result == 'start':
            renpy.hide_screen('player_unit_pool_collapsed')
            renpy.hide_screen('enemy_unit_pool_collapsed')
            renpy.hide_screen('player_unit_pool')
            renpy.hide_screen('enemy_unit_pool')
            renpy.hide_screen('mousefollow')            
            BM.battlemode = False
            
        elif result[0] == "zoom":
            zoom_handling(result,BM)
            
        elif result == "next ship":
            templist = []
            for ship in player_ships:
                if ship.location == None:
                    templist.append(ship)
                    
            if BM.selected == None:
                if len(templist) > 0:
                    BM.select_ship(templist[0])                
            else:
                if BM.selected.location != None:
                    set_cell_available(BM.selected.location) 
                index = templist.index(BM.selected)
                if index == (len(templist)-1):
                    index = 0
                else:
                    index += 1
                BM.select_ship(templist[index])
                    
            if BM.selected != None:
                BM.targetwarp = True
                renpy.show_screen('mousefollow')
                BM.selected.location = None
            
        elif result == 'deselect':
            #if you picked up an enemy unit that was already put down right clicking should delete it entirely
            #player ships automatically return to the blue pool to be placed again later.
            if BM.selected != None:
                if BM.selected in enemy_ships:
                    BM.ships.remove(BM.selected)
                    enemy_ships.remove(BM.selected)
            BM.targetwarp = False
            renpy.hide_screen('mousefollow')                
            BM.unselect_ship(BM.selected)
            
        elif result[0] == 'selection':
            # this result can be from one of the imagebuttons in the pool screens or returned from
            # MouseTracker because a hex with a unit in it was clicked.
            selected_ship = result[1]
            BM.targetwarp = True
            renpy.show_screen('mousefollow')
            
            if selected_ship.faction == 'Player':
                BM.select_ship(selected_ship)
            else:
                if selected_ship.location != None:
                    BM.selected = selected_ship
                    if selected_ship in enemy_ships:
                        BM.ships.remove(BM.selected)
                        enemy_ships.remove(BM.selected)
                else:
                    BM.selected = deepcopy(selected_ship) #breaks alias
                    BM.selected.weapons = BM.selected.default_weapon_list
                    
            if BM.selected.location != None:
                set_cell_available(BM.selected.location)           
            BM.selected.location = None
                
            
        elif result[0] == 'warptarget':
            # returned from MouseTracker if you click on an empty hex when BM.warptarget == True.
            if BM.selected != None:
                new_location = result[1]
                set_cell_available(new_location,True)
                
                if BM.selected.faction != 'Player':
                    enemy_ships.append(BM.selected)
                    BM.ships.append(BM.selected)               
                
                BM.selected.location = new_location
                
                if BM.selected.faction != 'Player' and pygame.key.get_mods() != 0:
                    BM.selected = deepcopy(BM.selected) #breaks alias                    
                else:
                    BM.targetwarp = False
                    renpy.hide_screen('mousefollow')                
                    BM.unselect_ship(BM.selected)

    if BM.battlemode:   #whenever this is set to False battle ends.
        jump missionskirmish #loop back
    else:
        pass #continue down

    return
    
    
label formationphase:  #pretty much a copy of missionskirmish but I can't be bothered merging these 2 right now
    python:
        result = ui.interact()
        
        if result == 'start':
        
            #check if there are still player units that are not placed
            unplaced_units = False
            for ship in player_ships:
                if ship.location == None:
                    unplaced_units = True
            if unplaced_units:
                show_message('there are still ships you have not placed!')
            else:
                renpy.hide_screen('player_unit_pool_collapsed')
                renpy.hide_screen('enemy_unit_pool_collapsed')
                renpy.hide_screen('player_unit_pool')
                renpy.hide_screen('enemy_unit_pool')
                renpy.hide_screen('mousefollow')
                BM.phase = 'Player'
                renpy.jump('mission{}'.format(BM.mission))
            
        elif result[0] == "zoom":
            zoom_handling(result,BM)
            
        elif result == "next ship":
            templist = []
            for ship in player_ships:
                if ship.location == None:
                    templist.append(ship)
                    
            if BM.selected == None:
                if len(templist) > 0:
                    BM.select_ship(templist[0])                
            else:
                if BM.selected.location != None:
                    set_cell_available(BM.selected.location) 
                index = templist.index(BM.selected)
                if index == (len(templist)-1):
                    index = 0
                else:
                    index += 1
                BM.select_ship(templist[index])
                    
            if BM.selected != None:
                BM.targetwarp = True
                renpy.show_screen('mousefollow')
                BM.selected.location = None
                   
        
        elif result == 'deselect':
            #if you picked up an enemy unit that was already put down right clicking should delete it entirely
            #player ships automatically return to the blue pool to be placed again later.
            if BM.selected != None:
                if BM.selected in enemy_ships:
                    BM.ships.remove(BM.selected)
                    enemy_ships.remove(BM.selected)
            BM.targetwarp = False
            renpy.hide_screen('mousefollow')                
            BM.unselect_ship(BM.selected)
            
        elif result[0] == 'selection':
            # this result can be from one of the imagebuttons in the pool screens or returned from
            # MouseTracker because a hex with a unit in it was clicked.
            selected_ship = result[1]
            BM.targetwarp = True
            renpy.show_screen('mousefollow')
            
            if selected_ship.faction == 'Player':
                BM.select_ship(selected_ship)
            else:
                if selected_ship.location != None:
                    BM.selected = selected_ship
                    if selected_ship in enemy_ships:
                        BM.ships.remove(BM.selected)
                        enemy_ships.remove(BM.selected)
                else:
                    BM.selected = deepcopy(selected_ship) #breaks alias
                    BM.selected.weapons = BM.selected.default_weapon_list
                    
            if BM.selected.location != None:
                set_cell_available(BM.selected.location)           
            BM.selected.location = None
                
            
        elif result[0] == 'warptarget':
            # returned from MouseTracker if you click on an empty hex when BM.warptarget == True.
            if BM.selected != None:
                new_location = result[1]
                
                #when setting up before a mission you can't put your ships farther to the right than column 7
                if new_location[0] > 7:
                    show_message('too far infield')
                else:               
                    set_cell_available(new_location,True)
                    
                    if BM.selected.faction != 'Player':
                        enemy_ships.append(BM.selected)
                        BM.ships.append(BM.selected)               
                    
                    BM.selected.location = new_location
                    
                    if BM.selected.faction != 'Player' and pygame.key.get_mods() != 0:
                        BM.selected = deepcopy(BM.selected) #breaks alias                    
                    else:
                        BM.targetwarp = False
                        renpy.hide_screen('mousefollow')                
                        BM.unselect_ship(BM.selected)                        

    if BM.battlemode:   #whenever this is set to False battle ends.
        jump formationphase #loop back
    else:
        pass #continue down

    return    
    

transform melee_atkanim(img1,img2):
    img1
    xalign 0.5 yalign 0.5
    zoom 2 xpos 0.2
    ease 0.5 zoom 1 xpos 0.5
    pause 1.3
    img2 with Dissolve(.5, alpha=True)
    pause 1.0
    xpos 0.5 ypos 0.5
    ease 1.0 xpos 2.0 ypos -1.0
    xpos -2.0 ypos 1.0
    ease 1.5 xpos 0.9 ypos 0.5
    pause 0.5
    xpos 0.9 ypos 0.5
    ease 1.0 xpos 2.0 ypos -1.0

transform melee_atkanim_enemy(img1,img2):
    img1
    xalign 0.5 yalign 0.5
    zoom 2 xpos 0.8
    ease 0.5 zoom 1 xpos 0.5
    pause 1.3
    img2 with Dissolve(.5, alpha=True)
    pause 1.0
    xpos 0.5 ypos 0.5
    ease 1.0 xpos -2.0 ypos -1.0
    xpos 2.0 ypos 1.0
    ease 1.5 xpos 0.1 ypos 0.5
    pause 0.5
    xpos 0.1 ypos 0.5
    ease 1.0 xpos -1.0 ypos -1.0


transform melee_atkanim_sprite(img1):
    img1
    yanchor 0.51 ypos 1.0
    xanchor 0.5
    zoom 0.6255
    subpixel True
    xzoom -1 xpos -0.2
    ease 0.3 xpos 0.15
    pause 0.5
    ease 1.5 alpha 0

transform melee_hitanim(img1,yy):
    pause 3.5
    img1
    yanchor 0.5 xanchor 0.5
    xpos 0.5 ypos 0.5
    linear 1.0 ypos yy

screen melee_player:
    zorder 2

    if store.damage == 'miss':
        add melee_hitanim(BM.target.sprites['standard'],-1.5)
    else:
        add melee_hitanim(BM.target.sprites['standard'],0.5)

    if BM.attacker.faction == 'Player':
        add melee_atkanim(BM.attacker.sprites['standard'],BM.attacker.sprites['melee'])
    else:
        add melee_atkanim_enemy(BM.attacker.sprites['standard'],BM.attacker.sprites['melee'])

    add melee_atkanim_sprite(BM.attacker.sprites['character'])

label melee_attack_player:
    python:
        renpy.show_screen('show_background',_layer='master')
        renpy.show_screen('melee_player',_layer='master')

        try:
            random = renpy.random.randint(0,len(BM.attacker.attack_voice)-1)
            renpy.music.play(BM.attacker.attack_voice[random],channel=BM.attacker.voice_channel)
        except:
            pass

    pause 1.3
    if BM.attacker.name == 'Havoc':
        play sound "sound/chainsaw.ogg"
    else:
        play sound "sound/mech1.ogg"
    pause 1.0 #I think dissolve effect also pauses for a little while
    play sound "sound/boasters.ogg"
    pause 1.4


    ## hitanim ##   little reason not to combine them if it's all dynamically generated anyway.

    show screen animation_hp
    pause 1.0
    play sound "sound/Sword Shing 2.ogg"


    if store.damage != 'miss':

        if BM.attacker.faction == 'Player':
            show melee_overlay onlayer screens:
                xzoom -1
            with meleehitreverse
        else:
            show melee_overlay onlayer screens:
                xzoom -1
            with meleehit

        pause 0.1
        hide melee_overlay onlayer screens with dissolvequick
        pause 0.5
        play sound1 "sound/explosion1.ogg"
        show layer master at shake2(repeats=6)

        if BM.attacker.faction == 'Player':
            show piratebomber_kinetichit2 onlayer screens:
                xpos 0.55 ypos 0.5 zoom 1.2
                ease 1.2 alpha 0
            pause 0.1
            play sound2 "sound/explosion1.ogg"
            show layer master at shake2(repeats=6)
            show piratebomber_kinetichit1 onlayer screens:
                xpos 0.55 ypos 0.5 zoom 1.2
                ease 1.2 alpha 0
        else:
            show piratebomber_kinetichit2 onlayer screens:
                xpos 0.4 ypos 0.5 xzoom -1 zoom 1.2
                ease 1.2 alpha 0
            pause 0.1
            play sound2 "sound/explosion1.ogg"
            show layer master at shake2(repeats=6)
            show piratebomber_kinetichit1 onlayer screens:
                xpos 0.4 ypos 0.5 xzoom -1 zoom 1.2
                ease 1.2 alpha 0

        pause 0.5

        if BM.attacker.faction == 'Player':
            $renpy.call('attacksuccess_{}'.format(BM.attacker.animation_name))
        else:
            $renpy.call('hit_{}'.format(BM.target.animation_name))
    else:
        pause 0.5
        if BM.attacker.faction == 'Player':
            $renpy.call('attackfail_{}'.format(BM.attacker.animation_name))
        else:
            python:
                try:
                    random = renpy.random.randint(0,len(BM.attacker.no_damage_voice)-1)
                    renpy.music.play(BM.attacker.no_damage_voice[random],channel=BM.attacker.voice_channel)
                except:
                    pass

    return

label endofturn:
    show screen battle_screen
    $update_stats()

    if not BM.phase == 'Player':
        play sound 'sound/battle.wav'
        show sunrider_phase onlayer screens zorder 50
        pause TURN_SPEED
        play sound 'sound/drum.ogg'
        hide sunrider_phase onlayer screens zorder 50 with dissolve
        $ BM.phase = 'Player'
    elif BM.phase == 'Player' and enemy_ships[0].faction == 'PACT':
        play sound 'sound/battle.wav'
        show PACT_phase onlayer screens zorder 50
        pause TURN_SPEED
        play sound 'sound/drum.ogg'
        hide PACT_phase onlayer screens zorder 50 with dissolve
        $ BM.phase = 'PACT'
    elif BM.phase == 'Player' and enemy_ships[0].faction == 'Pirate':
        play sound 'sound/battle.wav'
        show Pirate_phase onlayer screens zorder 50
        pause TURN_SPEED
        play sound 'sound/drum.ogg'
        hide Pirate_phase onlayer screens zorder 50 with dissolve
        $ BM.phase = 'Pirate'

    $update_modifiers() #update buffs and curses

    if BM.phase == 'Player':
        $ renpy.take_screenshot()
        $ renpy.save('beginturn')

    return

label battle_start:
    play music PlayerTurnMusic
    python:
        BM.stopAI = False
        BM.order_used = False
        renpy.take_screenshot()
        renpy.save('battlestart')
        renpy.take_screenshot()
        renpy.save('beginturn')
        if BM.show_tooltips:
            renpy.show_screen('tooltips')
        # BM.xadj.value = 872
        # BM.yadj.value = 370
        for ship in player_ships:
            ship.hp = ship.max_hp
            ship.en = ship.max_en
        # renpy.show_screen('mousefollow')
        store.zoomlevel = 0.65
        BM.show_grid = False
        sort_ship_list()
        BM.start()


    return

label sunrider_destroyed:
    hide screen commands
    hide screen battle_screen
    scene badend

    $ BM.phase = 'Player' #this makes it so you can save and load again, as it's normally blocked during the enemy's turn

    menu:
        "Try Again":
            jump tryagain

        "Load Saved Game":
            jump loadsavedgame

    return

label loadsavedgame:   #used when the player chooses to load a saved game after game over
    show screen load
    pause
    jump sunrider_destroyed
    return

#label battle:
#    $BM.battle()
#    if BM.battlemode == True:
#        jump battle
#    else:
#        return

label tryagain:
    $renpy.load('battlestart')
    pause
    $show_message('this should never show up')
    pause
    return

label restartturn:
    $renpy.load('beginturn')
    pause
    $show_message('this should never show up')
    pause
    return

label after_load:

    python:
        reset = False
        if not hasattr(store,'BM'):
            BM = Battle()
        if hasattr(BM,'save_version'):
            if BM.save_version != config.version:
                reset = True
            else:
                pass #everything is fine, do not reset
        else:
            reset = True

        if reset:
            rocketdamage = 800
            if hasattr(store,'sunrider_rocket'):
                rocketdamage = store.sunrider_rocket.damage
            reset_classes()
            if sunrider != None:
                store.sunrider.weapons[3].damage = rocketdamage
            BM.save_version = config.version
            res_location = "lab"
            res_event = "allocatefunds"

             #check if the ship variable is defined or not. if not, define it
            if not hasattr(store,'bianca'):
                bianca = None
             #it should now be defined. if it's None create the ship at location None
            if bianca == None:
                pass
            else:
                bianca.weapons = [BiancaAssault(),GravityGun(),AccDown(),DamageUp()]

            if not hasattr(store,'liberty'):
                liberty = None
            if liberty == None:
                pass
            else:
                liberty.weapons = [LibertyLaser(),Repair(),AccUp(),Disable(),FlakOff(),ShutOff()]

            if not hasattr(store,'phoenix'):
                phoenix = None
            if phoenix == None:
                pass
            else:
                phoenix.weapons = [PhoenixAssault(),PhoenixMelee(),Stealth()]

        #cleanup
        if hasattr(BM,'ships') and hasattr(store,'player_ships') and hasattr(store,'enemy_ships'):
            if BM.ships != []:
                BM.ships = []
                for ship in player_ships:
                    BM.ships.append(ship)
                for ship in enemy_ships:
                    BM.ships.append(ship)
    return




