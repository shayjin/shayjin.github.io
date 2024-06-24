import './App.css';
import {Link, Route, Routes, BrowserRouter } from 'react-router-dom';

export const NavBar = () => {

    return (
        <>
            <header className="header">
                <Link to ="/"><h2>Jay Shin</h2></Link>
            </header>
            <nav className="navbar">
            <ul className="navbar-list">
                <Link to ="/">
                    <li className="navbar-item">home</li>
                </Link>
                <Link to ="/school">
                    <li className="navbar-item">school</li>
                </Link>
            </ul>
            </nav>
        </>
    );
}