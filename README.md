# Project Proposal — Ursinus Course Planner

# Alex Hickman, Claire Shoemaker, & Luke Jeffries<br>Professor Ralph Rostock<br>CS 375-A<br>February 18, 2026 

## Description 

Over the course of the semester, we are going to build a project that helps students to plan their classes during their time at Ursinus. The user will provide their majors/minors, their interests outside of their fields of study, and which courses they’ve already taken, and the app will output a potential schedule spanning 2 semesters. This schedule will include their major requirements, as well as their general requirements which will be selected using the other interests inputted. The app will make use of the Ursinus Course catalog and the Quest Curriculum requirements to accurately compile a schedule. It will involve sorting through a large amount of data, as well as organizing that data into traversable data structures so that the information can be easily extracted.  

## Compelling Need 

Registering for classes is a cumbersome, time-consuming process. It involves identifying which major courses a student must take, as well as understanding which general education courses are required. Attempting to comb through the lengthy course catalog to find which courses meet what requirements, when each of the courses are offered, and deciding if the student is interested can take a long time. Our solution will aim to make this process easier for the students, allowing them to easily see which classes they can take and when they can take them. Faculty members at Ursinus who serve as advisors can also take advantage of this software to help their advisees schedule their courses.  

## Stakeholder Groups 

Students and advisors at Ursinus College would be able to put our software to use to aid course selection and alleviate stress. We plan to regularly update our stakeholders, such as professors who serve as advisors through emails and possible meetings. We’ll take into account any feedback they have regarding our solutions functionality.  

## Technical Expertise 

We have proficiency in programming languages such as python and C++languages, however we will need to learn how to utilize git and github to better communicate and collaborate our work on this project. 

## Minimum Viable Project Scope 

We would need to at least have functionality in place that takes in the student's major, minor and other interests, searches through the course catalog to find the relevant courses and then outputs the student schedule for 2 semesters. At first, we will limit our project to planning Computer Science, Mathematics, and Statistics majors’ schedules. The resulting schedule would need to reflect Ursinus College’s graduation requirements and would consider when each course is offered.  We will use a pdf processing library to convert the information into a text file, then attempt to traverse that text and extract the relevant course information. We would then put that information into a dictionary, which will be more easily traversed when looking for specific courses. We’re starting with only the Computer Science department to assess the feasibility of doing this with the entire catalog.  

## Aspirant Scope 

Time allowing, we would like to incorporate more AI elements into the project. The AI agent would automate the process of searching through the course catalog. It would zero in on the sections relevant to the students' interests and then would use that information to compile a schedule for them. We could also add a chat feature where the student could ask questions about the classes or make changed to the current schedule. We are also striving to increase the capabilities of the software to plan out a full college career of 8 semesters. Another feature that we would ideally incorporate would be broadening the scope of the project to all majors offered at Ursinus. Being able to generalize this software to other universities’ courses would allow us to bring this product to more users though it may prove unrealistic in the allotted time. 

## Timeline 

The timeline of our Project will stretch until the end of the semester. We will have 1-week sprints where we can rally together and share ideas as well as review work done during the previous week.  

## Intellectual Merit 

Ursinus doesn’t have a scheduling tool of this nature, so this has the potential to make the whole scheduling process more efficient for advisors and students. It’s worth making this tool to ease the stress and burden of planning courses through your college career and add convenience to the process. 

## Broader Impacts 

Students and advisors at Ursinus would benefit. If the project grows beyond the scope of Ursinus, then other students at other colleges could benefit as well.  
