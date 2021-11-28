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

import PieChart from './utils/pie-chart'
import BarGraph from './utils/bar-chart';
import Navbar from './layout/Navbar'
import GoogleBarGraph from './utils/google-bar-chart'

const baseURL = "/shoe/size/9";

export default function App() {
  const [shoeSizes, setShoeSizes] = React.useState([]); // for child comp
  const [freeShipping, setFreeShipping] = React.useState([]);
  const [itemOffer, setItemOffer] = React.useState([]);
  const [itemBid, setItemBid] = React.useState([]);
  const [totalImages, setTotalImages] = React.useState([]);


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

      {/* <XYPlot width={300} height={300}>
      <HorizontalGridLines style={{stroke: '#B7E9ED'}} />
      <VerticalGridLines style={{stroke: '#B7E9ED'}} />
      <XAxis
        title="X Axis"
        style={{
          line: {stroke: '#ADDDE1'},
          ticks: {stroke: '#ADDDE1'},
          text: {stroke: 'none', fill: '#6b6b76', fontWeight: 600}
        }}
      />
      <YAxis title="Y Axis" />
      <LineSeries
        className="first-series"
        data={[{x: 1, y: 3}, {x: 2, y: 5}, {x: 3, y: 15}, {x: 4, y: 12}]}
        style={{
          strokeLinejoin: 'round',
          strokeWidth: 4
        }}
      />
      <LineSeries className="second-series" data={null} />
      <LineSeries
        className="third-series"
        curve={'curveMonotoneX'}
        data={[{x: 1, y: 10}, {x: 2, y: 4}, {x: 3, y: 2}, {x: 4, y: 15}]}
        strokeDasharray="7, 3"
      />
      <LineSeries
        className="fourth-series"
        curve={curveCatmullRom.alpha(0.5)}
        data={[{x: 1, y: 7}, {x: 2, y: 11}, {x: 3, y: 9}, {x: 4, y: 2}]}
      />
    </XYPlot>

    <XYPlot xType="ordinal" width={300} height={300} xDistance={100}>
          <VerticalGridLines />
          <HorizontalGridLines />
          <XAxis />
          <YAxis />
          <VerticalBarSeries className="vertical-bar-series-example" data={greenData} />
          <VerticalBarSeries data={blueData} />
          <LabelSeries data={labelData} getLabel={d => d.x} />
        </XYPlot> */}



      {/* <BarGraph parentToChild={shoeSizes}/>
      <BarGraph parentToChild={shoeSizes}/>
      <BarGraph parentToChild={shoeSizes}/> */}

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
      </Container>

      {/* <ul>{listItems}</ul> */}
    </div>
  );
}
