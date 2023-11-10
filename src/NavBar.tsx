import './App.css';
import {Link, Route, Routes, BrowserRouter } from 'react-router-dom';

export const NavBar = () => {

    return (
        <>
            <header className="header"><h2>Jay Shin</h2></header>
            <nav className="navbar">
            <ul className="navbar-list">
                <Link to ="/">
                    <li className="navbar-item">work</li>
                </Link>
            </ul>
            </nav>
        </>
    );
}