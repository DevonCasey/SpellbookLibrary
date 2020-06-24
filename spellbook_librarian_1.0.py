import glob
import pandas
from flask import Flask
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np

def get_spellbook():
    new_spellbook_choice = input('Would you like to make a new spellbook (y/n): ')
    if new_spellbook_choice == 'y':
        temp_user_class_storage = []
        temp_user_spell_storage = []  # empty temp storage for an array of user inputs
        temp_user_feature_storage = []
        spell_entry = ''  # start off with an empty string to keep asking user for input
        feature_entry = ''
        user_class = input('Enter your class (i.e. "Cleric"): ')
        user_class = temp_user_class_storage.append(user_class)

        while spell_entry != 'stop':  # keep asking for input until stop is entered
            spell_entry = input('Enter spell name (i.e "Magic Missile" OR "stop" when done): ')
            if spell_entry != 'stop':  # to keep 'stop' from being added to the list
                temp_user_spell_storage.append(spell_entry)
            else:
                continue

        while feature_entry != 'stop':
            feature_entry = input('Enter feature name (i.e "Blind Spot" OR "stop" when done): ')
            if feature_entry != 'stop':
                temp_user_feature_storage.append(feature_entry)
            else:
                continue

        spells_spellbook = pandas.DataFrame(temp_user_spell_storage, columns=['Spells'])
        feature_spellbook = pandas.DataFrame(temp_user_feature_storage, columns=['Talents'])
        user_class_spellbook = pandas.DataFrame(user_class, columns=['Class'])

        spellbook_a = user_class_spellbook.join(spells_spellbook, how='right')
        spellbook_b = spells_spellbook.join(feature_spellbook)
        spellbook_create = pandas.merge(spellbook_a, spellbook_b, on='Spells')

        print('Writing input to .csv')
        spellbook_create.to_csv('src/Spellbook.csv', index=False)

    ### Uncomment when done testing ###
    Tk().withdraw()
    full_path_to_spellbook = askopenfilename()
    ### Comment when done testing ###
    print("Loading csv from disk")
    # path_to_directory = os.getcwd()
    # full_path_to_spellbook = path_to_directory + '/src/Spellbook.csv'
    return full_path_to_spellbook


def make_connections(path):
    spellbook_raw = pandas.read_csv(path, delimiter=',')
    path_to_directory = os.getcwd()
    # /' + player_class + '
    features_to_get = spellbook_raw['Talents']  # creates a df of the spell and feature names from user input
    spells_to_get = spellbook_raw['Spells']
    class_to_get = spellbook_raw['Class']

    spells_to_get = spells_to_get.fillna(' ')  # replaces null values
    features_to_get = features_to_get.fillna(' ')

    spells_to_get = [entry for entry in spells_to_get if str(entry) != 'nan']  # checks to see if there are any
    features_to_get = [entry for entry in features_to_get if str(entry) != 'nan']  # null rows and removes them

    clean_spells_to_get = [entry.replace(' ', '_') for entry in spells_to_get]  # replaces the spaces in the input
    clean_features_to_get = [entry.replace(' ', '_') for entry in features_to_get]  # with '_' for filename association

    spellbook = [path_to_directory + '/src/Mystic_Disciplines/' + x + ".csv" for x in
                 clean_spells_to_get]  # sets the path of the spell entry for each spell
    featurebook = [path_to_directory + '/src/Mystic_Talents/' + x + ".csv" for x in
                   clean_features_to_get]  # sets the path of the spell entry for each spell

    glued_spellbook = pandas.DataFrame()  # set up an empty array to put the spell info in here so that we don't keep
    glued_featurebook = pandas.DataFrame()  # same idea as glued_spellbook
    # adding new entries to the same book
    for i, filename in enumerate(spellbook):  # puts the individual .csvs into one df
        spell_entry = spellbook[i]
        for file in glob.glob(spell_entry):
            page = pandas.read_csv(file, delimiter=',', header=0, names=['Name', 'Focus', 'Form', 'Description',
                                                                         'Psi_Point_Cost', 'Cast_Type',
                                                                         'Duration'])  # we call each file a page here for flavor
            glued_spellbook = pandas.concat([glued_spellbook, page], sort=False)

    for i, filename in enumerate(featurebook):  # puts the individual .csvs into one df
        feature_entry = featurebook[i]
        for file in glob.glob(feature_entry):
            page = pandas.read_csv(file, delimiter=',', header=0,
                                   names=['Name', 'Description'])  # we call each file a page here for flavor
            glued_featurebook = pandas.concat([glued_featurebook, page], sort=False)

    new_index = []  # sets unique indexes for the new df
    for i in range(len(glued_spellbook.index)):
        new_index.append(i)
    glued_spellbook = glued_spellbook.set_index([pandas.Index(new_index)])
    new_index = []  # these are here to make sure the index gets reset after applying to the df
    for i in range(len(glued_featurebook.index)):
        new_index.append(i)
    glued_featurebook = glued_featurebook.set_index([pandas.Index(new_index)])

    glued_spellbook = glued_spellbook.fillna(' ')  # replaces null values
    glued_featurebook = glued_featurebook.fillna(' ')

    return glued_spellbook, glued_featurebook


def get_names(spellbook_to_get, featurebook_to_get):  # returns a list of the names of your chosen spells / features
    spellbook_to_get = spellbook_to_get['Name']
    featurebook_to_get = featurebook_to_get['Name']

    spellnames = spellbook_to_get.replace(' ', np.NaN).dropna(how='all')
    featurenames = featurebook_to_get.replace(' ', np.NaN).dropna(how='all')
    return spellnames, featurenames


def get_spell_description(spellbook_to_use):  # returns the description for your chosen spell
    name_user_input = input('Enter spell name i.e. ("Magic Missile"): ')
    form_user_input = input('Enter form name (i.e. "Iron Hide") enter "ls" to display all: ')
    while form_user_input == 'ls':
        forms_for_spell_temp = spellbook_to_use[spellbook_to_use['Name'] == name_user_input]
        forms_for_spell = forms_for_spell_temp['Form']
        print("Here are the forms for {0}: \n".format(name_user_input) + forms_for_spell.to_string(header=False, index=False))
        form_user_input = input('Enter form name: ')
    temp_spell_storage = spellbook_to_use[['Name', 'Form', 'Description']]
    temp_spell_storage = temp_spell_storage[temp_spell_storage['Name'] == name_user_input]
    temp_spell_storage = temp_spell_storage[temp_spell_storage['Form'] == form_user_input]
    temp_spell_storage = temp_spell_storage.drop(columns=['Name', 'Form'])
    spell_description = temp_spell_storage.to_string(header=False, index=False)
    return spell_description, name_user_input, form_user_input


def get_feature_description(featurebook_to_use):
    name_user_input = input('Enter feature name i.e. "Blind Spot": ')
    temp_feature_storage = featurebook_to_use[['Name', 'Description']]
    temp_feature_storage = temp_feature_storage[temp_feature_storage['Name'] == name_user_input]
    temp_feature_storage = temp_feature_storage.drop(columns='Name')
    feature_description = temp_feature_storage.to_string(header=False, index=False)
    return feature_description, name_user_input


path_to_spellbook = get_spellbook()

spellbook, featurebook = make_connections(path_to_spellbook)

spell_list, feature_list = get_names(spellbook, featurebook)

spell_description, spell_name, form_name = get_spell_description(spellbook)

feature_description, feature_name = get_feature_description(featurebook)

print('Spell Name: {0} \nDescription: {1}'.format(spell_name, spell_description))
print('Feature Name: {0} \nDescription: {1}'.format(feature_name, feature_description))