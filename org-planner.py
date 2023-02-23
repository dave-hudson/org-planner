import csv
import json
import sys

from PySide6 import QtWidgets

from EmploymentSunburstOrgWidget import employment_colours
from MainWindow import MainWindow
from person import person
from TeamSunburstOrgWidget import team_colours

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
        team = i["Teams"][-1]["Team"]
        if team not in teams:
            teams.append(team)

        employment_type = i["Employments"][-1]["Employment"]
        if employment_type not in employments:
            employments.append(employment_type)

    return (teams, employments)

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

def scan_json_people(all_people_list, locations):
    people = {}
    top_level = 0
    failed = False

    for i in all_people_list:
        uen = i["UEN"]
        people[uen] = person()
        people[uen].load(i, locations)

    for i in all_people_list:
        uen = i["UEN"]

        if not people[uen].is_employed():
            continue

        if not people[uen].has_supervisor():
            if top_level == 0:
                top_level = uen
            else:
                print(i["Name"], "does not have a supervisor, but",
                        top_level, "is already set as top-level")
                failed = True
        else:
            supervisor_uen = i["Supervisors"][-1]["Supervisor UEN"]
            people[supervisor_uen].append_direct_report(uen)

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

                if (("Supervisors" not in i.keys()) or
                        (i["Supervisors"][-1]["Supervisor UEN"] == 0)):
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

    all_teams, all_employments = scan_teams_and_employments(all_people_list)
    all_teams.sort()

    ci = 0
    for i in all_teams:
        team_colours[i] = team_colours_list[ci]
        ci += 1

    ci = 0
    for i in all_employments:
        employment_colours[i] = employment_colours_list[ci]
        ci += 1

    fail, all_people, supervisor_uen = scan_json_people(all_people_list, all_locations)
    if fail:
        exit()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(1536, 900)
    window.set_locations(all_locations)
    window.set_people(all_people, supervisor_uen)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
