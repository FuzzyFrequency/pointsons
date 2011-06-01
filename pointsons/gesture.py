# -*- coding: utf-8 -*-
#
# Pointsons
#
# Copyright (C) 2011 Guillaume Libersat <guillaume@fuzzyfrequency.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#

from .utils import Observable

class AbstractGesture(Observable):
    """
    Chaque message “Move” ajoutera un mouvement à reconnaître dans une direction. Chaque message devra donc comporter un nom, la main à observer, et des indications sur la direction à observer : 3 entiers définissant des directions comme suit.

    [0,0,0] : vers l'utilisateur;
    [2,2,2] : à partir de l'utilisateur;
    ou des combinaisons des éléments suivants (en évitant les deux combinaisons précédentes):

     - le premier entier défini l'axe gauche-droite : -1 vers la gauche, 0 pas prise en compte de cet axe et 1 vers la droite ;
     - le deuxième entier défini l'axe bas-haut : -1 vers le bas, 0 pas prise en compte de cet axe et 1 vers le haut ;
     - le dernier entier défini l'axe avant-arrière : -1 vers l'avant, 0 pas prise en compte de cet axe et 1 vers l'arrière.

    """
    name = u"[undefined gesture]"
    direction = (0, 0, 0)
    hands = 2


        

        



