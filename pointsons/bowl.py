class Bowl(object):
    """
    Un bol est décrit par les éléments suivants :
    
     - un nom (une chaîne de caractère) ;
     
     - la main à observer (0 : main droite , 1 : main gauche , 2 : les
       deux mains) ;

     - une position dans l'espace (toujours 3 entiers en mm par
       rapport au même point de référence) ;
     
     - un rayon (en mm).
    """
    note = None
    position = (0, 0, 0) # mm, from reference point
    radius = 0 # mm
    #velocity = 127
