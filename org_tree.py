import json
import sys

def scan_json(json_data):
    people = {}
    direct_reports = {}
    top_level = 0
    failed = False

    all_people_list = json_data["People"]
    for i in all_people_list:
        uen = i["UEN"]
        people[uen] = {}
        people[uen]["Person"] = i

        if "Supervisor UEN" not in i.keys():
            if top_level == 0:
                top_level = uen
            else:
                print(i["Name"], "does not have a supervisor, but", top_level, "is already set as top-level")
                failed = True
        else:
            supervisor_uen = i["Supervisor UEN"]
            if supervisor_uen not in direct_reports.keys():
                direct_reports[supervisor_uen] = []

            direct_reports[supervisor_uen].append(uen)

    return (failed, people, top_level, direct_reports)

def scan_org_tree(people, supervisor_uen, direct_reports, depth):
    if supervisor_uen in direct_reports.keys():
        for i in direct_reports[supervisor_uen]:
            scan_org_tree(people, i, direct_reports, depth + 1)

    people[supervisor_uen]["Org Depth"] = depth

json_file_path = r'people.json'
with open(json_file_path, encoding = 'utf-8') as user_file: 
    json_data = json.load(user_file) 

fail, all_people, top_level_supervisor, all_reports = scan_json(json_data)
if fail:
    exit()

scan_org_tree(all_people, top_level_supervisor, all_reports, 0)

level_count = [0] * 10
print(level_count)
for i in all_people:
    p = all_people[i]
    depth = p["Org Depth"]
    print(p["Person"]["UEN"], ":", p["Org Depth"])
    level_count[depth] += 1

for i in range(len(level_count)):
    print(i, ":", level_count[i])