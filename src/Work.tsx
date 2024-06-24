import './App.css';
import { NavBar } from './NavBar'
import {Link, Route, Routes, BrowserRouter } from 'react-router-dom';

export const Work = () => {
    var gtCoursesJson = [
      
    ];

    var osuCoursesJson = [
      {
        course: "CSE 5914",
        name: "Capstone: Knowledge-Based Systems"
      },
      {
        course: "CSE 5236",
        name: "Mobile Application Development"
      },
      {
        course: "CSE 4471",
        name: "Information Security"
      },
      {
        course: "CSE 4256",
        name: "Python Programming"
      },
      {
        course: "CSE 4253",
        name: "C# Programming"
      },
      {
        course: "CSE 4252",
        name: "C++ Programminng"
      },
      {
        course: "CSE 4251",
        name: "UNIX Programming"
      },
      {
        course: "CSE 3901",
        name: "Web Application Development"
      },
      {
        course: "CSE 3521",
        name: "Artificial Intelligence"
      },
      {
        course: "CSE 3461",
        name: "Computer Networks"
      },
      {
        course: "CSE 3341",
        name: "Programming Languages"
      },
      {
        course: "CSE 3244",
        name: "Data Management in the Cloud"
      },
      {
        course: "CSE 3241",
        name: "Database Systems"
      },
      {
        course: "CSE 3232",
        name: "Software Requirements Analysis"
      },
      {
        course: "CSE 3231",
        name: "Software Engineering Techniques"
      },
      {
        course: "CSE 2431",
        name: "Operating Systems"
      },
      {
        course: "CSE 2421",
        name: "Computer Organizations"
      },
      {
        course: "CSE 2331",
        name: "Data Structures and Algorithms"
      },
      {
        course: "CSE 2321",
        name: "Discrete Structures"
      },
      {
        course: "CSE 2231",
        name: "Software Design and Development"
      },
      {
        course: "CSE 2221",
        name: "Software Components"
      },
      {
        course: "ECE 2060",
        name: "Digital Logic"
      },
      {
        course: "ECE 2020",
        name: "Analog Systems and Circuits"
      },
      {
        course: "ENGR 1282",
        name: "Honors Engineering II"
      },
      {
        course: "ENGR 1281",
        name: "Honors Engineering I"
      },
    ]

    var oohsCoursesJson = [
      "AP Computer Science A",
      "AP Chemistry",
      "AP Physics C: Mechanics",
      "AP Physics I",
      "AP Calculus BC",
      "AP Calculus AB",
      "AP Statistics",
      "AP Microeconomics",
      "AP Macroeconomics",
      "AP Music Theory",
      "CSCI 1103 - Intro to Programming Logic",
      "ENGL 1100 - Composition I",
      "PSY 1100 - Intro to Psychology",
      "POLS 1100 - American Government",
      "HIST 1152 - American History Since 1877"
    ]

    var experiences = [];
    var experiences2 = [];
    var experiences3 = [''];

    for (var i = 0; i < osuCoursesJson.length; i++) {
      var course = osuCoursesJson[i];
  
      experiences.push(
        <div>
          {course.course} - {course.name}
        </div>
      );

    }

    for (var i = 0; i < oohsCoursesJson.length; i++) {
      var course2 = oohsCoursesJson[i];
  
      experiences2.push(
        <div>
          {course2}
        </div>
      );

    }

    return (
        <div className="container">
            <div className="top">
              <NavBar/>
            </div>

            <div className="content">
              <div className="exp-row1" style={{ marginBottom: 7 }}>
                <div style={{ flex: 1 }} id="place"><a href="d" target="_blank">The Ohio State University</a></div>
                <div>2020 - 2024</div>
              </div>
                  {experiences}
                  <hr/>
              <div className="exp-row1" style={{ marginBottom: 7 }}>
                <div style={{ flex: 1 }}><a href="d" target="_blank">Olentangy Orange High School</a></div>
                <div>2016 - 2020</div>
              </div>
                  {experiences2}
            </div>
        </div>
    );
}