import math
import time

from currencies import currencies, fx_rates
from EmploymentSunburstOrgWidget import employment_colours
from GenderSunburstOrgWidget import gender_colours
from GradeSunburstOrgWidget import grade_colours
from LocationSunburstOrgWidget import location_colours
from NumDirectReportsSunburstOrgWidget import num_direct_reports_colours
from NineBoxInfoWidget import nine_box_colours
from RatingSunburstOrgWidget import rating_colours
from SalaryBandOffsetSunburstOrgWidget import salary_band_offset_colours
from SalaryBandMidPointOffsetSunburstOrgWidget import salary_band_mid_point_offset_colours
from SalarySunburstOrgWidget import salary_colours
from TeamSunburstOrgWidget import team_colours

class person(object):
    """
    A class used to track information about a person.
    """
    def __init__(self) -> None:
        self._locations_ref_data = None
        self._uen = 0
        self._name = ""
        self._gender = "Unknown"
        self._email_address = ""
        self._github = []
        self._employments = []
        self._supervisors = []
        self._teams = []
        self._locations = []
        self._grades = []
        self._salaries = []
        self._bonuses = []
        self._uars = []
        self._ratings = []
        self._nine_boxes = []
        self._direct_reports = []

    def load(self, init, locations):
        """
        Load data into a person from a JSON-derived dictionary.
        """
        self._locations_ref_data = locations
        self._uen = init["UEN"]
        self._name = init["Name"]

        if "Gender" in init.keys():
            self._gender = init["Gender"]

        if "Email Address" in init.keys():
            self._email_address = init["Email Address"]

        if "GitHub" in init.keys():
            self._github = init["GitHub"]

        if "Employments" in init.keys():
            self._employments = init["Employments"]

        if "Supervisors" in init.keys():
            self._supervisors = init["Supervisors"]

        if "Teams" in init.keys():
            self._teams = init["Teams"]

        if "Locations" in init.keys():
            self._locations = init["Locations"]

        if "Grades" in init.keys():
            self._grades = init["Grades"]

        if "Salaries" in init.keys():
            self._salaries = init["Salaries"]

        if "Bonuses" in init.keys():
            self._bonuses = init["Bonuses"]

        if "UARs" in init.keys():
            self._uars = init["UARs"]

        if "Ratings" in init.keys():
            self._ratings = init["Ratings"]

        if "9 Box" in init.keys():
            self._nine_boxes = init["9 Box"]

    def get_name(self):
        return self._name

    def get_uen(self):
        return self._uen

    def has_email_address(self):
        return len(self._email_address) > 0

    def get_email_address(self):
        return self._email_address

    def has_supervisor(self):
        return len(self._supervisors) > 0

    def get_supervisor_uen(self):
        return self._supervisors[-1]["Supervisor UEN"]

    def has_github(self):
        return len(self._github) > 0

    def get_github_login(self):
        return self._github[-1]["Login"]

    def get_github_profile_url(self):
        return self._github[-1]["Profile URL"]

    def get_supervisor_fraction(self, people):
        if not self.has_supervisor():
            return 1.0

        p = people[self.get_supervisor_uen()]
        num_reports = p.get_total_reports(people)
        return (self.get_total_reports(people) + 1) / num_reports

    def get_service_duration(self):
        start_date = self._employments[-1]["Start Date"]
        t = time.strptime(start_date, "%Y-%m-%d")
        cur_time = time.time()
        return cur_time - time.mktime(t)

    def get_service_duration_fraction(self):
        start_date = self._employments[-1]["Start Date"]
        t = time.strptime(start_date, "%Y-%m-%d")

        # The company started on 2014-10-31.
        ot = (2014, 10, 31, 0, 0, 0, 0, 0, 0)
        cur_time = time.time()
        org_elapsed_time = cur_time - time.mktime(ot)
        worked_time = cur_time - time.mktime(t)
        return worked_time / org_elapsed_time

    def get_direct_reports(self, people):
        # Sort the direct reports to put the one with the largest fraction of the
        # org first.
        drs = self._direct_reports
        len_drs = len(drs)
        for i in range(len_drs):
            drs_j_sup_frac = people[drs[0]].get_supervisor_fraction(people)
            for j in range(len_drs - i - 1):
                drs_j_next_sup_frac = people[drs[j + 1]].get_supervisor_fraction(people)
                if drs_j_sup_frac >= drs_j_next_sup_frac:
                    drs_j_sup_frac = drs_j_next_sup_frac
                    continue

                t = drs[j + 1]
                drs[j + 1] = drs[j]
                drs[j] = t

        # Then sort any direct reports from the same team to cluster them.  While
        # this slightly undoes the sort it's a more natural view over the org,
        # placing people who do the same sorts of things in one grouping.
        for i in range(0, len_drs - 1):
            drs_i_team = people[drs[i]].get_team()
            if drs_i_team == people[drs[i + 1]].get_team():
                continue

            for j in range(i + 1, len_drs):
                if drs_i_team == people[drs[j]].get_team():
                    drs.insert(i + 1, drs.pop(j))
                    break

        return drs

    def append_direct_report(self, dr):
        self._direct_reports.append(dr)

    def get_num_direct_reports(self):
        return len(self._direct_reports)

    def get_num_direct_reports_counts(self, people):
        counts = [0] * len(num_direct_reports_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_num_direct_reports_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        counts[list(num_direct_reports_colours).index(str(self.get_num_direct_reports()))] += 1
        return counts

    def get_fte(self):
        if "Percentage Time" in self._employments[-1].keys():
            return self._employments[-1]["Percentage Time"] / 100

        return 1.0

    def get_team(self):
        return self._teams[-1]["Team"]

    def get_team_counts(self, people):
        counts = [0] * len(team_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_team_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        counts[list(team_colours).index(str(self.get_team()))] += 1
        return counts

    def is_employed(self):
        return "End Date" not in self._employments[-1].keys()

    def get_employment(self):
        return self._employments[-1]["Employment"]

    def get_start_date(self):
        return self._employments[-1]["Start Date"]

    def get_employment_counts(self, people):
        counts = [0] * len(employment_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_employment_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        counts[list(employment_colours).index(str(self.get_employment()))] += 1
        return counts

    def has_location(self):
        return len(self._locations) > 0

    def get_location(self):
        return self._locations[-1]["Location"]

    def get_location_counts(self, people):
        counts = [0] * len(location_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_location_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        if self.has_location():
            counts[list(location_colours).index(str(self.get_location()))] += 1

        return counts

    def has_grade(self):
        return len(self._grades) > 0

    def get_grade(self):
        return self._grades[-1]["Grade"]

    def get_grade_counts(self, people):
        counts = [0] * len(grade_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_grade_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        if self.has_grade():
            counts[list(grade_colours).index(str(self.get_grade()))] += 1

        return counts

    def get_gender(self):
        return self._gender

    def get_gender_counts(self, people):
        counts = [0] * len(gender_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_gender_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        counts[list(gender_colours).index(str(self.get_gender()))] += 1
        return counts

    def has_nine_box(self):
        return len(self._nine_boxes) > 0

    def get_nine_box_potential(self):
        return self._nine_boxes[-1]["Potential"]

    def get_nine_box_performance(self):
        return self._nine_boxes[-1]["Performance"]

    def get_nine_box_counts(self, people):
        counts = [[] for i in range(3)]
        for i in range(3):
            counts[i] = [0] * 3

        for i in self._direct_reports:
            res_counts = people[i].get_nine_box_counts(people)
            for j in range(3):
                counts[j] = [x + y for x, y in zip(counts[j], res_counts[j])]

        if self.has_nine_box():
            nine_box_potential = self.get_nine_box_potential()
            nine_box_potential_index = list(nine_box_colours).index(nine_box_potential)
            nine_box_performance_index = list(
                nine_box_colours[nine_box_potential]).index(self.get_nine_box_performance()
            )
            counts[nine_box_potential_index][nine_box_performance_index] += 1

        return counts

    def _str_usd(self, value):
        return f"${value:,.0f}".replace("$-", "-$")

    def _str_local(self, value):
        location = self.get_location()
        _, cur_sym = currencies[location]
        return f"{cur_sym}{value:,.0f}".replace(f"{cur_sym}-", f"-{cur_sym}")

    def has_salary(self):
        return len(self._salaries) > 0

    def get_salary(self):
        return self._salaries[-1]["Salary"]

    def get_salary_str(self):
        return self._str_local(self.get_salary())

    def get_salary_usd(self):
        salary = self._salaries[-1]["Salary"]
        return salary * fx_rates[self.get_location()]

    def get_salary_usd_str(self):
        return self._str_usd(self.get_salary_usd())

    def get_salary_counts(self, people):
        counts = [0] * len(salary_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_salary_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        if self.has_salary() and self.has_location():
            salary = self.get_salary()
            salary_usd = salary * fx_rates[self.get_location()]
            if salary_usd >= 10000:
                log_salary_usd = int((math.log10(salary_usd) - 4) / 0.25)
                counts[log_salary_usd] += 1

        return counts

    def has_salary_band(self):
        return self.has_salary() and self.has_grade() and self.has_location()

    def get_salary_band_lower_limit(self):
        location = self.get_location()
        corp_grade = self.get_grade()[:1]
        return self._locations_ref_data[location][corp_grade]["Low"] * self.get_fte()

    def get_salary_band_lower_limit_str(self):
        return self._str_local(self.get_salary_band_lower_limit())

    def get_salary_band_lower_limit_usd(self):
        location = self.get_location()
        fx_rate = fx_rates[location]
        return self.get_salary_band_lower_limit() * fx_rate

    def get_salary_band_lower_limit_usd_str(self):
        return self._str_usd(self.get_salary_band_lower_limit_usd())

    def get_salary_band_mid_point(self):
        return (self.get_salary_band_upper_limit() + self.get_salary_band_lower_limit()) / 2

    def get_salary_band_mid_point_str(self):
        return self._str_local(self.get_salary_band_mid_point())

    def get_salary_band_mid_point_usd(self):
        location = self.get_location()
        fx_rate = fx_rates[location]
        return self.get_salary_band_mid_point() * fx_rate

    def get_salary_band_mid_point_usd_str(self):
        return self._str_usd(self.get_salary_band_mid_point_usd())

    def get_salary_band_upper_limit(self):
        location = self.get_location()
        corp_grade = self.get_grade()[:1]
        return self._locations_ref_data[location][corp_grade]["High"] * self.get_fte()

    def get_salary_band_upper_limit_str(self):
        return self._str_local(self.get_salary_band_upper_limit())

    def get_salary_band_upper_limit_usd(self):
        location = self.get_location()
        fx_rate = fx_rates[location]
        return self.get_salary_band_upper_limit() * fx_rate

    def get_salary_band_upper_limit_usd_str(self):
        return self._str_usd(self.get_salary_band_upper_limit_usd())

    def get_salary_band_offset(self):
        salary = self.get_salary()
        band_lower_limit = self.get_salary_band_lower_limit()
        if salary < band_lower_limit:
            return salary - band_lower_limit

        band_upper_limit = self.get_salary_band_upper_limit()
        if salary > band_upper_limit:
            return salary - band_upper_limit

        return 0

    def get_salary_band_offset_str(self):
        return self._str_local(self.get_salary_band_offset())

    def get_salary_band_offset_usd(self):
        location = self.get_location()
        fx_rate = fx_rates[location]
        return self.get_salary_band_offset() * fx_rate

    def get_salary_band_offset_usd_str(self):
        return self._str_usd(self.get_salary_band_offset_usd())

    def get_salary_band_mid_point_offset(self):
        return self.get_salary() - self.get_salary_band_mid_point()

    def get_salary_band_mid_point_offset_str(self):
        return self._str_local(self.get_salary_band_mid_point_offset())

    def get_salary_band_mid_point_offset_usd(self):
        location = self.get_location()
        fx_rate = fx_rates[location]
        return self.get_salary_band_mid_point_offset() * fx_rate

    def get_salary_band_mid_point_offset_usd_str(self):
        return self._str_usd(self.get_salary_band_mid_point_offset_usd())

    def get_salary_band_offset_key(self):
        offset = int(self.get_salary_band_offset_usd())
        if offset == 0:
            return 0

        if offset < 0:
            key = (offset - 9999) // 10000
            if key < -5:
                key = -5
        else:
            key = (offset + 9999) // 10000
            if key > 5:
                key = 5

        return key

    def get_salary_band_offset_counts(self, people):
        counts = [0] * len(salary_band_offset_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_salary_band_offset_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        if self.has_salary_band():
            counts[5 + self.get_salary_band_offset_key()] += 1

        return counts

    def get_salary_band_mid_point_offset_key(self):
        key = int(self.get_salary_band_mid_point_offset_usd() + 5000) // 10000
        if key > 5:
            return 5

        if key < -5:
            return -5

        return key

    def get_salary_band_mid_point_offset_counts(self, people):
        counts = [0] * len(salary_band_mid_point_offset_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_salary_band_mid_point_offset_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        if self.has_salary_band():
            counts[5 + self.get_salary_band_mid_point_offset_key()] += 1

        return counts

    def has_rating(self):
        return len(self._ratings) > 0

    def get_rating(self):
        return self._ratings[-1]["Rating"]

    def get_rating_counts(self, people):
        counts = [0] * len(rating_colours)

        for i in self._direct_reports:
            res_counts = people[i].get_rating_counts(people)
            counts = [x + y for x, y in zip(counts, res_counts)]

        if self.has_rating():
            counts[list(rating_colours).index(str(self.get_rating()))] += 1

        return counts

    def get_total_reports(self, people):
        reports = 0
        for i in self._direct_reports:
            reports += people[i].get_total_reports(people) + 1

        return reports

    def get_rollup_salaries(self, people):
        rollup_salaries = 0
        missing_salaries = 0
        for i in self._direct_reports:
            (r, m) = people[i].get_rollup_salaries(people)
            rollup_salaries += r
            missing_salaries += m

        if not self.has_salary() or not self.has_location():
            missing_salaries += 1
        else:
            salary = self.get_salary()
            salary_usd = salary * fx_rates[self.get_location()]
            rollup_salaries += salary_usd

        return (rollup_salaries, missing_salaries)

    def get_org_depth(self, people):
        depth = 0
        p = self

        while p.has_supervisor():
            depth += 1
            supervisor_uen = p.get_supervisor_uen()
            p = people[supervisor_uen]

        return depth
