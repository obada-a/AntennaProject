import math
from pylab import*

# the function takes in input the number of array elements "n" and 
# the attenuation of the secondary lobes compared to the main lobe
def chebyParam( n , r ):
    n = float(n)
    r = float(r)
    iterator = math.cosh(1/n * math.acosh(r))
    a = (( iterator - 1 ) / 2 ).real
    b = (( iterator + 1 ) / 2 ).real
    #returns the list of chebyshev's parameters
    return [ a , b ]

#chebyshev's parameters and optimized distance value btw array elements
def chebyParamOptimized(n , r , k0 ):
    n = float(n)
    r = float(r)
    iterator = math.cosh(1/n * math.acosh(r))
    a = (( iterator - 1 ) / 2 ).real
    b = (( iterator + 1 ) / 2 ).real
    optimized_dist = ( 2*math.pi - math.acos((1 - a)/b)) / k0
    output = open("valori_a_b.txt",'a')
    output.write(" a = " + str(a) + " b = " + str(b) + "  N = " + str( n*2+1) + "\n")
    output.close()
    print( "N="+str(n*2+1) + "  d=" + str(optimized_dist))
    return [ a , b , optimized_dist]

# the function takes in input the chebyshev's parameters and returns the 
# excitation coefficients

def excitCoeff( n , a, b):
    if n not in range(2,5):
        raise Exception("The number isn't in the range [ 2 , 4 ]")
    # 5 elements array
    def five_elem():
        k0 = 2*a**2 + b**2 - 1
        k1 = 4*a*b/2
        k2 = b**2/2
        return [ k0 , k1 , k2 ]
    #7 elements array
    def seven_elem():
        k0 = 4*a**3 + 6*a*b**2 - 3*a
        k1 = ( 12*a**2*b +3*b**3 - 3*b )/2
        k2 = ( 6*a*b**2 )/2
        k3 = b**3/2
        return [ k0 , k1 , k2 , k3 ]
    #9 elements array
    def nine_elem():
        k0 = -8*a**2 + 8*a**4 - 4*b**2 + 3*b**4 + 24*a**2*b**2 +1
        k1 = (24*a*b**3 + 32*a**3*b - 16*a*b)/2
        k2 = (4*b**4 - 4*b**2 + 24*a**2*b**2)/2
        k3 = 8*a*b**3/2
        k4 = b**4/2
        return [ k0 , k1 , k2 , k3 , k4 ]

    feed_coeff = { 2 : five_elem , 3 : seven_elem , 4 : nine_elem }
    return feed_coeff[n]()

#the function takes in input the excitation coefficients, the distance between array elements, 
#the angle of orientation
#returns the array factor

def arrayFactor( coeff , dist , angle , k0 ):
    u = k0 * dist * cos((angle*pi)/180)
    f = zeros(len(angle))
    for item in range(0,len(angle)):
        f[item] = coeff[0]
        for item2 in range(1,len(coeff)):
            f[item] = f[item] + 2*coeff[item2]*cos(item2*u[item])
    return f


# Chebyshev sysnthesis

def chebyshevSynthesis( f0 , r , angle , gain , n ):

    gain = 10**(array(gain)/10)
    c = float(3*(10**8))
    #wave length
    r = 10**(r/20)
    lambda_0 = c/float(f0)
    k0 = 2*math.pi/lambda_0
    psi = 90 - np.array(angle)
    m = int(ceil(( n-1 )/2))
    params = chebyParamOptimized( m , r , k0)
    excitation_coeff = excitCoeff( m, params[0] , params[1] )
    array_factor = np.array(arrayFactor( excitation_coeff, params[2] , psi , k0))
    #square absolute value of the array factor
    abs_array_factor = abs(np.array(array_factor))**2

    # the sum of the absolute values of the excitation parameters
    sum_coeff = sum( abs(array(excitation_coeff))**2)*2 - abs(excitation_coeff[1])**2 
    
    array_factor_gain = abs_array_factor/float(sum_coeff)
    #the gain of the antenna
    system_gain = array_factor_gain * gain
    db_system_gain = 10*log10(system_gain)

    
    max_gain = max(db_system_gain)
    
    db_3_gain = 0
    teta_3_db = -1

    for  item in range(1, len(angle)):
        if db_system_gain[item] == db_3_gain :
            teta_3_db = angle[item]
            break
        elif db_system_gain[item] < db_3_gain:
            teta_3_db = angle[item - 1]
            break
    

    if teta_3_db == -1 :
        print(" Impossible to calculate the beamwidth ")
    print(teta_3_db)
    bw = 2*teta_3_db

    return [ array_factor , array_factor_gain , system_gain , max_gain , bw ]


def chebySynthesisDistance( f0 , r , angle , gain , n , dist ):
    c = float(3*10**8)
    r = 10**(r/20)
    lambda_0 = c/float(f0)
    k0 = 2*math.pi/lambda_0
    psi = 90 - array(angle)
    m = int(ceil((n-1)/2))
    params = chebyParam( m , r )
    excitation_coeff = excitCoeff( m , params[0] , params[1] )
    array_factor = arrayFactor(excitation_coeff , dist , psi , k0 )
    abs_array_factor = abs(array_factor)**2
    sum_coeff = sum(abs(array(excitation_coeff))**2)*2 - abs(excitation_coeff[1])**2
    array_factor_gain = abs_array_factor/float(sum_coeff)
    system_gain = array_factor_gain*gain
    db_system_gain = 10*log10(system_gain)
    max_gain = max(system_gain)
    db_max_gain = max(db_system_gain)
    db_3_gain = db_max_gain - 3
    print(db_system_gain)
    teta_3_db = -1
    for  item in range(0, len(angle)):
        if db_system_gain[item] == db_3_gain: 
            teta_3_db = angle[item]
            break
        elif db_system_gain[item] < db_3_gain:
            teta_3_db = angle[item - 1]                                                         
            break
        
    if teta_3_db == -1 :
        print(" Impossible to calculate the beamwidth ")

    bw = 2*teta_3_db
    return [ array_factor , array_factor_gain , system_gain , max_gain , bw ]

def plot_function(axes,values , names ):
    m = values[0]
    g=[]
    for item in axes:
        g.append(-1*item)
    g = g[::-1]
    axes = g + axes
    values = array(list(values[::-1])+list(values))
    plot(axes,values)
    ylim(-60,35)
    xlim(-90,90)
    annotate(str(m)[0:5], xy=(5, m+6), xytext=(5, m+6),bbox=dict(boxstyle="larrow", fc="w"), rotation = 35)
    grid(True)

    ylabel(names[0])
    xlabel(names[1])
    title(names[2])
    
