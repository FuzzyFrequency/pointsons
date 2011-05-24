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
import yaml
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from pointsons import logger

from .utils import Borg, Observable

class Configuration(Observable):
    """
    A generic configuration system for the pointsons installation
    """
    def __init__(self, config_path):
        self.config_path = config_path
    
    label = u"Sans nom"
    chords = []
    bowls = {}
    camera = None
    area = None

    ratioEyeBodySize = 94 # un pourcentage définissant la hauteur des yeux par rapport à la hauteur totale d'une personne
    ratioCylinderRayFromShouldersSpace = 120 # pourcentage par rapport au tronc de l'utilisateur en dehors duquel les membres sont pris en compte
    proximityCenterForHeadCalculation = 200 # distance maximale pour prendre en compte les pixels n'appartenant pas aux membres
    armBlobNumbermin = 100 # nombre de pixels minimum à partir duquel un membre se distingue d'une protubérance due au bruit de l'image
    croppingXMin = 0 # abscisse minimale de l'image à partir de laquelle prendre en compte les pixels
    croppingXMax = 640 # abscisse maximale de l'image jusque laquelle prendre en compte les pixels
    croppingYMin = 0 # ordonnée minimale de l'image à partir de laquelle prendre en compte les pixels
    croppingYMax = 480 # ordonnée maximale de l'image jusque laquelle prendre en compte les pixels
    lowPassFilter = 0 # activer/désactiver les filtres passe-bas
    eyeDepthOffset = 30 # décalage des yeux vers l'intérieur de la tête (en mm,pour atténuer la différence d'œil directeur chez les utilisateurs)
    bodyDepthOffset = 100 # décalage de la position de l'utilisateur pour compenser la prise en compte des pixels de surface (en mm)
    armSquaredDistanceThreshold = 900 # seuil de séparation des bras sur des pixels voisins lorsque les bras sont superposés dans l'image
    ratioArmLengthFromHeight = 75 # pourcentage définissant la longueur d'un bras tendu (sans la main) à partir de la hauteur d'une personne
    ratioHeightWidthMin = 50 # pourcentage indiquant la largeur minimum du tronc d'une personne à partir de sa taille (utile quand des entités passent entre la caméra et l'utilisateur provoquant une largeur de l'utilisateur de 0)
    userProfile = "TwoHands" # profil de l'utilisateur pour utiliser une ou deux mains (autres profils disponibles : RightHand et LeftHand)

    def save(self):
        thefile = open(self.config_path, 'wb')
        data = yaml.dump(self, Dumper=Dumper)
        thefile.write(data)
        thefile.close()

    @staticmethod
    def load(config_path):
        thefile = open(config_path, 'rb')
        config = yaml.load(thefile)

        # FIXME: Monkey patching
        #if config.camera is None:
        #    config.camera = Camera()
        
        #if config.area is None:
        #    config.area = Area()

        return config

class Configurations(Borg):
    current = None

    def load_configuration(self, config_path):
        self.current = Configuration.load(config_path)

    def save(self, config_path):
        self.current.save(config_path)

    def set_current(self, aConfiguration):
        self.current = aConfiguration
        logger.info("Switching to config '%s'" % aConfiguration.label)
