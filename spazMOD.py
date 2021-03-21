"""Define a simple example plugin."""

# ba_meta require api 6

from __future__ import annotations

from typing import TYPE_CHECKING

import random
from don import tintColor
import don

import ba
ba.screenmessage('Spaz Mods is created by PCModder for FRIENDS to use',color=(3,-4,8))#created by PCModder full rights to me. :)
ba.screenmessage('Use don.py to use specific settings',color=(3,-4,8))#I believe now i am gone with the wind
from _ba import chatmessage as cmsg, get_foreground_host_activity
import _ba
from bastd.actor.spaz import Spaz, SpazFactory, BombDiedMessage, CurseExplodeMessage, PunchHitMessage, PickupMessage
import bastd.actor.spaz
from bastd.actor.popuptext import PopupText
from bastd.gameutils import SharedObjects
from bastd.actor import bomb as stdbomb

if TYPE_CHECKING:
    from typing import Any, Type, Optional, Tuple, List, Dict


# ba_meta export plugin
class spazMOD(ba.Plugin):
    """My first ballistica plugin!"""

    Spaz._old_init = Spaz.__init__
    def _new_init(self,
                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 highlight: Sequence[float] = (0.5, 0.5, 0.5),
                 character: str = 'Spaz',
                 source_player: ba.Player = None,
                 start_invincible: bool = True,
                 can_accept_powerups: bool = True,
                 powerups_expire: bool = False,
                 demo_mode: bool = False):
        self._old_init(color,highlight,character,source_player,
                       start_invincible,can_accept_powerups,
                       powerups_expire,demo_mode)
                       
        if don.light:        
            self.light = ba.newnode('light',
                           owner=self.node,
                           attrs={
                               'position': self.node.position,
                               'radius': 0.1,#ahem pc was here
                               'volume_intensity_scale':0.1,
                               'height_attenuated': False,
                               'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0))})
            self.node.connectattr('position', self.light, 'position')
            ba.animate_array(self.light, 'color', 3,{0:(1,0,0),0.2:(1,0.5,0),0.4:(1,1,0),0.6:(0,1,0),0.8:(0,1,1),1.0:(0,0,1),1.2:(1,0,0)},True)
                       
        def _new_hp():
            if not self.node:
                return
            hp = ba.newnode('math',
                            owner=self.node,
                            attrs={'input1': (0, 0.65, 0),'operation': 'add'})
            self.node.connectattr('torso_position', hp, 'input2')
            self.hp = ba.newnode('text',
                                 owner=self.node,
                                 attrs={
                                    'text': '',
                                    'in_world': True,
                                    'shadow': 1.0,
                                    'flatness': 1.0,
                                    'scale': 0.008,
                                    'h_align': 'center',
                                 })
            hp.connectattr('output', self.hp, 'position')
            #ba.animate(self.hp, 'scale', {0:0, 0.2:0, 0.6:0.018, 0.8:0.012})
            activity = get_foreground_host_activity()
            if don.tint:
                activity.globalsnode.tint=(tintColor)

            def _update():
                if not self.hp:
                    return
                if self.shield:
                    hptext = int(
                        (self.shield_hitpoints/self.shield_hitpoints_max)*100)
                else:
                    hptext = int(self.hitpoints*0.1)
                if hptext >= 75:
                    color = (1, 1, 1)
                elif hptext >= 50:
                    color = (1, 1, 1)
                elif hptext >= 25:
                    color = (1, 1, 1)
                else:
                    color = (1, 1, 1)
                self.hp.text = 'HP:' + str(hptext)
                self.hp.color = (0.2, 1.0, 0.8) if self.shield else color
            ba.timer(0.05, _update, repeat=True)
        _new_hp()
        app = _ba.app
        cfg = app.config
        new_hp = cfg.get('New HP', True)
        if new_hp:
            _new_hp()
                       
    def on_punch_press(self) -> None:
        """
        Called to 'press punch' on this spaz;
        used for player or AI connections.
        """
        if not self.node or self.frozen or self.node.knockout > 0.0:
            return
        t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(t_ms, int)
        if t_ms - self.last_punch_time_ms >= self._punch_cooldown:
            if self.punch_callback is not None:
                self.punch_callback(self)
            self._punched_nodes = set()  # Reset this.
            self.last_punch_time_ms = t_ms
            self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
            self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))          
            ba.emitfx(position=self.node.position,velocity=self.node.velocity,count=35,scale=0.5,spread=2,chunk_type='spark')
            self.node.punch_pressed = True
            if not self.node.hold_node:
                ba.timer(
                    0.1,
                    ba.WeakCall(self._safe_play_sound,
                                SpazFactory.get().swish_sound, 0.8))
        self._turbo_filter_add_press('punch')
        
    def on_jump_press(self) -> None:
        """
        Called to 'press jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node:
            return
        if don.jumpFly:
            self.node.handlemessage("impulse",self.node.position[0],self.node.position[1]-2,self.node.position[2],self.node.velocity[0]*0,20 +0.01,self.node.velocity[2]*0,10,5,0,0,self.node.velocity[0]*-0.1,20 + 0.01,self.node.velocity[2]*0)
            self.node.handlemessage("impulse",self.node.position[0],self.node.position[1],self.node.position[2],self.node.velocity[0]*0,20 +0.01,self.node.velocity[2]*0,10,5,0,0,self.node.velocity[0]*-0.1,20 + 0.01,self.node.velocity[2]*0)
        self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
        self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5)) 
        self.node.jump_pressed = True
        self._turbo_filter_add_press('jump')
        
    def equip_shields(self, decay: bool = False) -> None:
        """
        Give this spaz a nice energy shield.
        """

        if not self.node:
            ba.print_error('Can\'t equip shields; no node.')
            return

        factory = SpazFactory.get()
        if self.shield is None:
            self.shield = ba.newnode('shield',
                                     owner=self.node,
                                     attrs={
                                         'color': ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5)), 
                                         'radius': 1.3
                                     })
            self.node.connectattr('position_center', self.shield, 'position')
            #ba.animate_array(self.shield, 'color', 3,{0:(1,0,0),0.2:(1,0.5,0),0.4:(1,1,0),0.6:(0,1,0),0.8:(0,1,1),1.0:(0,0,1),1.2:(1,0,0)},True)
        self.shield_hitpoints = self.shield_hitpoints_max = 650
        self.shield_decay_rate = factory.shield_decay_rate if decay else 0
        self.shield.hurt = 0
        ba.playsound(factory.shield_up_sound, 1.0, position=self.node.position)

        if self.shield_decay_rate > 0:
            self.shield_decay_timer = ba.Timer(0.5,
                                               ba.WeakCall(self.shield_decay),
                                               repeat=True)
            # So user can see the decay.
            self.shield.always_show_health_bar = True

    Spaz.__init__ = _new_init
    Spaz.on_punch_press = on_punch_press
    Spaz.on_jump_press = on_jump_press
    Spaz.equip_shields = equip_shields
