import herepy
# import json
import yaml
import pandas
import re

'''
    Helpers
'''


def places_init(filename):
    '''
    Initialize Here.com Places API with credentials from yaml file
    :param filename:  string for file containing credentials in yaml format
    :return:
    '''

    with open(filename, 'r') as f:
        credentials = yaml.safe_load(f)
        f.close()

    app_id = credentials['app_id']
    app_code = credentials['app_code']

    return(herepy.PlacesApi(app_id, app_code))


def at_nearby(desc, lat, long, fmts='\.|\/'):
    '''
    Write nearby places and places at out of home placements to text files.
    :param desc: name of the column containing placement description in filename
    :param lat: name of the column containing latitude in filename
    :param long: name of the column containing longitude in filename
    :param fmts: regular expression for characters to remove from desc when writing to file
    :return: None
    '''

    desc = re.sub(fmts, '', desc)
    fname = desc + '.txt'
    coordinates = [lat, long]

    at_request = placesApi.places_at(coordinates)
    at_request = at_request.as_dict()
    # at_response = json.dumps(at_request, sort_keys=True, indent=4)

    nearby_request = placesApi.nearby_places(coordinates)
    nearby_request = nearby_request.as_dict()
    # nearby_response = json.dumps(nearby_request, sort_keys=True, indent=4)

    with open(fname, 'w') as f:
        f.write('NEARBY \n\n')
        for entry in nearby_request['results']['items']:
            f.write(str(entry['title'])+'\n')
            f.write(str(entry['position'])+'\n')
            f.write(str(entry['distance'])+'\n')
            f.write(str(entry['vicinity'])+'\n\n')

        f.write('PLACES AT \n\n')
        for entry in at_request['results']['items']:
            f.write(str(entry['title'])+'\n')
            f.write(str(entry['position'])+'\n')
            f.write(str(entry['distance'])+'\n')
            f.write(str(entry['vicinity'])+'\n\n')
        f.close()


'''
    Run
'''


def WriteResults(filename, desc, lat, long):
    '''
    Read input csv and call at_nearby function to write results to text files
    One text file for every row (i.e. placement) in the input csv
    :param filename: string of the filename containing out of home placements in .csv format
    :param desc: name of the column containing placement description in filename
    :param lat: name of the column containing latitude in filename
    :param long: name of the column containing longitude in filename
    :return: None
    '''
    activations = pandas.read_csv(filename, skipinitialspace=True)

    activation_description = activations[desc]
    activations_latitude = activations[lat]
    activations_longitude = activations[long]

    list(map(at_nearby, activation_description, activations_latitude, activations_longitude))


placesApi = places_init(filename='credentials.yaml')


WriteResults(filename='placements.csv', desc='Location', lat='Latitude', long='Longitude')
