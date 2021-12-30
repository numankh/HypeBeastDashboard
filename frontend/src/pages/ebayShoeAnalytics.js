import React, { useState, useEffect } from 'react';
import '../App.css';
import axios from 'axios';
// import '../../node_modules/react-vis/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Navbar from '../layout/Navbar';
import PieChart from '../utils/pie-chart';
import GoogleBarGraph from '../utils/google-bar-chart';
import Histogram from '../utils/histogram';
import Dropdown from 'react-bootstrap/Dropdown'
import DropdownButton from 'react-bootstrap/DropdownButton'

class DataVizType {
  static ALL = new DataVizType("all")
  static SOLD = new DataVizType("sold")
  static NOTSOLD = new DataVizType("notsold")

  constructor(name) {
    this.name = name
  }
}

export default function EbayShoeAnalytics() {
  const [shoeSizes, setShoeSizes] = React.useState([]); // for child comp
  const [freeShipping, setFreeShipping] = React.useState([]);
  const [itemOffer, setItemOffer] = React.useState([]);
  const [itemBid, setItemBid] = React.useState([]);
  const [totalImages, setTotalImages] = React.useState([]);
  const [shoePrices, setShoePrices] = React.useState([]);
  const [sellerRatings, setSellerRatings] = React.useState([]);
  const [freScores, setFreScores] = React.useState([]);
  const [gradeScores, setGradeScores] = React.useState([]);

  const [dataVizType, setDataVizType] = React.useState(DataVizType.ALL);

  React.useEffect(() => {
    if (dataVizType === DataVizType.ALL) {
      axios.get("/size/adult").then((response) => {
        setShoeSizes(response.data);
      });
      axios.get("/free_shipping").then((response) => {
        setFreeShipping(response.data);
      });
      axios.get("/item_offer").then((response) => {
        setItemOffer(response.data);
      });
      axios.get("/item_bid").then((response) => {
        setItemBid(response.data);
      });
      axios.get("/total_item_images").then((response) => {
        setTotalImages(response.data);
      });
      axios.get("/price").then((response) => {
        setShoePrices(response.data);
      });
      axios.get("/seller_rating").then((response) => {
        setSellerRatings(response.data);
      });
      axios.get("/item_description/fre_score").then((response) => {
        setFreScores(response.data);
      });
      axios.get("/item_description/avg_grade_score").then((response) => {
        setGradeScores(response.data);
      });
    } else if (dataVizType === DataVizType.SOLD) {
      axios.get("/size/adult?sold=True").then((response) => {
        setShoeSizes(response.data);
      });
      axios.get("/free_shipping?sold=True").then((response) => {
        setFreeShipping(response.data);
      });

      setItemOffer([]);
      setItemBid([]);
     
      axios.get("/total_item_images?sold=True").then((response) => {
        setTotalImages(response.data);
      });
      axios.get("/price?sold=True").then((response) => {
        setShoePrices(response.data);
      });
      axios.get("/seller_rating?sold=True").then((response) => {
        setSellerRatings(response.data);
      });
      axios.get("/item_description/fre_score?sold=True").then((response) => {
        setFreScores(response.data);
      });
      axios.get("/item_description/avg_grade_score?sold=True").then((response) => {
        setGradeScores(response.data);
      });
    } else {
      axios.get("/size/adult?sold=False").then((response) => {
        setShoeSizes(response.data);
      });
      axios.get("/free_shipping?sold=False").then((response) => {
        setFreeShipping(response.data);
      });
      axios.get("/item_offer?sold=False").then((response) => {
        setItemOffer(response.data);
      });
      axios.get("/item_bid?sold=False").then((response) => {
        setItemBid(response.data);
      });
      axios.get("/total_item_images?sold=False").then((response) => {
        setTotalImages(response.data);
      });
      axios.get("/price?sold=False").then((response) => {
        setShoePrices(response.data);
      });
      axios.get("/seller_rating?sold=False").then((response) => {
        setSellerRatings(response.data);
      });
      axios.get("/item_description/fre_score?sold=False").then((response) => {
        setFreScores(response.data);
      });
      axios.get("/item_description/avg_grade_score?sold=False").then((response) => {
        setGradeScores(response.data);
      });
    }
  }, [dataVizType]);


  return (
    <div>
      <Navbar />

      <DropdownButton id="dropdown-basic-button" title="Dropdown button">
        <Dropdown.Item onClick={() => setDataVizType(DataVizType.ALL)}>All Shoes</Dropdown.Item>
        <Dropdown.Item onClick={() => setDataVizType(DataVizType.NOTSOLD)}>Not sold Shoes</Dropdown.Item>
        <Dropdown.Item onClick={() => setDataVizType(DataVizType.SOLD)}>Sold Shoes</Dropdown.Item>
      </DropdownButton>

      <Container>
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
