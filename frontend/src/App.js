import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import '../node_modules/react-vis/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {XYPlot,
        LineSeries,
        VerticalGridLines,
        HorizontalGridLines,
        XAxis,
        YAxis,
        VerticalBarSeries} from 'react-vis';
import {curveCatmullRom} from 'd3-shape';
import {Container, Row, Col} from 'react-bootstrap';
import Navbar from './layout/Navbar';
import PieChart from './utils/pie-chart';
import GoogleBarGraph from './utils/google-bar-chart';
import Histogram from './utils/histogram';

const baseURL = "/shoe/size/9";

export default function App() {
  const [shoeSizes, setShoeSizes] = React.useState([]); // for child comp
  const [freeShipping, setFreeShipping] = React.useState([]);
  const [itemOffer, setItemOffer] = React.useState([]);
  const [itemBid, setItemBid] = React.useState([]);
  const [totalImages, setTotalImages] = React.useState([]);
  const [shoePrices, setShoePrices] = React.useState([]);
  const [sellerRatings, setSellerRatings] = React.useState([]);
  const [freScores, setFreScores] = React.useState([]);
  const [gradeScores, setGradeScores] = React.useState([]);



  const data = [
    {x: 0, y: 8},
    {x: 1, y: 5},
    {x: 2, y: 4},
    {x: 3, y: 9},
    {x: 4, y: 1},
    {x: 5, y: 7},
    {x: 6, y: 6},
    {x: 7, y: 3},
    {x: 8, y: 2},
    {x: 9, y: 0}
  ];

  const greenData = [{x: 'A', y: 10}, {x: 'B', y: 5}, {x: 'C', y: 15}];

  const blueData = [{x: 'A', y: 12}, {x: 'B', y: 2}, {x: 'C', y: 11}];

  const labelData = greenData.map((d, idx) => ({
    x: d.x,
    y: Math.max(greenData[idx].y, blueData[idx].y)
  }));


  React.useEffect(() => {
    axios.get("/size/adult").then((response) => {
      setShoeSizes(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/free_shipping").then((response) => {
      setFreeShipping(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/item_offer").then((response) => {
      setItemOffer(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/item_bid").then((response) => {
      setItemBid(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/total_item_images").then((response) => {
      setTotalImages(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/price").then((response) => {
      setShoePrices(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/seller_rating").then((response) => {
      setSellerRatings(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/item_description/fre_score").then((response) => {
      setFreScores(response.data);
    });
  }, []);

  React.useEffect(() => {
    axios.get("/item_description/avg_grade_score").then((response) => {
      setGradeScores(response.data);
    });
  }, []);


  // if (!shoes) return null;

  // const listItems = shoes.map((shoe) =>
  //   <div>
  //     <p>{shoe.name}</p>
  //     <p>{shoe.item_description}</p>
  //     <p>{shoe.url}</p>
  //     <p>---------------------------------</p>
  //   </div>
  // );

  return (
    <div>
      <Navbar />

      <Container>
        {/* <Row>
          <Col>
            <BarGraph parentToChild={shoeSizes}/>
          </Col>
          <Col>
            <BarGraph parentToChild={shoeSizes}/>
          </Col>
        </Row> */}
        <Row>
          <Col>
            <PieChart value={freeShipping}
                      title={"Free Shipping Offered"}
                      feature1={"Free Shipping"}
                      feature2={"No Free Shipping"}
            />
          </Col>
          <Col>
            <PieChart value={itemOffer}
                      title={"Item Offer Provided"}
                      feature1={"Item Offer"}
                      feature2={"No Item Offer"}
            />
          </Col>
          <Col>
            <PieChart value={itemBid}
                      title={"Item Bid Provided"}
                      feature1={"Item Bid"}
                      feature2={"No Item Bid"}
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

      {/* <ul>{listItems}</ul> */}
    </div>
  );
}
