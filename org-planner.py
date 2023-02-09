import csv
import json
import math
import sys
import time
from PySide6 import QtWidgets
from SunburstOrgWidget import fx_rates
from MainWindow import MainWindow
from GenderSunburstOrgWidget import gender_colours
from GradeSunburstOrgWidget import grade_colours
from LocationSunburstOrgWidget import location_colours
from NumDirectReportsSunburstOrgWidget import num_direct_reports_colours
from NineBoxInfoWidget import nine_box_colours
from RatingSunburstOrgWidget import rating_colours
from SalaryBandOffsetSunburstOrgWidget import salary_band_offset_colours
from SalaryOffsetSunburstOrgWidget import salary_offset_colours
from SalarySunburstOrgWidget import salary_colours
from TeamSunburstOrgWidget import team_colours
from EmploymentSunburstOrgWidget import employment_colours

team_colours_list = [
    [0xff, 0xc0, 0xc0],
    [0xc0, 0xff, 0xc0],
    [0xc0, 0xc0, 0xff],
    [0xff, 0xff, 0xc0],
    [0xc0, 0xff, 0xff],
    [0xff, 0xc0, 0xff],
    [0xc0, 0x80, 0x80],
    [0x80, 0xc0, 0x80],
    [0x80, 0x80, 0xc0],
    [0xc0, 0xc0, 0x80],
    [0x80, 0xc0, 0xc0],
    [0xc0, 0x80, 0xc0],
    [0x80, 0x40, 0x40],
    [0x40, 0x80, 0x40],
    [0x40, 0x40, 0x80],
    [0x80, 0x80, 0x40],
    [0x40, 0x80, 0x80],
    [0x80, 0x40, 0x80],
    [0x40, 0x00, 0x00],
    [0x00, 0x40, 0x00],
    [0x00, 0x00, 0x40],
    [0x40, 0x40, 0x00],
    [0x00, 0x40, 0x40],
    [0x40, 0x00, 0x40],
    [0xff, 0x80, 0x80],
    [0x80, 0xff, 0x80],
    [0x80, 0x80, 0xff],
    [0xff, 0xff, 0x80],
    [0x80, 0xff, 0xff],
    [0xff, 0x80, 0xff],
    [0xff, 0x40, 0x40],
    [0x40, 0xff, 0x40],
    [0x40, 0x40, 0xff],
    [0xff, 0xff, 0x40],
    [0x40, 0xff, 0xff],
    [0xff, 0x40, 0xff],
    [0x00, 0x00, 0x00]
]

employment_colours_list = [
    [0x60, 0xc0, 0x60],
    [0xc0, 0x60, 0x60],
    [0x60, 0x60, 0xc0],
    [0x60, 0xc0, 0xc0],
    [0xc0, 0xc0, 0x60],
    [0xc0, 0x60, 0xc0],
    [0xc0, 0xc0, 0xc0],
    [0x00, 0x00, 0x00]
]

office_locations = [
    ("london", "UK"),
    ("dublin", "Ireland"),
    ("singapore", "Singapore"),
    ("mumbai", "India"),
    ("new york", "USA"),
    ("san francisco", "USA"),
    ("ohio", "USA"),
    ("home - ma", "USA"),
    ("home - fl", "USA"),
    ("home - il", "USA"),
    ("sofia", "Bulgaria"),
    ("sao paolo", "Brazil"),
    ("hong kong", "Hong Kong")
]

def scan_teams_and_employments(people):
    teams = []
    employments = []

    for i in people:
        team = people[i]["Person"]["Teams"][-1]["Team"]
        if team not in teams:
            teams.append(team)

        employment_type = people[i]["Person"]["Employments"][-1]["Employment"]
        if employment_type not in employments:
            employments.append(employment_type)

    return (teams, employments)

