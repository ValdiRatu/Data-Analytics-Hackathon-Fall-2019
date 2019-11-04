import pandas as pd
import numpy as np


class Specialization:
    def __init__(self, name):
        self.name = name
        self.requirements = pd.DataFrame(columns=['courses', 'faculty'])
        self.future = pd.DataFrame(columns=['courses', 'faculty'])

    def add_requirements(self, course):
        self.requirements = self.requirements.append(course)

    def add_future(self, course):
        self.future = self.future.append(course)


def main():
    canvas_dataPre = pd.read_csv("ubc_course_calendar_data.csv", index_col=False)

    canvas_data = canvas_dataPre.dropna(subset=['COURSE_NUMBER',
                                                'SUBJECT_CODE', 'PRE_REQUISITE_DESCRIPTIONS'])

    def course_predictor(s1, subject_code, course_number):
        s1 = s1[s1['PRE_REQUISITE_DESCRIPTIONS'].str.contains(course_number)]
        s1 = s1[s1['PRE_REQUISITE_DESCRIPTIONS'].str.contains(subject_code)]
        return s1

    def course_getter(course, subject_code, course_number):
        course = course[course['COURSE_NUMBER'].str.contains(course_number)]
        course = course[course['SUBJECT_CODE'].str.contains(subject_code)]
        return course

    def results_dataset(pre_req_match):
        courses = pd.DataFrame(columns=[])
        courses['future_courses'] = pre_req_match['SUBJECT_CODE'] + ' ' + pre_req_match['COURSE_NUMBER']
        courses['future_faculty'] = pre_req_match['FACULTY']
        courses = courses.drop_duplicates()
        return courses

    def course_dataset(course_match):
        courses = pd.DataFrame(columns=[])
        courses['courses'] = course_match['SUBJECT_CODE'] + ' ' + course_match['COURSE_NUMBER']
        courses['faculty'] = course_match['FACULTY']
        courses = courses.drop_duplicates()
        return courses

    def remove_duplicates(course_list):
        course_list = course_list.drop_duplicates()
        return course_list

    listOfFutureCourses = pd.DataFrame(columns=['future_courses', 'future_faculty'])

    courses = pd.DataFrame(columns=['courses', 'faculty'])

    cpscSpecialization = Specialization("Computer Science")

    cpscSpecialization.add_requirements(course_dataset(course_getter(canvas_dataPre, "CPSC", "110")))
    cpscSpecialization.add_requirements(course_dataset(course_getter(canvas_dataPre, "CPSC", "103")))

    cpscSpecialization.add_future(course_dataset(course_getter(canvas_dataPre, "CPSC", "210")))
    cpscSpecialization.add_future(course_dataset(course_getter(canvas_dataPre, "CPSC", "221")))
    cpscSpecialization.add_future(course_dataset(course_getter(canvas_dataPre, "CPSC", "213")))

    physSpecialization = Specialization("Physics")

    physSpecialization.add_requirements(course_dataset(course_getter(canvas_dataPre, "PHYS", "117")))
    physSpecialization.add_requirements(course_dataset(course_getter(canvas_dataPre, "PHYS", "118")))

    physSpecialization.add_future(course_dataset(course_getter(canvas_dataPre, "PHYS", "200")))
    physSpecialization.add_future(course_dataset(course_getter(canvas_dataPre, "PHYS", "216")))

    while True:
        course = input("Enter course: ")
        predicted = results_dataset(course_predictor(canvas_data, course.split()[0], course.split()[1]))
        courseadd = course_dataset(course_getter(canvas_dataPre, course.split()[0], course.split()[1]))
        courses = courses.append(courseadd)
        listOfFutureCourses = remove_duplicates(listOfFutureCourses.append(predicted))

        print(listOfFutureCourses)
        print(courses)

        if True in courses.isin(cpscSpecialization.requirements).values:
            print(cpscSpecialization.name)
            print(cpscSpecialization.future)
        if True in courses.isin(physSpecialization.requirements).values:
            print(physSpecialization.name)
            print(physSpecialization.future)
        else:
            print('No specialization found')


if __name__ == "__main__":
    main()

# MIT License

# Copyright (c) [2019] [Valdi Ratu, Hans Lam, Bob Chen, Furqan Khan]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
