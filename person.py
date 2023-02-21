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
from SalaryMidBandOffsetSunburstOrgWidget import salary_mid_band_offset_colours
from SalarySunburstOrgWidget import salary_colours
from TeamSunburstOrgWidget import team_colours

class person(object):
    """
    A class used to track information about a person.
    """
    def __init__(self) -> None:
        self._uen = 0
        self._name = ""
        self._gender = "Unknown"
        self._email_address = ""
        self._github = []
        self._employments = []
        self._service_duration = 0
        self._service_duration_fraction = 0
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
        self._org_depth = -1
        self._supervisor_fraction = 0.0
        self._fte = 1.0
        self._total_reports = 0
        self._rollup_salaries = 0
        self._missing_salaries = 0
        self._salary_band_lower_limit = 0
        self._salary_band_lower_limit_usd = 0
        self._salary_band_upper_limit = 0
        self._salary_band_upper_limit_usd = 0
        self._salary_band_mid_point = 0
        self._salary_band_mid_point_usd = 0
        self._salary_mid_band_offset = 0
        self._salary_mid_band_offset_usd = 0
        self._salary_mid_band_offset_key = 0
        self._salary_band_offset = 0
        self._salary_band_offset_usd = 0
        self._salary_band_offset_key = 0

    def load(self, init, locations):
        """
        Load data into a person from a JSON-derived dictionary.
        """
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
            start_date = init["Employments"][-1]["Start Date"]
            t = time.strptime(start_date, "%Y-%m-%d")
            ot = time.strptime("2014-10-31", "%Y-%m-%d")
            cur_time = time.time()
            org_elapsed_time = cur_time - time.mktime(ot)
            worked_time = cur_time - time.mktime(t)
            self._service_duration = cur_time - time.mktime(t)
            self._service_duration_fraction = worked_time / org_elapsed_time

            if "Percentage Time" in self._employments[-1].keys():
                self._fte = self._employments[-1]["Percentage Time"] / 100

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

        if (("Grades" in init.keys()) and
                ("Salaries" in init.keys()) and
                ("Locations" in init.keys())):
            location = self.get_location()
            fx_rate = fx_rates[location]

            corp_grade = self.get_grade()[:1]
            band_lower_limit = locations[location][corp_grade]["Low"] * self._fte
            self._salary_band_lower_limit = band_lower_limit
            self._salary_band_lower_limit_usd = band_lower_limit * fx_rate
            band_upper_limit = locations[location][corp_grade]["High"] * self._fte
            self._salary_band_upper_limit = band_upper_limit
            self._salary_band_upper_limit_usd = band_upper_limit * fx_rate
            band_mid_salary = (band_upper_limit + band_lower_limit) / 2
            self._salary_band_mid_point = band_mid_salary
            self._salary_band_mid_point_usd = band_mid_salary * fx_rate

            salary = self.get_salary()
            salary_mid_band_offset = salary - band_mid_salary
            self._salary_mid_band_offset = salary_mid_band_offset
            salary_mid_band_offset_usd = salary_mid_band_offset * fx_rate
            self._salary_mid_band_offset_usd = salary_mid_band_offset_usd

            salary_mid_band_offset_key = int(salary_mid_band_offset_usd + 5000) // 10000
            if salary_mid_band_offset_key > 5:
                salary_mid_band_offset_key = 5
            elif salary_mid_band_offset_key < -5:
                salary_mid_band_offset_key = -5

            self._salary_mid_band_offset_key = salary_mid_band_offset_key

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

            self._salary_band_offset = band_offset
            self._salary_band_offset_usd = band_offset_usd
            self._salary_band_offset_key = band_offset_key

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

    def get_supervisor_fraction(self):
        return self._supervisor_fraction

    def set_supervisor_fraction(self, fraction):
        self._supervisor_fraction = fraction

    def get_service_duration(self):
        return self._service_duration

    def get_service_duration_fraction(self):
        return self._service_duration_fraction

    def get_direct_reports(self):
        return self._direct_reports

    def append_direct_report(self, dr):
        self._direct_reports.append(dr)

    def get_num_direct_reports(self):
        return len(self._direct_reports)

    def _get_num_direct_reports_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_num_direct_reports_counts(people, counts)

        counts[list(num_direct_reports_colours).index(str(self.get_num_direct_reports()))] += 1

    def get_num_direct_reports_counts(self, people):
        counts = [0] * len(num_direct_reports_colours)
        self._get_num_direct_reports_counts(people, counts)
        return counts

    def get_fte(self):
        return self._fte

    def get_team(self):
        return self._teams[-1]["Team"]

    def _get_team_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_team_counts(people, counts)

        counts[list(team_colours).index(str(self.get_team()))] += 1

    def get_team_counts(self, people):
        counts = [0] * len(team_colours)
        self._get_team_counts(people, counts)
        return counts

    def get_employment(self):
        return self._employments[-1]["Employment"]

    def get_start_date(self):
        return self._employments[-1]["Start Date"]

    def _get_employment_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_employment_counts(people, counts)

        counts[list(employment_colours).index(str(self.get_employment()))] += 1

    def get_employment_counts(self, people):
        counts = [0] * len(team_colours)
        self._get_employment_counts(people, counts)
        return counts

    def has_location(self):
        return len(self._locations) > 0

    def get_location(self):
        return self._locations[-1]["Location"]

    def _get_location_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_location_counts(people, counts)

        if self.has_location():
            counts[list(location_colours).index(str(self.get_location()))] += 1

    def get_location_counts(self, people):
        counts = [0] * len(location_colours)
        self._get_location_counts(people, counts)
        return counts

    def has_grade(self):
        return len(self._grades) > 0

    def get_grade(self):
        return self._grades[-1]["Grade"]

    def _get_grade_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_grade_counts(people, counts)

        if self.has_grade():
            counts[list(grade_colours).index(str(self.get_grade()))] += 1

    def get_grade_counts(self, people):
        counts = [0] * len(grade_colours)
        self._get_grade_counts(people, counts)
        return counts

    def get_gender(self):
        return self._gender

    def _get_gender_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_gender_counts(people, counts)

        counts[list(gender_colours).index(str(self.get_gender()))] += 1

    def get_gender_counts(self, people):
        counts = [0] * len(gender_colours)
        self._get_gender_counts(people, counts)
        return counts

    def has_nine_box(self):
        return len(self._nine_boxes) > 0

    def get_nine_box_potential(self):
        return self._nine_boxes[-1]["Potential"]

    def get_nine_box_performance(self):
        return self._nine_boxes[-1]["Performance"]

    def _get_nine_box_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_nine_box_counts(people, counts)

        if self.has_nine_box():
            nine_box_potential = self.get_nine_box_potential()
            nine_box_potential_index = list(nine_box_colours).index(nine_box_potential)
            nine_box_performance_index = list(
                nine_box_colours[nine_box_potential]).index(self.get_nine_box_performance()
            )
            counts[nine_box_potential_index][nine_box_performance_index] += 1

    def get_nine_box_counts(self, people):
        counts = [[] for i in range(3)]
        for i in range(3):
            counts[i] = [0] * 3

        self._get_nine_box_counts(people, counts)
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

    def get_salary_usd(self):
        salary = self._salaries[-1]["Salary"]
        return salary * fx_rates[self.get_location()]

    def _get_salary_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_salary_counts(people, counts)

        if self.has_salary() and self.has_location():
            salary = self.get_salary()
            salary_usd = salary * fx_rates[self.get_location()]
            if salary_usd >= 10000:
                log_salary_usd = int((math.log10(salary_usd) - 4) / 0.25)
                counts[log_salary_usd] += 1

    def get_salary_counts(self, people):
        counts = [0] * len(salary_colours)
        self._get_salary_counts(people, counts)
        return counts

    def get_salary_mid_band_offset_key(self):
        return self._salary_mid_band_offset_key

    def _get_salary_mid_band_offset_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_salary_mid_band_offset_counts(people, counts)

        counts[5 + self.get_salary_mid_band_offset_key()] += 1

    def get_salary_mid_band_offset_counts(self, people):
        counts = [0] * len(salary_mid_band_offset_colours)
        self._get_salary_mid_band_offset_counts(people, counts)
        return counts

    def has_salary_band(self):
        return self.has_salary() and self.has_grade() and self.has_location()

    def get_salary_band_offset_key(self):
        return self._salary_band_offset_key

    def _get_salary_band_offset_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_salary_band_offset_counts(people, counts)

        counts[5 + self.get_salary_band_offset_key()] += 1

    def get_salary_band_offset_counts(self, people):
        counts = [0] * len(salary_band_offset_colours)
        self._get_salary_band_offset_counts(people, counts)
        return counts

    def get_salary_mid_band_offset(self):
        return self._salary_mid_band_offset

    def get_salary_mid_band_offset_str(self):
        return self._str_local(self.get_salary_mid_band_offset())

    def get_salary_mid_band_offset_usd(self):
        return self._salary_mid_band_offset_usd

    def get_salary_mid_band_offset_usd_str(self):
        return self._str_usd(self.get_salary_mid_band_offset_usd())

    def get_salary_band_offset(self):
        return self._salary_band_offset

    def get_salary_band_offset_usd(self):
        return self._salary_band_offset_usd

    def get_salary_band_mid_point(self):
        return self._salary_band_mid_point

    def get_salary_band_mid_point_usd(self):
        return self._salary_band_mid_point_usd

    def get_salary_band_lower_limit(self):
        return self._salary_band_lower_limit

    def get_salary_band_lower_limit_usd(self):
        return self._salary_band_lower_limit_usd

    def get_salary_band_upper_limit(self):
        return self._salary_band_upper_limit

    def get_salary_band_upper_limit_usd(self):
        return self._salary_band_upper_limit_usd

    def has_rating(self):
        return len(self._ratings) > 0

    def get_rating(self):
        return self._ratings[-1]["Rating"]

    def _get_rating_counts(self, people, counts):
        for i in self._direct_reports:
            people[i]._get_rating_counts(people, counts)

        if self.has_rating():
            counts[list(rating_colours).index(str(self.get_rating()))] += 1

    def get_rating_counts(self, people):
        counts = [0] * len(rating_colours)
        self._get_rating_counts(people, counts)
        return counts

    def _get_total_reports(self, people):
        reports = 0
        for i in self._direct_reports:
            reports += people[i]._get_total_reports(people) + 1

        return reports

    def get_total_reports(self, people):
        return self._get_total_reports(people)

    def _get_rollup_salaries(self, people):
        rollup_salaries = 0
        missing_salaries = 0
        for i in self._direct_reports:
            (r, m) = people[i]._get_rollup_salaries(people)
            rollup_salaries += r
            missing_salaries += m

        if not self.has_salary() or not self.has_location():
            missing_salaries += 1
        else:
            salary = self.get_salary()
            salary_usd = salary * fx_rates[self.get_location()]
            rollup_salaries += salary_usd

        return (rollup_salaries, missing_salaries)

    def get_rollup_salaries(self, people):
        return self._get_rollup_salaries(people)

    def get_org_depth(self):
        return self._org_depth

    def set_org_depth(self, depth):
        self._org_depth = depth
