import React from 'react';
import logo from './logo.svg';
import './App.css';
import {Link, Route, Routes, BrowserRouter } from 'react-router-dom';
import { NavBar } from './NavBar';

function Main() {
  var experienceJson = [
    {
      company: "The Ohio State University",
      website: "",
      location: "Columbus, OH",
      position: "B.S. in Computer Science",
      date: "08.2020 - 12.2024",
      acheivements: [
        "Land Grant Scholarship (Full Ride) ",
      ]
    },
    {
      company: "Expedia Group",
      website: "",
      location: "Seattle, WA",
      position: "Software Development Engineer Intern",
      date: "05.2023 - 08.2023",
      acheivements: [
      ]
    },
    {
      company: "Clinisys",
      website: "",
      location: "Tucson, AZ",
      position: "Software Engineer Intern",
      date: "05.2022 - 08.2022",
      acheivements: [
      ]
    },
    {
      company: "Ohio State College of Engineering",
      website: "",
      location: "Columbus, OH",
      position: "Teaching Assistant II",
      date: "08.2021 - Present",
      acheivements: [
      ]
    },
    {
      company: "Robintek",
      website: "",
      location: "Westerville, OH",
      position: "Software Engineer Intern",
      date: "05.2021-08.2021",
      acheivements: [
      ]
    },
  ];

  var experiences = [];

  for (var i = 0; i < experienceJson.length; i++) {
    var experience = experienceJson[i];
  
    var achievements = [];
  
    for (var achievement of experience.acheivements) {
      achievements.push(<div className="achievement" dangerouslySetInnerHTML={{ __html: "  -     " + achievement }}/>);
    }
  
    experiences.push(
      <div className="experience">
        <div className="exp-row1">
          <div style={{ flex: 1 }}><b><a href={experience.website} target="_blank">{experience.company}</a></b></div>
          <div><b>{experience.location}</b></div>
        </div>
        <div className="exp-row2">
          <div id="position" style={{ flex: 1 }}>{experience.position}</div>
          <div>{experience.date}</div>
        </div>
        <div className="exp-row3">
          <div className="achievement-container">
            <div className="achievement-list">
              {achievements}
            </div>
          </div>
        </div>
        <hr/>
      </div>
    )
  }

  return (
    <div className="container">
        <div className="top">
            <NavBar/>
        </div>
        <div className="profile">
          <img src={require('./images/bitmoji.png')}/>
          <div className="profile-des">
            <h2>Jay Shin</h2>
            <p>Ex-Expedia | CSE @ Ohio State</p>
          </div>

        </div>
          <div className="cotent">
            {experiences}
          </div>
      </div>
  );
}

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="" element={<Main />} />
      <Route path="/" element={<Main />} />
      <Route path="/work" element={<Main />} />
    </Routes>
  </BrowserRouter>
  );
}

export default App;