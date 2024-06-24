import React from 'react';
import logo from './logo.svg';
import './App.css';
import {Link, Route, Routes, BrowserRouter } from 'react-router-dom';
import { NavBar } from './NavBar';
import { Work } from './Work';

function Main() {
  var experienceJson = [
    {
      company: "Georgia Institute of Technology",
      website: "https://www.gatech.edu/",
      location: "Atlanta, GA",
      position: "Master of Science - Computer Science",
      date: "Starts 08.2024",
      acheivements: [
      ]
    },
    {
      company: "The Ohio State University",
      website: "https://www.osu.edu/",
      location: "Columbus, OH",
      position: "Bachelor of Science - Computer Science",
      date: "08.2020 - 05.2024",
      acheivements: [
        {
          name: "Land Grant Opportunity Scholarship (Full Ride) ",
          link: "https://undergrad.osu.edu/cost-and-aid/merit-based-scholarships"
        }
      ] 
      
    },
    {
      company: "Expedia Group",
      website: "https://www.expedia.com/",
      location: "Seattle, WA",
      position: "Software Development Engineer Intern",
      date: "05.2024 - 08.2024",
      acheivements: [
      ]
    },
    {
      company: "Expedia Group",
      website: "https://www.expedia.com/",
      location: "Seattle, WA",
      position: "Software Development Engineer Intern",
      date: "05.2023 - 08.2023",
      acheivements: [
      ]
    },
    {
      company: "Clinisys",
      website: "https://www.clinisys.com/in/en/",
      location: "Tucson, AZ",
      position: "Software Engineer Intern",
      date: "05.2022 - 08.2022",
      acheivements: [
      ]
    },
    {
      company: "Ohio State College of Engineering",
      website: "https://engineering.osu.edu/",
      location: "Columbus, OH",
      position: "Teaching Assistant II",
      date: "08.2021 - 05.2024",
      acheivements: [
      ]
    },
    {
      company: "Robintek",
      website: "https://www.robintek.com/",
      location: "Westerville, OH",
      position: "Software Engineer Intern",
      date: "05.2021 - 08.2021",
      acheivements: [
      ]
    },
  ];

  var experiences = [];

  for (var i = 0; i < experienceJson.length; i++) {
    var experience = experienceJson[i];
  
    var achievements = [];
  
    for (var achievement of experience.acheivements) {
      achievements.push(<div className="achievement"><a href={achievement.link} target="_blank">- {achievement.name}</a></div>);
    }
  
    experiences.push(
      <>      
        <div className="experience">
          <div className="exp-row1">
            <div style={{ flex: 1 }} id="place"><a href={experience.website} target="_blank">{experience.company}</a></div>
            <div>{experience.date}</div>
          </div>
          <div className="exp-row2">
            <div id="position" style={{ flex: 1 }}>{experience.position}</div>
            <div><i>{experience.location}</i></div>
          </div>
          <div className="exp-row3">
            <div className="achievement-container">
              <div className="achievement-list">
                {achievements}
              </div>
            </div>
          </div>
        </div>
        <hr/>
      </>
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
            <p>SDE Intern @ Expedia | MSCS @ Georgia Tech</p>
          </div>

        </div>
          <div>
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
      <Route path="/school" element={<Work />} />
    </Routes>
  </BrowserRouter>
  );
}

export default App;