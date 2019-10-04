import pandas as pd

#group age slices
FIRST_GROUP = [0.0, 1.0, 2.0]
SECOND_GROUP = [3.0, 4.0, 5.0]
THIRD_GROUP = [6.0, 7.0, 8.0, 9.0, 10.0]
FOURTH_GROUP = [11.0, 12.0, 13.0, 14.0, 15.0]
SIXTH_GROUP = [16.0]

#group sets
YEARS_SLICE = {'FIRST_GROUP' : FIRST_GROUP,
               'SECOND_GROUP': SECOND_GROUP,
               'THIRD_GROUP' : THIRD_GROUP,
               'FOURTH_GROUP': FOURTH_GROUP,
               'SIXTH_GROUP' : SIXTH_GROUP}

#exist data file
INPUT_DATA_PATH = '../common/data.csv'
input_file = pd.read_csv(INPUT_DATA_PATH)

#Company Specifier -> Company YrsExperience c [0-2, 3-5, 6-10, 11-15, 16+]
#Company -> Company YrsCompany
#Company YrsExperience = min -> max Company YrsExperience : YrsCompany = [0-2] && [3-5] && [6-10] && [11-15] && [16+]

def is_year_in_years_slice(min_company_age):
    #by default return 1 st group if None age bound/...
    actual_group = 'FIRST_GROUP'
    for group_data in YEARS_SLICE.items():
        #print('current year = ', group_data, ' for group: ', group_data[0], min_company_age)
        if min_company_age in group_data[1]:
            #print('In bounds, minimum age for group: ', group_data[0])
            actual_group = group_data[0]
    return actual_group

def pdf(_input_file):
    return pd.DataFrame(_input_file)

def column_index(file, _column):
    df = pd.DataFrame(file)
    return df.columns.get_loc(_column)

def column_data_by_index(file, _index):
    df = pd.DataFrame(file)
    return df.iloc[:, _index]

#get actual company info from data
company_name = column_data_by_index(input_file, column_index(input_file, 'Company'))
company_years = column_data_by_index(input_file, column_index(input_file, 'YrsCompany'))
company_experience = column_data_by_index(input_file, column_index(input_file, 'YrsExperience')) #as profile marker

company_profile = {}
company_profile['Company'] = company_name
company_profile['YrsCompany'] = company_years
company_profile['YrsExperience'] = company_experience

#print(pdf(input_file).loc[pdf(input_file)['YrsCompany'] == company_profile['YrsExperience']][0:10])

#YrsCompany, Company are the same length - data with equal row numbers for each column
print("Unfiltered companies & ages length: ", len(company_profile['YrsExperience']))

#filter by unique rows
company_profile_filtered = list()
for company_info in zip(company_profile['Company'], company_profile['YrsExperience']):
    company_profile_filtered.append(company_info)
company_profile_filtered = list(set(company_profile_filtered))

print("Filtered companies & ages length: ", len(company_profile_filtered))

company_ages_by_names_raw = {}
#make list of tuples with [(Company, Age1, Age2, ..., AgeN)]
for c_name, c_age in company_profile_filtered:
    company_ages_by_names_raw.setdefault(c_name, [c_name]).append(c_age)
company_ages_by_names = list(map(tuple, company_ages_by_names_raw.values()))

print("Filtered companies by ages length: ", len(company_ages_by_names))

#find minimum company age and search if that value in group ages slice
for company_info in company_ages_by_names:
    print('company name', company_info[0], 'ages: ', company_info[1:-1])
    min_company_age = 0.0

    try:
        min_company_age = min(company_info[1:-1])
    except ValueError:
        print('Company have not age bounds, suppose that necessary experience is 0 years')

    print('minimum age: ', min_company_age)
    print('ages slice: ', is_year_in_years_slice(min_company_age))


#for each company value find minimum, if minimum c YEARS_SLICE
#save this company with key of YEARS_SLICE dict