import pandas as pd

INPUT_DATA_PATH = '../common/data.csv'

YEARS_SLICE = [2, 5, 10, 15]
input_file = pd.read_csv(INPUT_DATA_PATH)

#people Specifier -> people YrsExperience c [0-2, 3-5, 6-10, 11-15, 16+]
#Company -> Company YrsCompany
#people YrsExperience = min -> max Company YrsCompany : YrsCompany = [0-2] && [3-5] && [6-10] && [11-15] && [16+]

def pdf(_input_file):
    return pd.DataFrame(_input_file)

def get_column_index(file, _column):
    df = pd.DataFrame(file)
    return df.columns.get_loc(_column)

def get_column_data_by_index(file, _index):
    df = pd.DataFrame(file)
    return df.iloc[:, _index]

people_profile = {}
company_profile = {}

specifier_data = get_column_data_by_index(input_file, get_column_index(input_file, 'Specifier'))
experience_years_data = get_column_data_by_index(input_file, get_column_index(input_file, 'YrsExperience'))

people_profile['Specifier'] = specifier_data
people_profile['YrsExperience'] = experience_years_data

company_name = get_column_data_by_index(input_file, get_column_index(input_file, 'Company'))
company_years = get_column_data_by_index(input_file, get_column_index(input_file, 'YrsCompany'))

company_profile['Company'] = company_name
company_profile['YrsCompany'] = company_years

#for profile age make dict with profile age and YEARS_SLICE index or all
#for profile age slice (YEARS_SLICE subset) find company with YrsCompany c YEARS_SLICE
print(pdf(input_file).loc[pdf(input_file)['YrsCompany'] == people_profile['YrsExperience']])
