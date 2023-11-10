import './App.css';
import { NavBar } from './NavBar'
import {Link, Route, Routes, BrowserRouter } from 'react-router-dom';

export const Work = () => {
    var projectJson = [
        {
            name: "CSE 101 @ The Ohio State University",
            website: "",
            location: "",
            tools: "TypeScript, MongoDB, React.js, Express.js, Node.js, Bootstrap",
            date: "",
            summary: [
              "An informative website for my major. Built a drag & drop schedule builder and a class review feature. "
            ],
            description: [
              "I built this full-stack website as a practice of using the MERN stack. ", 
              "This is meant to give CSE students (especially freshmen) at The Ohio State University a guide to our computer science program. ",
              "I used <a href=\"\">react-dnd library</a> to algorithmically build a drag and drop scheduler builder that checks pre-requisites and co-requisites and your progress towards graduation. ",
              "There were limited information and tutorials about this library, but when I finally figured it out, it was powerful. ",
              "Inspired by ratemyprofessors.com, I also built a course review and rating feature with a simple CRUD system for reviews and also a login system. ",
              "Before signing up for classes in college, I’ve always wanted to know the actual experience or the informal description of classes. ",
              "Reddit was usually where I went to find them, but they were usually scattered in multiple posts. ",
              "I combined them into 1 page. ",
              "Other than these, there are also nicely designed prerequisite charts and very useful and informal freshman tips and Q&A’s. "
            ], 
            picture: "./images/"
        },
        {
            name: "Robinhood Trading Bot",
            website: "",
            location: "",
            tools: "Python, Robinhood API, Discord API, robin_stocks",
            date: "",
            summary: [
              "Built a bot that automates stock trading based on historical data and target prices. "
            ],
            description: [
              "I built this Python stock trading bot because I wanted to make money while doing nothing. ",
              "All I have to do is run this program and go to work. ",
              "This bot uses a very defensive and safe algorithm that won’t let me lose money. ",
              "This algorithm utilizes historical data and target price to buy and sell. "
            ], 
            picture: "./images/"
        },
        {
            name: "CSE 5236 Project - SwiftyNews",
            website: "",
            location: "",
            tools: "Swift, Xcode, Firebase, OpenAI API, NewsAPI",
            date: "",
            summary: [
              "An iOS application that summarizes and categorizes news articles for busy audiences. "
            ],
            description: [
              "This project was built as a semester project in CSE 5236. ",
              "So this app summarizes local news articles to cater busy audiences and let them stay informed with a click or two. ",
              "How it does this is, this iOS application receives user location, finds news articles around you by calling the NewsAPI, summarizes the article in bullet points by calling the OpenAI API, and displays in a nice UI format. ",
              "I also implemented CRUDing user accounts, liking posts, and searching for articles with a search bar. ",
              "Pretty simple idea, but it can be pretty useful. "
            ], 
            picture: "./images/"
        },   
        {
            name: "Fantasy Show Me The Money",
            website: "",
            location: "",
            tools: "React.js",
            date: "",
            summary: [
              "Built a fantasy version of Show Me The Money 11, a rap competition TV show in South Korea. "
            ],
            description: [
              "So many CS LinkedIn warriors use all these tech stacks that you never learn at school. There is one common fact about them: they can’t code. ",
              "That’s why I built this somewhat complex project with the most basic tech stack: the HCJ (HTML, CSS, JS) Stack. "
            ], 
            picture: "./images/"
        },     
        {
            name: "Sorting Algorithm Visualizer",
            website: "",
            location: "",
            tools: "HTML, CSS, JavaScript",
            date: "",
            summary: [
              "Visualized 5 CS sorting algorithms (quick, merge, selection, insertion, heap) on a web browser. "
            ],
            description: [
              "So many CS LinkedIn warriors use all these tech stacks that you never learn at school. There is one common fact about them: they can’t code. ",
              "That’s why I built this somewhat complex project with the most basic tech stack: the HCJ (HTML, CSS, JS) Stack. ",
              "Before I started coning this project, I thought there would be a sleep() type function like in Ardunio, where it pauses the entire program for a specified seconds. ",
              "I was planning on giving the bar a color, sleep the program, then remove the color of the bar to implement animation. ",
              "JavaScript didn’t have that function. ",
              "After hours of searching, I found this function called SetTimeout, which executes a function with a delay. ",
              "So I splatted the function into 2-3 parts. In the HeapSort function, I called the helper function inside of settimeout. ",
              "The helper function, when it was done, called the heap sort function again. ",
              "The process repeated until it ended. ",
              "I did similar stuff with other algorithms. "
            ], 
            picture: "./images/"
        },
        {
            name: "OSUing",
            website: "",
            location: "",
            tools: "Swift, Xcode",
            date: "",
            summary: [
              "An iOS application that reports live progress towards graduation for student at Ohio State."
            ],
            description: [
              "Inspired by Goondori, his is a graduation progress tracker app where it shows you live progress towards your graduation. ",
              "After you specify your starting and ending semester, this app algorithmically calculates your grade and days until the end of the current semester, current school year, and graduation. ",
              "When calculating, it also considers edge cases such as transfer students and students with gap semesters. ",
              "I was too lazy to learn how to use database systems, so I algorithmically implemented a nogada data saving feature in the frontend lmao. "
            ],
            picture: "./images/"
        },
        {
            name: "Egyptian Rat Screw (ERS)",
            website: "",
            location: "",
            tools: "Python, pygame",
            date: "",
            summary: [
              "Bulit a complex, multiplayer card game with a GUI and considered all possible 100+ scenarios. "
            ],
            description: [
              "I built this project during summer 2022. ",
              "I low-key regret doing this project; it took me a very long time to finish and it was algorithmically the most challenging project I’ve ever worked on, but when I have to explain it to someone, it’s just a Python game lol. ",
              "ERS is a card game that involves slapping, attacking, and defending, and there are lot of scenarios for slapping, slapping at the wrong time, defending, contiuning after a player dies during the round, player reviving, and a combination of everything. ",
              "Mostly OOP stuff with cards, table, players declared as classes + GUI stuff with pygame library. ",
              "This project is where my freshman software design classes clicked. "
            ], 
            picture: "./images/"
        },
        {
            name: "Gomoku",
            website: "",
            location: "",
            tools: "Python, pygame",
            date: "",
            summary: [
              "Built a multiplayer and singleplayer (vs a stupid AI) Gomoku and its GUI. "
            ],
            description: [
              "This project was my first time ever implementing a backend of a website. ",
              "I collaborated with Kledji Vrekaj, Riley Gilman, and Nick. ",
              "We used Ruby on Rails, Devise (a Ruby gem), and SQLite for backend. ",
              "It’s a very simple CRUD website that lets you login, choose your position, and CRUD reviews. " 
            ], 
            picture: "./images/"
        },
        {
            name: "Honors Fundamentals of Engineering II - Escape Room",
            website: "",
            location: "",
            tools: "Arduino, C++, Breadboard, SOLIDWORKS",
            date: "",
            summary: [
              "Designed and built a virtual escape room and all of its components. "
            ],
            description: [
              "For the 2nd semester of the FEH (Fundamentals of Engineering Honors) program, I collaborated with 3 other engineering majors to design and develop a virtual, Among Us themed escape room. ",
              "Throughout the semester, we: ",
              "- Came up with the theme of the escape room, overall story line, and clues ",
              "-	designed a very detailed room layout, using SOLIDWORKS ",
              "-	developed the logic of 4 simple games used in the room, using C++ and Ardunio ",
              "-	built the hardware of all games, using a breadboard and the Ardunio Kit ",
              "-	kept track of all of our plans, designs, and progresses, using Excel ",             
              "-	presented to 100+ audiences ",
              "It was a great project for freshmen since we gained exposure to all areas engineering and networked with many engineering students. ",
              "I really liked Ardunio because I can see the results in real life. "
            ],
            picture: "./images/"
        },
        {
          name: "Honors Fundamentals of Engineering I - Memory Matching Game",
          website: "",
          location: "",
          tools: "C++",
          date: "",
          summary: [
            "Built a memory matching game and a GUI with C++ for my final project."
          ],
          description: [
            "For the 1st semester of the FEH (Fundamentals of Engineering Honors) program, I collaborated with 2 other engineering majors to design and develop a memory tile game in C++. ",
            "The game was very simple lol. The user just has to repeat the randomly generated sequence on the screen by clicking. ",
            "Lots of OOP, functions, and GUI components. ",
            "We had to use Ohio State’s own GUI library for C++ and it was really cool to learn how to read documentations of a brand new library and connect it to the coding language I already knew. "
          ], 
          picture: "./images/"
        },
    ]

    var experiences = [];
    var descriptions = [];

    for (var i = 0; i < projectJson.length; i++) {
      var experience = projectJson[i];
  
      var summary = [];
  
      for (var acheivement of experience.summary) {
        summary.push(<div dangerouslySetInnerHTML={{ __html: "- " + acheivement }}/>);
      }
  
      experiences.push(
        <div className="experience">
          <div className="exp-row1">
            <div style={{ flex: 1 }}><b><a href={experience.website} target="_blank">{experience.name}</a></b></div>
          </div>
          <div className="exp-row2">
            <div id="tools" style={{ flex: 1 }}>{experience.tools}</div>
          </div>
          <div className="exp-row3">
            {summary}
          </div>
          <hr/>
        </div>
      );

      var description = "";

      for (var j = 0; j < experience.description.length; j++) {
        description += experience.description[j];
      }

      descriptions.push(
        <div>
          <h2 style={{textDecoration: "underline"}}>{experience.name}</h2>
          <div dangerouslySetInnerHTML={{ __html: description }}/>
        </div>
      );
    }

    return (
        <div className="container">
            <div className="top">
              <NavBar/>
            </div>

            <div className="content">
            <div>
                {experiences}
            </div>
            </div>
        </div>
    );
}