def scan_org_tree(people, locations, supervisor_uen, depth):
    # Scan each direct report recursively, computing how deep each person is in
    # the overall org, and how many reports roll up to them in total.
    p = people[supervisor_uen]
    p["Num Direct Reports"] = len(p["Direct Reports"])
    p["Num Direct Reports Counts"] = [0] * len(num_direct_reports_colours)
    p["Location Counts"] = [0] * len(location_colours)
    p["Team Counts"] = [0] * len(team_colours)
    p["Employment Counts"] = [0] * len(employment_colours)
    p["Grade Counts"] = [0] * len(grade_colours)
    p["Gender Counts"] = [0] * len(gender_colours)
    p["9 Box Counts"] = [[] for i in range(3)]
    for i in range(3):
        p["9 Box Counts"][i] = [0] * 3

    p["Rating Counts"] = [0] * len(rating_colours)
    p["Total Reports"] = 0
    p["Salary Counts"] = [0] * len(salary_colours)
    p["Salary Offset Counts"] = [0] * len(salary_offset_colours)
    p["Salary Band Offset Counts"] = [0] * len(salary_band_offset_colours)
    p["Rollup Salaries"] = 0
    p["Missing Salaries"] = 0

    for i in p["Direct Reports"]:
        scan_org_tree(people, locations, i, depth + 1)
        dr = people[i]

        for j in range(len(p["Num Direct Reports Counts"])):
            p["Num Direct Reports Counts"][j] += dr["Num Direct Reports Counts"][j]

        for j in range(len(p["Team Counts"])):
            p["Team Counts"][j] += dr["Team Counts"][j]

        for j in range(len(p["Employment Counts"])):
            p["Employment Counts"][j] += dr["Employment Counts"][j]

        for j in range(len(p["Location Counts"])):
            p["Location Counts"][j] += dr["Location Counts"][j]

        for j in range(len(p["Grade Counts"])):
            p["Grade Counts"][j] += dr["Grade Counts"][j]

        for j in range(len(p["Gender Counts"])):
            p["Gender Counts"][j] += dr["Gender Counts"][j]

        for j in range(len(p["9 Box Counts"])):
            for k in range(len(p["9 Box Counts"][j])):
                p["9 Box Counts"][j][k] += dr["9 Box Counts"][j][k]

        for j in range(len(p["Salary Counts"])):
            p["Salary Counts"][j] += dr["Salary Counts"][j]

        for j in range(len(p["Salary Offset Counts"])):
            p["Salary Offset Counts"][j] += dr["Salary Offset Counts"][j]

        for j in range(len(p["Salary Band Offset Counts"])):
            p["Salary Band Offset Counts"][j] += dr["Salary Band Offset Counts"][j]

        for j in range(len(p["Rating Counts"])):
            p["Rating Counts"][j] += dr["Rating Counts"][j]

        p["Total Reports"] += (dr["Total Reports"] + 1)
        p["Rollup Salaries"] += dr["Rollup Salaries"]
        p["Missing Salaries"] += dr["Missing Salaries"]

    num_direct_reports = str(p["Num Direct Reports"])
    p["Num Direct Reports Counts"][list(num_direct_reports_colours).index(num_direct_reports)] += 1

    team = p["Person"]["Teams"][-1]["Team"]
    p["Team Counts"][list(team_colours).index(team)] += 1

    employment_type = "Unknown"
    if "Employment" in p["Person"]["Employments"][-1]:
        employment_type = p["Person"]["Employments"][-1]["Employment"]
        p["Employment Counts"][list(employment_colours).index(employment_type)] += 1

    if "Locations" in p["Person"].keys():
        location = p["Person"]["Locations"][-1]["Location"]
        p["Location Counts"][list(location_colours).index(location)] += 1

    grade = ""
    if "Grades" in p["Person"].keys():
        grade = p["Person"]["Grades"][-1]["Grade"]
        p["Grade Counts"][list(grade_colours).index(grade)] += 1

    if "Gender" in p["Person"].keys():
        gender = p["Person"]["Gender"]
        p["Gender Counts"][list(gender_colours).index(gender)] += 1

    if "9 Box" in p["Person"].keys():
        nine_box_potential = p["Person"]["9 Box"][-1]["Potential"]
        nine_box_potential_index = list(nine_box_colours).index(nine_box_potential)
        nine_box_performance = p["Person"]["9 Box"][-1]["Performance"]
        nine_box_performance_index = list(
            nine_box_colours[nine_box_potential]
        ).index(nine_box_performance)
        p["9 Box Counts"][nine_box_potential_index][nine_box_performance_index] += 1

    if "Ratings" in p["Person"].keys():
        rating = str(p["Person"]["Ratings"][-1]["Rating"])
        p["Rating Counts"][list(rating_colours).index(rating)] += 1

    p["Org Depth"] = depth

    # Scan each direct report, but this time compute the fraction of the overall
    # team their subteam represents.
    drs = p["Direct Reports"]
    num_reports = p["Total Reports"]
    for i in drs:
        people[i]["Supervisor Fraction"] = (people[i]["Total Reports"] + 1) / num_reports

    # Sort the direct reports to put the one with the largest fraction of the
    # org first.
    for i in range(len(drs)):
        for j in range(len(drs) - i - 1):
            if people[drs[j]]["Supervisor Fraction"] < people[drs[j + 1]]["Supervisor Fraction"]:
                t = drs[j + 1]
                drs[j + 1] = drs[j]
                drs[j] = t

    # Then sort any direct reports from the same team to cluster them.  While
    # this slightly undoes the sort it's a more natural view over the org,
    # placing people who do the same sorts of things in one grouping.
    for i in range(1, len(drs)):
        if (people[drs[i - 1]]["Person"]["Teams"][-1]["Team"]
                == people[drs[i]]["Person"]["Teams"][-1]["Team"]):
            continue

        for j in range(i + 1, len(drs)):
            if (people[drs[i - 1]]["Person"]["Teams"][-1]["Team"]
                    == people[drs[j]]["Person"]["Teams"][-1]["Team"]):
                for k in range(j, i, -1):
                    t = drs[k - 1]
                    drs[k - 1] = drs[k]
                    drs[k] = t

    start_date = p["Person"]["Employments"][-1]["Start Date"]
    t = time.strptime(start_date, "%Y-%m-%d")
    ot = time.strptime("2014-10-31", "%Y-%m-%d")
    cur_time = time.time()
    org_elapsed_time = cur_time - time.mktime(ot)
    worked_time = cur_time - time.mktime(t)
    p["Service Duration"] = cur_time - time.mktime(t)
    p["Service Duration Fraction"] = worked_time / org_elapsed_time

    salary = 0
    if "Salaries" not in p["Person"].keys():
        p["Missing Salaries"] += 1
    else:
        salary = p["Person"]["Salaries"][-1]["Salary"]
        salary_usd = salary * fx_rates[location]
        p["Rollup Salaries"] += salary_usd

        if salary_usd >= 10000:
            log_salary_usd = int((math.log10(salary_usd) - 4) / 0.25)
            p["Salary Counts"][log_salary_usd] += 1

    if (("Grades" in p["Person"].keys()) and
            ("Salaries" in p["Person"].keys()) and
            ("Locations" in p["Person"].keys())):
        fx_rate = fx_rates[location]
        fte = 1
        if "Percentage Time" in p["Person"]["Employments"][-1].keys():
            fte = p["Person"]["Employments"][-1]["Percentage Time"] / 100

        corp_grade = p["Person"]["Grades"][-1]["Grade"][:1]
        location = p["Person"]["Locations"][-1]["Location"]
        band_lower_limit = int(locations[location][corp_grade]["Low"] * fte)
        p["Salary Band Lower Limit"] = band_lower_limit
        p["Salary Band Lower Limit USD"] = int(band_lower_limit * fx_rate)
        band_upper_limit = int(locations[location][corp_grade]["High"] * fte)
        p["Salary Band Upper Limit"] = band_upper_limit
        p["Salary Band Upper Limit USD"] = int(band_upper_limit * fx_rate)
        band_mid_salary = (band_upper_limit + band_lower_limit) // 2
        p["Salary Band Mid Point"] = band_mid_salary
        p["Salary Band Mid Point USD"] = int(band_mid_salary * fx_rate)

        salary_offset = salary - band_mid_salary
        p["Salary Offset"] = salary_offset
        salary_offset_usd = salary_offset * fx_rate
        p["Salary Offset USD"] = salary_offset_usd
        salary_offset_percentage = (salary_offset / band_mid_salary) * 100
        p["Salary Offset Percentage"] = salary_offset_percentage

        salary_offset_usd_key = salary_offset_usd
        salary_offset_key = int(salary_offset_usd_key + 5000) // 10000
        if salary_offset_key > 5:
            salary_offset_key = 5
        elif salary_offset_key < -5:
            salary_offset_key = -5

        p["Salary Offset Key"] = str(salary_offset_key)
        p["Salary Offset Counts"][5 + salary_offset_key] += 1

        band_offset = 0
        band_offset_usd = 0
        band_offset_key = 0
        if salary < band_lower_limit:
            band_offset = salary - band_lower_limit
            band_offset_usd = int(band_offset * fx_rate)
            band_offset_key = (band_offset_usd - 9999) // 10000
            if band_offset_key < -5:
                band_offset_key = -5
        elif salary > band_upper_limit:
            band_offset = salary - band_upper_limit
            band_offset_usd = int(band_offset * fx_rate)
            band_offset_key = (band_offset_usd + 9999) // 10000
            if band_offset_key > 5:
                band_offset_key = 5

        p["Salary Band Offset"] = band_offset
        p["Salary Band Offset USD"] = band_offset_usd
        p["Salary Band Offset Key"] = str(band_offset_key)
        p["Salary Band Offset Counts"][5 + band_offset_key] += 1

