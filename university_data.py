import re
import pandas as pd


def __main__():
    with open('university.data', 'r') as file:
        raw_data = file.readlines()

    universities = []
    current_uni = {}
    seen_universities = []
    uni_name = ''

    for line in raw_data:
        line = line.strip().lower()

        if 'duplicate' in line:
            continue

        elif line.startswith('(def-instance'):
            
            new_uni_name = re.search(r'\(def-instance ([^\s]+)', line).group(1)
            new_uni_name = re.sub(r'\d+$', '', new_uni_name)

            if new_uni_name in seen_universities:
                continue

            if current_uni:
                universities.append(current_uni)

            current_uni = {}
            uni_name = new_uni_name
            current_uni['name'] = uni_name
            seen_universities.append(uni_name)
            
        else:
            matches = re.findall(r'\(([^)]+)\)', line)
            for match in matches:
                parts = match.split()

                key = parts[0].lower()
                value = parts[1:]
                
                if key == 'academic-emphasis' or key == 'control':
                    
                    for subject in value:
                        if key == 'control':
                            current_uni[f"control-{subject}"] = 1
                        else:    
                            current_uni[f"academic-emphasis-{subject}"] = 1
                    
                else:    
                    value = ' '.join(value)
                    current_uni[key] = value
                    

    universities = pd.DataFrame(universities)

    universities

    universities.dropna(subset=['male:female'], inplace=True)
    universities.dropna(subset=['student:faculty'], inplace=True)
    universities.dropna(subset=['sat-verbal'], inplace=True)
    universities.dropna(subset=['sat-math'], inplace=True)

    universities = universities[universities['location'] != '0']
    universities = universities[universities['male:female'] != '0']
    universities = universities[universities['student:faculty'] != '0']
    universities = universities[universities['student:faculty'] != '0']
    universities = universities[universities['student:faculty'] != 'ratio:?']
    universities = universities[universities['student:faculty'] != 'ratio:unavailable']
    universities = universities[universities['sat-verbal'] != '0']
    universities = universities[universities['sat-math'] != '0']
    universities = universities[universities['sat-math'] != 'na']
    universities = universities[universities['percent-financial-aid'] != '0']
    universities = universities[universities['no-applicants'] != '0']

    universities = universities.fillna(0)

    universities['sat-verbal'] = universities['sat-verbal'].astype(float)
    universities['sat-math'] = universities['sat-math'].astype(float)
    universities['percent-financial-aid'] = universities['percent-financial-aid'].astype(float)
    universities['percent-admittance'] = universities['percent-admittance'].astype(float)
    universities['percent-enrolled'] = universities['percent-enrolled'].astype(float)
    universities['academics-scale:1-5'] = universities['academics-scale:1-5'].astype(float)
    universities['social-scale:1-5'] = universities['social-scale:1-5'].astype(float)
    universities['quality-of-life-scale:1-5'] = universities['quality-of-life-scale:1-5'].astype(float)

    # location ranges:
    #    urban: 1
    #    suburban: 2
    #    small-city: 3
    #    small-town: 4
    location_map = {
        'urban': 1,
        'suburban': 2,
        'small-city': 3,
        'small-town': 4,
    }

    universities['location'] = universities['location'].map(location_map).fillna(0).astype(float)

    # applicants ranges:
    #    0 - 5 thousand: 1,
    #    5 - 10 thousand': 2,
    #    10 - 15 thousand: 3,
    #    15 - 20 thousand: 4,
    #    20+ thousand: 5,
    students_map = {
        'thous:5-': 1,
        'thous:5-10': 2,
        'thous:10-15': 3,
        'thous:15-20': 4,
        'thous:20+': 5,
    }
    universities['no-of-students'] = universities['no-of-students'].map(students_map).fillna(0).astype(float)

    # expenses ranges:
    #    0 - 4 thousand: 1
    #    4 - 7 thousand: 2
    #    7 to 10 thousand: 3
    #    10+ thousand: 4
    expenses_map = {
        'thous$:4-': 1,
        'thous$:4-7': 2,
        'thous$:7-10': 3,
        'thous$:10+': 4,
    }
    universities['expenses'] = universities['expenses'].map(expenses_map).fillna(0).astype(float)

    # applicants ranges:
    #    0 - 4 thousand: 1,
    #    4 - 7 thousand': 1,
    #    7 - 10 thousand: 2,
    #    10 - 13 thousand: 2,
    #    13 - 17 thousand: 3,
    #    17+ thousand: 3,
    applicants_map = {
        'thous:4-': 1,
        'thous:4-7': 1,
        'thous:7-10': 2,
        'thous:10-13': 2,
        'thous:13-17': 3,
        'thous:17+': 3,
    }
    universities['no-applicants'] = universities['no-applicants'].map(applicants_map).fillna(0).astype(float)


    all_columns = universities.columns.tolist()
    academic_cols = [col for col in all_columns if col.startswith('academic-emphasis')]
    control_cols = [col for col in all_columns if col.startswith('control')]
    other_cols = [col for col in all_columns if (not col.startswith('academic-emphasis') and not col.startswith('control'))]
    new_order = other_cols + control_cols + academic_cols
    universities = universities[new_order]
