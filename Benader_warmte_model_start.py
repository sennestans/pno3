#Benadering model warmtecircuit: begin van berekingen
def benader_warmte_model_start(T_out, S_rad):           #functie om het warmtemodel te benaderen
                                                        #input:
                                                        # lijst met buitentemperaturen (K)
                                                        # lijst met solar radiation (W)
                                                        #output:
                                                        # lijst met binnentemperaturen (Celsius)
                                                        # lijst met temperaturen van de bouwmassa (Celsius)

    #importeren van modules
    import numpy as np
    import matplotlib.pyplot as plt

    #functions
    def extend_list(L, N):              #functie om lijsten te verlengen
        temp_list = []                  #maak een tijdelijke lijst
        for i in L:                     #voor elk element in de lijst L
            temp_list.extend([i] * N)   #voeg het element N keer toe aan de tijdelijke lijst
        return temp_list                #geef de tijdelijke lijst terug

    def extend_list(L, N):              #functie om lijsten te verlengen
        temp_list = []                  #maak een tijdelijke lijst
        for i in L:                     #voor elk element in de lijst L
            temp_list.extend([i] * N)   #voeg het element N keer toe aan de tijdelijke lijst
        return temp_list                #geef de tijdelijke lijst terug

    #string to float
    T_out = [float(i) for i in T_out]   #omzetten van lijst met temperaturen (K) in strings naar lijst met floats
    S_rad = [float(i) for i in S_rad]   #omzetten van lijst met solar radiation (W) in strings naar lijst met floats

    #Celsius to Kelvin
    T_out = [i + 273.15 for i in T_out] #omzetten van lijst met temperaturen van Celsius naar Kelvin

    # Define parameters
    t0 = 0                  #begintijdstip
    t_end = 24*60*60        #aantal seconden in een dag
    N = 2                   #nauwkeurigheid benadering: N=2 => berekening om het half uur, N=4 => berekening om het kwartier
    n = N*24                #aantal stappen = ieder uur opgedeeld in 2 stappen => elk half uur een stap
    h = (t_end-t0)/(n)      #stapgrootte, dag wordt opgedeeld in 48 stukken van een half uur
    T_in_0 = 20 + 273.15    #binnentemperatuur begint op 20 graden (arbitrair)
    T_m_0 = 18 + 273.15     #begintemperatuur van de bouwmassa is 18 graden (arbitrair)

    #aanpassen lengte van lijsten om te matchen met n: 1 waarde per half uur/kwartier
    T_out = extend_list(T_out, N)           #lengte van lijst met buitentemperaturen (K) aanpassen
    S_rad = extend_list(S_rad, N)           #lengte van lijst met solar radiation (W) aanpassen

    # Parameters van de vergelijkingen van het model
    C_i = 2.44*10**6                    #warmtecapaciteit van de binnenlucht (J/K)
    C_m = 9.40*10**7                    #warmtecapaciteit van de bouwmassa (J/K)
    R_i = 8.64*10**(-4)                 #warmteweerstand van de binnenlucht naar de muur (K/W)
    R_e = 1.05*10**(-2)                 #warmteweerstand van de muur naar de buitenlucht (K/W)
    R_vent = 7.98*10**(-3)              #warmteweerstand van temperatuurverlies door ventilatie (K/W)
    gA = 12                             #solar gain factor (m^2)
    frad = 0.3                          #distributiefactor van warmtepomp (constante)
    CoP = 3                             #COP van de warmtepomp (constante) (arbitrair)
    P_in = np.zeros(n)                  #benadering van warmtemodel waarin warmtepomp nog niet aanstaat => P_in = 0 altijd

    #Voorwaartse methode van Euler
    T_in = np.zeros([n])            #initialisatie lijst met binnentemperaturen
    T_m = np.zeros([n])             #initialisatie lijst met temperaturen van de bouwmassa
    T_in[0] = T_in_0                #initialisatie begintemperatuur van de binnentemperatuur
    T_m[0] = T_m_0                  #initialisatie begintemperatuur van de bouwmassa

    for i in range(1,n):                                                                                                            #voor n tijdstappen van lengte h
        T_in[i] = T_in[i-1] + h * (1/C_i)*(P_in[i-1]*(1-frad)*CoP - (T_in[i-1]-T_out[i-1])/R_vent - (T_in[i-1]-T_m[i-1])/R_i)       #benadering van de binnentemperatuur na tijdstap h
        T_m[i] = T_m[i-1] + h * (1/C_m)*(P_in[i-1]*frad*CoP+gA*S_rad[i-1] - (T_m[i-1]-T_out[i-1])/R_e - (T_m[i-1]-T_in[i-1])/R_i)   #benadering van de temperatuur van de bouwmassa na tijdstap h

    '''#plot resultaten
    t = np.linspace(t0,t_end, n)                            #tijd wordt opgedeeld in n gelijke stukken van lengte h
    plt.figure("Temperatuur")                               #maak een figuur met naam "Temperatuur"
    plt.plot(t/(60*60),T_in-273.15,'b', label='T_in')       #plot binnentemperatuur (Celsius) i.f.v. tijd (uur)
    plt.plot(t/(60*60),T_m-273.15,'g', label='T_m')         #plot temperatuur (Celsius) van de bouwmassa i.f.v. tijd (uur)
    plt.xlabel('Tijd (uur)')                                #label x-as
    plt.ylabel('Temperatuur (°C)')                          #label y-as
    plt.title('Binnen- en buitentemperatuur zonnehuis')     #titel van de grafiek
    plt.grid()                                              #raster op de grafiek
    plt.legend(loc='upper right')                           #legende rechtsboven
    plt.figure("Warmtepomp")                                #maak een figuur met naam "Warmtepomp"
    plt.plot(t/(60*60),P_in)                                #plot vermogen (W) van de warmtepomp i.f.v. tijd (uur)
    plt.xlabel('Tijd (uur)')                                #label x-as
    plt.ylabel('Vermogen (W)')                              #label y-as
    plt.title('Vermogen van de warmtepomp')                 #titel van de grafiek
    plt.grid()                                              #raster op de grafiek
    plt.show()                                              #toon de grafieken
    Handig?'''

    #data terugsturen naar controller.py
    T_in = [round(elem, 2) for elem in list(T_in-273.15)]    #omzetten van numpy array naar lijst met afronding op 2 decimalen; Celsius naar Kelvin
    T_m = [round(elem, 2) for elem in list(T_m-273.15)]      #omzetten van numpy array naar lijst met afronding op 2 decimalen; Celsius naar Kelvin
    T_in = shorten_list(T_in, N)                             #lengte van lijst met binnentemperaturen (Celsius) aanpassen: 1 waarde per uur
    T_m = shorten_list(T_m, N)                               #lengte van lijst met temperaturen van de bouwmassa (Celsius) aanpassen: 1 waarde per uur
    return T_in, T_m                                         #terugsturen van de lijsten met binnentemperatuur en temperatuur van de bouwmassa