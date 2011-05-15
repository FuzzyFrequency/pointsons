import pickle

FILENAME = 'save.pss'

class Configuration(object):
    label = ""
    chords = []
    bowls = []
    camera = None
    area = None

    RatioEyeBodySize = 94 # un pourcentage définissant la hauteur des yeux par rapport à la hauteur totale d'une personne
    RatioCylinderRayFromShouldersSpace = 120 # pourcentage par rapport au tronc de l'utilisateur en dehors duquel les membres sont pris en compte
    ProximityCenterForHeadCalculation = 200 # distance maximale pour prendre en compte les pixels n'appartenant pas aux membres
    ArmBlobNumbermin = 100 # nombre de pixels minimum à partir duquel un membre se distingue d'une protubérance due au bruit de l'image
    CroppingXMin = 0 # abscisse minimale de l'image à partir de laquelle prendre en compte les pixels
    CroppingXMax = 640 # abscisse maximale de l'image jusque laquelle prendre en compte les pixels
    CroppingYMin = 0 # ordonnée minimale de l'image à partir de laquelle prendre en compte les pixels
    CroppingYMax = 480 # ordonnée maximale de l'image jusque laquelle prendre en compte les pixels
    LowPassFilter = False # activer/désactiver les filtres passe-bas
    EyeDepthOffset = 30 # décalage des yeux vers l'intérieur de la tête (en mm,pour atténuer la différence d'œil directeur chez les utilisateurs)
    BodyDepthOffset = 100 # décalage de la position de l'utilisateur pour compenser la prise en compte des pixels de surface (en mm)
    ArmSquaredDistanceThreshold = 900 # seuil de séparation des bras sur des pixels voisins lorsque les bras sont superposés dans l'image
    RatioArmLengthFromHeight = 75 # pourcentage définissant la longueur d'un bras tendu (sans la main) à partir de la hauteur d'une personne
    RatioHeightWidthMin = 50 # pourcentage indiquant la largeur minimum du tronc d'une personne à partir de sa taille (utile quand des entités passent entre la caméra et l'utilisateur provoquant une largeur de l'utilisateur de 0)
    UserProfile = "TwoHands" # profil de l'utilisateur pour utiliser une ou deux mains (autres profils disponibles : RightHand et LeftHand)

    

    def save(self):
        thefile = open(FILENAME, 'wb')
        pickle.dump(self, thefile)
        thefile.close()

    @static
    def load(self):
        thefile = open(FILENAME, 'rb')
        pickle.load(self, thefile)
        thefile.close()


    