def scan_json_locations(all_locations_list):
    locations = {}

    for i in all_locations_list:
        grade = {}
        for j in i["Bands"]:
            band = {}
            band["Low"] = j["Low"]
            band["High"] = j["High"]
            grade[j["Grade"]] = band

        locations[i["Location"]] = grade

    return locations

def scan_json_people(all_people_list):
    people = {}
    top_level = 0
    failed = False

    for i in all_people_list:
        uen = i["UEN"]
        people[uen] = {}
        people[uen]["Person"] = i
        people[uen]["Direct Reports"] = []

    for i in all_people_list:
        uen = i["UEN"]
        if "Supervisors" not in i.keys():
            if top_level == 0:
                top_level = uen
            else:
                print(i["Name"], "does not have a supervisor, but",
                        top_level, "is already set as top-level")
                failed = True
        else:
            supervisor_uen = i["Supervisors"][-1]["Supervisor UEN"]
            people[supervisor_uen]["Direct Reports"].append(uen)

    return (failed, people, top_level)

def create_employments_json(employment, start_date):
    inner = {}
    inner["Employment"] = employment
    inner["Start Date"] = start_date
    outer = []
    outer.append(inner)
    return outer

def create_locations_json(location):
    inner = {}
    inner["Location"] = location
    outer = []
    outer.append(inner)
    return outer

