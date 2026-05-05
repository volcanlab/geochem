import numpy as np

def getnames_all():
    COLUMN_NAMES = ['SiO2', 'Al2O3', 'TiO2', 'FeO', 'Fe2O3', 'FeOT', 'CaO', 'MgO', \
                    'MnO', 'Na2O', 'K2O', 'P2O5', \
                    'Cu', 'V', 'Cr', 'Co', 'Ni', 'Zn',\
                    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Ba', 'Pb', 'Sc', 'Ga', 'Cs', 'Hf',\
                    'Ta', 'Th', 'U', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',\
                    'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', \
                    'As', 'Au', 'Hg', 'I', 'Mo', 'Re', 'Sb', 'Se', 'Te', 'W',\
                    'Ag', 'Bi', 'Cd', 'Ge', 'In', 'Sn', 'Tl', 'Ti',\
                    'Os', 'Pd', 'Pt', 'Ru', 'Be', 'Li', 'Mn', \
                    'Al', 'Ca', 'Mg', 'Na', 'K', 'Fe', 'P', 'S',\
                    'Cr2O3', 'SO3', 'SO4', 'SO2', 'HCl', 'HF', 'Cl', 'CO2', 'H2O', 'Br','Mg#',\
                    'X', 'Y', 'Z'
                    ] 
    return COLUMN_NAMES

def getnames_major():
    MAJOR_OXIDES = ['SiO2', 'Al2O3', 'TiO2', 'FeOT', 'CaO', 'MgO', \
                    'MnO', 'Na2O', 'K2O', 'P2O5'
                    ]
    return MAJOR_OXIDES

def getnames_REE():
    REE = ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', \
            'Er', 'Tm', 'Yb', 'Lu'
            ]
    return REE

def getnames_trace():
    trace = ['Cs', 'Rb', 'Ba', 'Th', 'U', 'Nb', 'K', 'La', 'Ce', 'Pb', \
            'Pr', 'Sr', 'P', 'Nd', 'Zr', 'Sm', 'Eu', 'Ti', 'Dy', 'Y', 'Yb', 'Lu'
            ]
    return trace

def getvalues_SM89(source='chondrite'):
    """
    getvalues_SM89(source='chondrite')

    Sun and McDonough (1989) dataset
    source = "chondrite" -> C1 chondrite
    source = "mantle"    -> Primtive Mantle
    source = "nmorb"     -> N-type MORB

    Returns a dictionary with the values for the selected source.
    The values are in ppm.
    """
    if source == 'chondrite':
        values = {'Source': 'C1 chondrite',\
                'Cs': 0.188, 'Tl': 0.140, 'Rb': 2.32 , 'Ba': 2.41, 'W': 0.095,\
                'Th': 0.029, 'U':  0.008, 'Nb': 0.246, 'Ta': 0.014,'K': 545,\
                'La': 0.237, 'Ce': 0.612, 'Pb': 2.47 , 'Pr': 0.095,'Mo':0.92,\
                'Sr': 7.26,  'P':  1220 , 'Nd': 0.467, 'F':  60.7, 'Sm':0.153,\
                'Zr': 3.87,  'Hf': 0.1066,'Eu': 0.058, 'Sn': 1.72, 'Sb':0.16,\
                'Ti': 445,   'Gd': 0.2055,'Tb': 0.0374,'Dy': 0.2540,'Li':1.57,\
                'Y':  1.57,  'Ho': 0.0566,'Er': 0.1655,'Tm': 0.0255,'Yb':0.170,\
                'Lu': 0.0254 \
                }
    elif source == 'mantle':
        values = {'Source': 'Primitive Mantle',\
                'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989,'W': 0.020,\
                'Th': 0.085, 'U':  0.021, 'Nb': 0.713, 'Ta': 0.041,'K': 250,\
                'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276,'Mo':0.063,\
                'Sr': 21.1,  'P':  95   , 'Nd': 1.354, 'F':  26,   'Sm':0.444,\
                'Zr': 11.2,  'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.170,'Sb':0.005,\
                'Ti': 1300,  'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.737,'Li':1.60,\
                'Y':  4.55,  'Ho': 0.164, 'Er': 0.480, 'Tm': 0.074,'Yb':0.493,\
                'Lu': 0.074 \
                }
    elif source == 'nmorb':
        values = {'Source': 'N-type MORB',\
                'Cs': 0.007, 'Tl': 0.0014,'Rb': 0.56,  'Ba': 6.30, 'W': 0.01,\
                'Th': 0.120, 'U':  0.047, 'Nb': 2.33,  'Ta': 0.132,'K': 600,\
                'La': 2.50,  'Ce': 7.50,  'Pb': 0.30,  'Pr': 1.32, 'Mo':0.31,\
                'Sr': 90,    'P':  510  , 'Nd': 7.30,  'F':  210,  'Sm':2.63,\
                'Zr': 74,    'Hf': 2.05 , 'Eu': 1.02,  'Sn': 1.1,  'Sb':0.01,\
                'Ti': 7600,  'Gd': 3.680, 'Tb': 0.670, 'Dy': 4.550,'Li':4.3,\
                'Y':  28,    'Ho': 1.01,  'Er': 2.97,  'Tm': 0.456,'Yb':3.05,\
                'Lu': 0.455 \
                }
    else:
        values ={}

    return values

def getvalues_IB71():
    """
    The coordinates for Irvine and Baragar's boundary are (A, F, M): 
    58.8, 36.2, 5.0; 
    47.6, 42.4, 10.0; 
    29.6, 52.6, 17.8; 
    25.4, 54.6, 20.0; 
    21.4, 54.6, 24.0; 
    19.4, 52.8, 27.8; 
    18.9, 51.1, 30.0; 
    16.6, 43.4, 40.4; 
    15.0, 35.0, 50.0 
    (from Rickwood, 1989; Rollinson, 1993). 

    Returns three numpy arrays A, F, M with the values for the coordinates.
    The values are in wt% for A, F and M.
    """    

    A = [58.8, 47.6, 29.6, 25.4, 21.4, 19.4, 18.9, 16.6, 15.0]
    F = [36.2, 42.4, 52.6, 54.6, 54.6, 52.8, 51.1, 43.4, 35.0]
    M = [ 5.0, 10.0, 17.8, 20.0, 24.0, 27.8, 30.0, 40.4, 50.0]

    return np.array(A), np.array(F), np.array(M)

def getvalues_IB71xy():
    """
    The coordinates x-y can be calculated with this code:

    import numpy as np

    x = np.array([58.8, 47.6, 29.6, 25.4, 21.4, 19.4, 18.9, 16.6, 15.0])
    y = np.array([36.2, 42.4, 52.6, 54.6, 54.6, 52.8, 51.1, 43.4, 35.0])
    z = np.array([ 5.0, 10.0, 17.8, 20.0, 24.0, 27.8, 30.0, 40.4, 50.0])

    s  = 2*(x+y+z)
    xt = (y+(2*z))/s
    yt = y*np.sqrt(3)/s

    Returns two numpy arrays xt and yt with the values for the coordinates.
    """
    # Coordinates for Irvine and Baragar's boundary 
    xt = [0.231, 0.312, 0.441, 0.473, 0.513, 0.542, 0.5555, 0.6185259, 0.675]
    yt = [0.3135012, 0.36719477, 0.45552936, 0.47284987, 0.47284987, \
          0.45726141, 0.44253898, 0.37435759, 0.30310889]
    
    return np.array(xt), np.array(yt)
    

