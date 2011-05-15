
class Camera(objects):
    """
    La caméra doit absolument être configurée dès le départ du
    programme. Sa configuration nécessite 4 paramètres :

     - 3 entiers en mm pour sa position dans l'espace(par rapport au
    point de référence choisi pour tout configurer);

     - 1 entier en degrés pour son orientation (de -27 si elle regarde
    vers le haut à 27 si elle regarde vers le bas).
    """
    position = (x, y, z) # mm, from reference point
    orientation = 0 # from -27 (looking at the sky) to +27 (looking at the floor)
