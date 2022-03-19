import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
// import '../node_modules/react-vis/dist/style.css';
// import '../routes/node_modules/bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Navbar from './layout/Navbar';
import PieChart from './utils/pie-chart';
import GoogleBarGraph from './utils/google-bar-chart';
import Histogram from './utils/histogram';
import 'bootstrap/dist/css/bootstrap.min.css';


import { Link } from "react-router-dom";

export default function App() {
  return (
    <div>
      <Navbar />
      <h1>Landing Page</h1>
    </div>
  );
}