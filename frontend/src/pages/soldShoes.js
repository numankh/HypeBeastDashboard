import React, { useState, useEffect } from 'react';
import '../App.css';
import axios from 'axios';
// import '../../node_modules/react-vis/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Navbar from '../layout/Navbar';
import LineChart from '../utils/line-chart';
import ScatterChart from '../utils/scatter-trendline-chart';
import PieChart from '../utils/pie-chart';
import GoogleBarGraph from '../utils/google-bar-chart';
import Histogram from '../utils/histogram';


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
  const [shoeSizes, setShoeSizes] = React.useState([]);
  const [soldDates, setSoldDates] = React.useState([]);
  const [freeShipping, setFreeShipping] = React.useState([]);
  const [totalImages, setTotalImages] = React.useState([]);
  const [shoePrices, setShoePrices] = React.useState([]);
  const [sellerRatings, setSellerRatings] = React.useState([]);
  const [freScores, setFreScores] = React.useState([]);
  const [gradeScores, setGradeScores] = React.useState([]);
  
  React.useEffect(() => {
    axios.get("/size/adult?sold=True").then((response) => {
      setShoeSizes(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/sold_dates").then((response) => {
      setSoldDates(getFrequency(response.data));
    });
  }, []);

  React.useEffect(() => {
    axios.get("/free_shipping?sold=True").then((response) => {
      setFreeShipping(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/total_item_images?sold=True").then((response) => {
      setTotalImages(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/price?sold=True").then((response) => {
      setShoePrices(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/seller_rating?sold=True").then((response) => {
      setSellerRatings(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/item_description/fre_score?sold=True").then((response) => {
      setFreScores(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/item_description/avg_grade_score?sold=True").then((response) => {
      setGradeScores(response.data);
    });
  }, []);

  return (
    <div>
      <Navbar />

      <Container>
        <Row>
          <Col>
            <ScatterChart data={soldDates}/>
          </Col>
          <Col>
            <PieChart value={freeShipping}
                      title={"Free Shipping Offered"}
                      feature1={"Free Shipping"}
                      feature2={"No Free Shipping"}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <GoogleBarGraph value={totalImages}
                            title={"Total Seller Provided Item Images"}
                            xaxis={"Total Images"}
                            yaxis={"Frequency"}
                            width={'400px'}
                            height={'500px'}/>
          </Col>
          <Col>
            <GoogleBarGraph value={shoeSizes}
                            title={"Distribution of Adult Shoe Size"}
                            xaxis={"Adult Shoe Size"}
                            yaxis={"Frequency"}
                            width={'800px'}
                            height={'500px'}/>
          </Col>

        </Row>
        <Row>
          <Col>
            <Histogram value={shoePrices}
                       title={"Shoe Prices"}
                       width={"800px"}
                       height={"500px"}/>
          </Col>
          <Col>
            <Histogram value={sellerRatings}
                       title={"Seller Ratings"}
                       width={"800px"}
                       height={"500px"}/>
          </Col>
        </Row>
        <Row>
          <Col>
            <Histogram value={freScores}
                       title={"Flesch Reading Ease Scores for Shoe Descriptions (complex descriptions have low scores)"}
                       width={"800px"}
                       height={"500px"}/>
          </Col>
          <Col>
            <Histogram value={gradeScores}
                       title={"Average Grade Readability Scores for Shoe Descriptions (complex descriptions have high scores)"}
                       width={"800px"}
                       height={"500px"}/>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
