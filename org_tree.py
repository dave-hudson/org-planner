import json
import math
import sys
import time
from PySide6 import QtWidgets
from MainWindow import MainWindow, fx_rates, team_colours, type_colours, num_direct_reports_colours, location_colours, grade_colours, gender_colours, salary_colours, rating_colours, nine_box_colours, salary_offset_colours

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
    [0xff, 0xff, 0xff],
    [0xc0, 0xc0, 0xc0],
    [0x80, 0x80, 0x80],
    [0x40, 0x40, 0x40],
    [0x00, 0x00, 0x00]
]

type_colours_list = [
    [0x60, 0xc0, 0x60],
    [0xc0, 0x60, 0x60],
    [0x60, 0x60, 0xc0],
    [0x60, 0xc0, 0xc0],
    [0xc0, 0xc0, 0x60],
    [0xc0, 0x60, 0xc0],
    [0xc0, 0xc0, 0xc0],
    [0x00, 0x00, 0x00]
]

def scan_teams_and_types(people):
    teams = []
    types = []

    for i in people:
        team = people[i]["Person"]["Team"]
        if team not in teams:
            teams.append(team)

        type = people[i]["Person"]["Type"]
        if type not in types:
            types.append(type)

    return (teams, types)

def scan_org_tree(people, locations, supervisor_uen, depth):
    # Scan each direct report recursively, computing how deep each person is in
    # the overall org, and how many reports roll up to them in total.
    p = people[supervisor_uen]
    p["Num Direct Reports"] = len(p["Direct Reports"])
    p["Num Direct Reports Counts"] = [0] * len(num_direct_reports_colours)
    p["Location Counts"] = [0] * len(location_colours)
    p["Team Counts"] = [0] * len(team_colours)
    p["Type Counts"] = [0] * len(type_colours)
    p["Grade Counts"] = [0] * len(grade_colours)
    p["Gender Counts"] = [0] * len(gender_colours)
    p["9 Box Counts"] = [[] for i in range(3)]
    for i in range(3):
        p["9 Box Counts"][i] = [0] * 3
    p["Rating Counts"] = [0] * len(rating_colours)
    p["Total Reports"] = 0
    p["Salary Counts"] = [0] * len(salary_colours)
    p["Salary Offset Counts"] = [0] * len(salary_offset_colours)
    p["Rollup Salaries"] = 0
    p["Missing Salaries"] = 0

    for i in p["Direct Reports"]:
        scan_org_tree(people, locations, i, depth + 1)
        dr = people[i]

        for j in range(len(p["Num Direct Reports Counts"])):
            p["Num Direct Reports Counts"][j] += dr["Num Direct Reports Counts"][j]

        for j in range(len(p["Team Counts"])):
            p["Team Counts"][j] += dr["Team Counts"][j]

        for j in range(len(p["Type Counts"])):
            p["Type Counts"][j] += dr["Type Counts"][j]

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

        for j in range(len(p["Rating Counts"])):
            p["Rating Counts"][j] += dr["Rating Counts"][j]

        p["Total Reports"] += (dr["Total Reports"] + 1)
        p["Rollup Salaries"] += dr["Rollup Salaries"]
        p["Missing Salaries"] += dr["Missing Salaries"]

    num_direct_reports = str(p["Num Direct Reports"])
    p["Num Direct Reports Counts"][list(num_direct_reports_colours).index(num_direct_reports)] += 1

    team = p["Person"]["Team"]
    p["Team Counts"][list(team_colours).index(team)] += 1

    type = p["Person"]["Type"]
    p["Type Counts"][list(type_colours).index(type)] += 1

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
        nine_box_performance_index = list(nine_box_colours[nine_box_potential]).index(nine_box_performance)
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
        if people[drs[i - 1]]["Person"]["Team"] == people[drs[i]]["Person"]["Team"]:
            continue

        for j in range(i + 1, len(drs)):
            if people[drs[i - 1]]["Person"]["Team"] == people[drs[j]]["Person"]["Team"]:
                for k in range(j, i, -1):
                    t = drs[j - 1]
                    drs[j - 1] = drs[j]
                    drs[j] = t

    start_date = p["Person"]["Start Date"]
    t = time.strptime(start_date, "%Y-%m-%d")
    ot = time.strptime("2016-01-01", "%Y-%m-%d")
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
            print(supervisor_uen, log_salary_usd, salary_usd)
            p["Salary Counts"][log_salary_usd] += 1

    if ("Grades" in p["Person"].keys()) and ("Salaries" in p["Person"].keys()):
        band_lower_salary = locations[location][grade]["Low"]
        band_upper_salary = locations[location][grade]["High"]
        band_mid_salary = (band_upper_salary + band_lower_salary) // 2
        salary_offset = salary - band_mid_salary
        p["Salary Offset"] = salary_offset
        salary_offset_usd = salary_offset * fx_rates[location]
        p["Salary Offset USD"] = salary_offset_usd
        salary_offset_percentage = (salary_offset / band_mid_salary) * 100
        p["Salary Offset Percentage"] = salary_offset_percentage

        salary_offset_usd_key = salary_offset_usd
        if salary_offset_usd_key > 50000:
            salary_offset_usd_key = 50000
        elif salary_offset_usd_key < -50000:
            salary_offset_usd_key = -50000

        salary_offset_key = (int(salary_offset_usd_key) // 10000) * 10000
        p["Salary Offset Key"] = str(salary_offset_key)
        p["Salary Offset Counts"][(50000 + salary_offset_key) // 10000] += 1

        band_offset = 0
        if salary < band_lower_salary:
            band_offset = -1
        elif salary > band_upper_salary:
            band_offset = 1

        p["Salary Band Offset"] = band_offset

def scan_json_people(json_data):
    people = {}
    top_level = 0
    failed = False

    all_people_list = json_data["People"]
    for i in all_people_list:
        uen = i["UEN"]
        people[uen] = {}
        people[uen]["Person"] = i
        people[uen]["Direct Reports"] = []

    for i in all_people_list:
        uen = i["UEN"]
        if "Supervisor UEN" not in i.keys():
            if top_level == 0:
                top_level = uen
            else:
                print(i["Name"], "does not have a supervisor, but", top_level, "is already set as top-level")
                failed = True
        else:
            supervisor_uen = i["Supervisor UEN"]
            people[supervisor_uen]["Direct Reports"].append(uen)

    return (failed, people, top_level)

def main():
    if len(sys.argv) != 2:
        print("Usage: org-planner <file>")
        return

    json_file_path = sys.argv[1]
    with open(json_file_path, encoding = 'utf-8') as user_file:
        json_data = json.load(user_file)

    all_locations = json_data["Locations"]

    fail, all_people, supervisor_uen = scan_json_people(json_data)
    if fail:
        exit()

    all_teams, all_types = scan_teams_and_types(all_people)
    all_teams.sort()

    ci = 0
    for i in all_teams:
        team_colours[i] = team_colours_list[ci]
        ci += 1

    ci = 0
    for i in all_types:
        type_colours[i] = type_colours_list[ci]
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