def create_supervisors_json(supervisor):
    inner = {}
    inner["Supervisor UEN"] = supervisor
    outer = []
    outer.append(inner)
    return outer

def create_teams_json(team):
    inner = {}
    inner["Team"] = team
    outer = []
    outer.append(inner)
    return outer

def merge_csv(csv_file, people_list):
    # Given a CSV file, extracted from Namely, look up important data and
    # fake out JSON entries to match.  Then insert the JSON entries into
    # our people_list.
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        found = False
        for i in people_list:
            uen = i["UEN"]
            if row["Employee Id"].strip() == str(uen):
                found = True

                if "Supervisors" not in i.keys():
                    i["Supervisors"] = create_supervisors_json(int(row["Reports To"]))
                break

        if not found:
            new_json = {}
            emp_id = row["Employee Id"].strip()
            if emp_id[:1] == "7":
                new_json["UEN"] = int(emp_id)
                new_json["Name"] = " ".join(row["Full Name"].split())
                rep_to = row["Reports To"].strip()
                if rep_to[:1] == "7":
                    new_json["Supervisors"] = create_supervisors_json(int(rep_to))
                else:
                    print("UEN", int(emp_id), "no super", rep_to)

                team = "R3"
                if row["Division"] != "":
                    team = row["Division"]

                new_json["Teams"] = create_teams_json(team)

                start_date = row["Start Date"]
                new_json["Employments"] = create_employments_json("Unknown", start_date)

                office = row["Office"].lower()
                location = "Other"
                for o in office_locations:
                    (search_key, country) = o
                    if office.find(search_key) != -1:
                        location = country
                        break

                if location == "Other":
                    city = row["City"].lower()
                    for o in office_locations:
                        (search_key, country) = o
                        if city.find(search_key) != -1:
                            location = country
                            break

                new_json["Locations"] = create_locations_json(location)

                people_list.append(new_json)

def main():
    if len(sys.argv) < 2:
        print("Usage: org-planner <JSON file> <optional-CSV file>")
        return

    json_file_path = sys.argv[1]
    with open(json_file_path, encoding = 'utf-8') as json_file:
        json_data = json.load(json_file)

    all_locations_list = json_data["Locations"]
    all_locations = scan_json_locations(all_locations_list)

    all_people_list = json_data["People"]

    if len(sys.argv) == 3:
        csv_file_path = sys.argv[2]
        with open(csv_file_path, encoding = 'utf-8') as csv_file:
            merge_csv(csv_file, all_people_list)

    fail, all_people, supervisor_uen = scan_json_people(all_people_list)
    if fail:
        exit()

    all_teams, all_employments = scan_teams_and_employments(all_people)
    all_teams.sort()

    ci = 0
    for i in all_teams:
        team_colours[i] = team_colours_list[ci]
        ci += 1

    ci = 0
    for i in all_employments:
        employment_colours[i] = employment_colours_list[ci]
        ci += 1

    scan_org_tree(all_people, all_locations, supervisor_uen, 0)
    all_people[supervisor_uen]["Supervisor Fraction"] = 1

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(1536, 900)
    window.set_locations(all_locations)
    window.set_people(all_people, supervisor_uen)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
