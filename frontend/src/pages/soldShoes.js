import React, { useState, useEffect } from 'react';
import '../App.css';
import axios from 'axios';
// import '../../node_modules/react-vis/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Navbar from '../layout/Navbar';
import LineChart from '../utils/line-chart';
import ScatterChart from '../utils/scatter-trendline-chart';



function getFrequency(arr) {
  const res = {};
  const dates = new Set();
  for (const num of arr) {
    const d = new Date(num);
    const month = (d.getMonth()).toString();
    const day = (d.getDate()).toString();
    const key = month + "/" + day;
    dates.add(key);
    if (res[key]) {
      res[key] = res[key] + 1;
    } else {
      res[key] = 1;
    }
  }

  const myIterator = dates.values();
  const finalDates = new Set();
  let text = "";
  for (const entry of myIterator) {
    text += entry + ",";

    let index = entry.indexOf('/');
    let month = entry.substring(0,index);
    let day = entry.substring(index+1);
    finalDates.add(new Date(2021,month,day));
  }

  let output = [];
  for (const entry of finalDates) {
    output.push(entry);
  }
  output.sort((date1, date2) => date1 - date2);
  
  const res2 = [["Date","Frequency"]]
  for (let key of output) {
    let formattedKey = key.getMonth() + "/" + key.getDate();
    let temp = [formattedKey, res[formattedKey]];
    res2.push(temp);
  }
  return res2;
}

export default function SoldShoes() {
  const [soldDates, setSoldDates] = React.useState();
  
  React.useEffect(() => {
    axios.get("/sold_dates").then((response) => {
      // (response.data);
      setSoldDates(getFrequency(response.data));
    });
  }, []);

  return (
    <div>
      <Navbar />

      <Container>
        <Row>
          {/* <Col>
            <LineChart />
          </Col> */}
          <Col>
            <ScatterChart data={soldDates}/>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
