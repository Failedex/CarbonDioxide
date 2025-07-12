#!/usr/bin/env python3

import gi
gi.require_version('Playerctl', '2.0')
from gi.repository import Playerctl, GLib

def on_play(player, status):
    print('player is playing: {}'.format(player.props.player_name))


def on_metadata(player, metadata):
    keys = metadata.keys()
    if 'xesam:artist' in keys and 'xesam:title' in keys:
        print('{} - {}'.format(metadata['xesam:artist'][0],
                               metadata['xesam:title']))


def init_player(name, manager):
    player = Playerctl.Player.new_from_name(name)
    player.connect('playback-status::playing', on_play)
    player.connect('metadata', on_metadata)
    manager.manage_player(player)


class Manager(Playerctl.PlayerManager):
    def __init__(self): 
        super().__init__()
        self.connect('name-appeared', self.on_name_appeared)
        self.connect('player-vanished', self.on_player_vanished)

        for name in self.props.player_names:
            init_player(name, self)

        main = GLib.MainLoop()
        main.run()

    def on_name_appeared(self, manager, name):
        init_player(name, self)

    def on_player_vanished(self, manager, player):
        print('player has exited: {}'.format(player.props.player_name))

manager = Manager()
