import pandas as pd

#group age slices
FIRST_GROUP = [0, 2]
SECOND_GROUP = [3, 5]
THIRD_GROUP = [6, 10]
FOURTH_GROUP = [11, 15]
SIXTH_GROUP = [16]

#group sets
YEARS_SLICE = {'FIRST_GROUP' : FIRST_GROUP,
               'SECOND_GROUP': SECOND_GROUP,
               'THIRD_GROUP' : THIRD_GROUP,
               'FOURTH_GROUP': FOURTH_GROUP,
               'SIXTH_GROUP' : SIXTH_GROUP}

#exist data file
INPUT_DATA_PATH = '../common/data.csv'
input_file = pd.read_csv(INPUT_DATA_PATH)

#people Specifier -> people YrsExperience c [0-2, 3-5, 6-10, 11-15, 16+]
#Company -> Company YrsCompany
#people YrsExperience = min -> max Company YrsCompany : YrsCompany = [0-2] && [3-5] && [6-10] && [11-15] && [16+]

def is_year_in_years_slice(year):
    for current_year in YEARS_SLICE.items():
        print('current year = ', current_year, year)



def pdf(_input_file):
    return pd.DataFrame(_input_file)

def column_index(file, _column):
    df = pd.DataFrame(file)
    return df.columns.get_loc(_column)

def column_data_by_index(file, _index):
    df = pd.DataFrame(file)
    return df.iloc[:, _index]

people_profile = {}
company_profile = {}

specifier_data = column_data_by_index(input_file, column_index(input_file, 'Specifier'))
experience_years_data = column_data_by_index(input_file, column_index(input_file, 'YrsExperience'))

#not necessary - see task
people_profile['Specifier'] = specifier_data
people_profile['YrsExperience'] = experience_years_data

company_name = column_data_by_index(input_file, column_index(input_file, 'Company'))
company_years = column_data_by_index(input_file, column_index(input_file, 'YrsCompany'))
company_experience = column_data_by_index(input_file, column_index(input_file, 'YrsExperience')) #as profile marker

company_profile['Company'] = company_name
company_profile['YrsCompany'] = company_years
company_profile['YrsExperience'] = company_experience

#print(pdf(input_file).loc[pdf(input_file)['YrsCompany'] == company_profile['YrsExperience']][0:10])

#YrsCompany, Company are the same length - data with equal row numbers for each column
print("Unfiltered companies & ages length: ", len(company_profile['YrsCompany']))

#filter by unique rows
company_profile_filtered = list()
for company_info in zip(company_profile['Company'], company_profile['YrsCompany']):
    company_profile_filtered.append(company_info)

company_profile_filtered = list(set(company_profile_filtered))

print("Filtered companies & ages length: ", len(company_profile_filtered))

for company_info in company_profile_filtered:
    print(company_info)

