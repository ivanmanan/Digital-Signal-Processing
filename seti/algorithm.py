import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time

Star_List = []

class Star:
    name = ''
    analyst = ''
    ra = ''
    dec = ''
    gal_lon = ''
    gal_lat = ''
    parallax = ''

# Parse starlist first
path = './starlist.txt'
with open(path, 'r') as f:
    lines = f.readlines()

    # This gives me a for-loop for each line in the txt file
    for j in lines:
        new_star = Star()
        new_name = ''
        new_analyst = ''
        new_ra = ''
        new_dec = ''
        new_gal_lon = ''
        new_gal_lat = ''
        new_parallax = ''
        count = 0;

        # Parse Star Names
        while not j[count].isspace():
            new_name = new_name + j[count]
            count = count+1

        # Loop through next whitespaces
        while j[count].isspace():
            count = count+1

        # Parse Analyst Names
        while not j[count].isspace():
            new_analyst = new_analyst + j[count]
            count = count+1

        # Loop through next whitespaces
        while j[count].isspace():
            count = count+1

        # Parse RA
        whitespaces = 0
        while whitespaces < 3:
            if j[count].isspace():
                whitespaces = whitespaces + 1
                if whitespaces == 3:
                    break
            new_ra = new_ra + j[count]
            count = count+1

        # Loop through next whitespaces
        while j[count].isspace():
            count = count+1

        # Parse DEC
        whitespaces = 0
        while whitespaces < 3:
            if j[count].isspace():
                whitespaces = whitespaces + 1
                if whitespaces == 3:
                    break
            new_dec = new_dec + j[count]
            count = count+1

        # Loop through next whitespaces
        while j[count].isspace():
            count = count+1

        # Parse galactic longitude
        while not j[count].isspace():
            new_gal_lon = new_gal_lon + j[count]
            count = count+1

        # Loop through next whitespaces
        while j[count].isspace():
            count = count+1

        # Parse galactic latitude
        while not j[count].isspace():
            new_gal_lat = new_gal_lat + j[count]
            count=count+1

        # Loop through next whitespaces
        while j[count].isspace():
            count = count+1

        ### Take rest of parallax until end of line
        while count < len(j)-1:
            new_parallax = new_parallax + j[count]
            count=count+1

        new_star.name = new_name
        new_star.analyst = new_analyst
        new_star.ra = new_ra
        new_star.dec = new_dec
        new_star.gal_lon = new_gal_lon
        new_star.gal_lat = new_gal_lat
        new_star.parallax = new_parallax
        Star_List.append(new_star)


# NUMBER = 0
# print(Star_List[NUMBER].name)
# print(Star_List[NUMBER].analyst)
# print(Star_List[NUMBER].ra)
# print(Star_List[NUMBER].dec)
# print(Star_List[NUMBER].gal_lon)
# print(Star_List[NUMBER].gal_lat)
# print(Star_List[NUMBER].parallax)

f.close()


## Now design algorithm that maps it

fig,ax =plt.subplots()


# Convert RA and DEC to degree values

i = 0
Right_Ascension = 0
Declination = 0

while i < 16:

    # Gather Right Ascension
    string_hour = ''
    string_hour_decimal = ''
    j = 0

    # Get hours
    while not Star_List[i].ra[j].isspace():
        string_hour = string_hour + Star_List[i].ra[j]
        j = j+1

    # There is a whitespace
    string_hour = string_hour + '.'
    j = j+1

    while not Star_List[i].ra[j].isspace():
        string_hour_decimal = string_hour_decimal + Star_List[i].ra[j]
        j = j+1

    number_hour_decimal = float(string_hour_decimal)/60
    number_hour = float(string_hour)
    number_hour = (number_hour + number_hour_decimal) * 15 * 60 # Convert to arcminutes
    #print number_hour

    # Gather Declination
    string_degree = ''
    string_degree_decimal = ''
    j = 0
    while not Star_List[i].dec[j].isspace():
        string_degree = string_degree + Star_List[i].dec[j]
        j = j+1

    # There is a whitespace
    string_degree = string_degree + '.'
    j = j+1

    while not Star_List[i].dec[j].isspace():
        string_degree_decimal = string_degree_decimal + Star_List[i].dec[j]
        j = j+1

    number_degree_decimal = float(string_degree_decimal)/60
    number_degree = float(string_degree)
    number_degree = (number_degree + number_degree_decimal) * 60 # Convert to arcminutes
    #print number_degree
    i = i+1

    # Plot
    plt.plot([number_hour], [number_degree], 'bo')
    beam_size = plt.Circle((number_hour, number_degree), 8.9, color='r', fill='false')
    ax.add_artist(beam_size)

#plt.axis([5.5, 7, -5, 35])
plt.xlabel('Right Ascension (arcmins)')
plt.ylabel('Declination (arcmins)')
plt.show()