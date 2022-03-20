import React, { useState, useEffect } from 'react';
import '../App.css';
import axios from 'axios';
// import '../../node_modules/react-vis/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Navbar from '../layout/Navbar';
// import PieChart from '../utils/pie-chart';
import GoogleBarGraph from '../utils/google-bar-chart';
import Histogram from '../utils/histogram';
// import Dropdown from 'react-bootstrap/Dropdown'
// import DropdownButton from 'react-bootstrap/DropdownButton'
// import ScatterChart from '../utils/scatter-trendline-chart';
import LineChart from '../utils/line-chart';


export default function EbayShoeAnalytics() {
  const [priceData, setPriceData] = React.useState([]);
  const [freeShippingData, setFreeShippingData] = React.useState([]);
  const [imagesData, setImagesData] = React.useState([]);

  const [shoeSizeData, setShoeSizeData] = React.useState([]);
  const [ageGroupData, setAgeGroupData] = React.useState([]);

  const [freScoreData, setFreScoreData] = React.useState([]);
  const [avgGradeScoreData, setAvgGradeScoreData] = React.useState([]);

  const [recentFeedbackData, setRecentFeedbackData] = React.useState([]);
  const [allJoinDateData, setAllJoinDateData] = React.useState([]);
  const [followersData, setFollowersData] = React.useState([]);
  const [followersBelow2000Data, setFollowersBelow2000Data] = React.useState([]);
  const [overallFeedbackData, setOverallFeedbackData] = React.useState([]);

  React.useEffect(() => {
    axios.get("/GetBulkSizeData").then((response) => {
      let shoeSize = [];
      let ageGroupStrings = [];

      for (let seller of response.data) {
        shoeSize.push(seller.shoe_size);
        if (seller.adult_shoe) {
          ageGroupStrings.push("Adult");
        } else if (seller.child_shoe) {
          ageGroupStrings.push("Child");
        } else if (seller.youth_shoe) {
          ageGroupStrings.push("Youth");
        }
      }
      setShoeSizeData(shoeSize);
      setAgeGroupData(ageGroupStrings);
    });

    axios.get("/GetBulkShoeListings").then((response) => {
      let price = []
      let free_shipping = []
      let images = []

      for (let shoeListing of response.data) {
        price.push(shoeListing.price);
        free_shipping.push(shoeListing.free_shipping);
        images.push(shoeListing.images);
      }
      setPriceData(price);
      setFreeShippingData(free_shipping);
      setImagesData(images);
    });

    axios.get("/GetBulkSellers").then((response) => {
      let recent_feedback = []
      let join_date = []
      let followers = []
      let followers_below_2000 = []
      let overall_feedback = []

      for (let seller of response.data) {
        let recent_feedback_total = seller.positive + seller.neutral + seller.negative;
        recent_feedback.push(Math.round((seller.positive/recent_feedback_total)*100));
       
        let date = new Date(seller.join_date);
        join_date.push(date.getFullYear());

        if (seller.followers < 2000) {
          followers_below_2000.push(seller.followers);
        }
        followers.push(seller.followers);

        overall_feedback.push(seller.positive_feedback);
      }
      setRecentFeedbackData(recent_feedback);
      setAllJoinDateData(join_date);
      setFollowersData(followers);
      setOverallFeedbackData(overall_feedback);
      setFollowersBelow2000Data(followers_below_2000);
    });

    axios.get("/GetDescData").then((response) => {
      let fre_score = []
      let avg_grade_score = []

      for (let desc of response.data) {
        fre_score.push(desc.fre_score);
        avg_grade_score.push(desc.avg_grade_score);
      }
      setFreScoreData(fre_score);
      setAvgGradeScoreData(avg_grade_score);
    });
    
  }, []);

  return (
    <div>
      <Navbar />
      <Container>
        <Row>
          <h2>General Shoe Listing Graphs</h2>
          <Col>
            <Histogram value={priceData}
                        title={"Shoe Prices"}
                        width={"400px"}
                        height={"300px"}/>
          </Col>
          <Col>
            <GoogleBarGraph value={freeShippingData}
                            title={"Free Shipping Offered"}
                            xaxis={"Free Shipping"}
                            yaxis={"Frequency"}
                            width={'200px'}
                            height={'300px'}/>
          </Col>
          <Col>
            <GoogleBarGraph value={imagesData}
                            title={"Number of Images on a Shoe Listing"}
                            xaxis={"Number of Images"}
                            yaxis={"Frequency"}
                            width={'300px'}
                            height={'300px'}/>
          </Col>
        </Row>

        <h2>Shoe Size Graphs</h2>
        <Row>
          <Col>
            <GoogleBarGraph value={shoeSizeData}
                            title={"Shoe Sizes"}
                            xaxis={"Shoe Size"}
                            yaxis={"Frequency"}
                            width={'800px'}
                            height={'300px'}/>
          </Col>
          <Col>
            <GoogleBarGraph value={ageGroupData}
                            title={"Age Group for Shoes"}
                            xaxis={"Age Group"}
                            yaxis={"Frequency"}
                            width={'300px'}
                            height={'300px'}/>
          </Col>
        </Row>

        <h2>Item Description Readability Graphs</h2>
        <Row>
          <Col>
            <Histogram value={freScoreData}
                        title={"FRE Scores of Shoe Listing Descriptions"}
                        width={"600px"}
                        height={"300px"}/>
          </Col>
          <Col>
            <Histogram value={avgGradeScoreData}
                        title={"Average Readability of Shoe Listing Descriptions"}
                        width={"600px"}
                        height={"300px"}/>
          </Col>
        </Row>

        <h2>Seller Graphs</h2>
        <Row>
          <Col>
            <Histogram value={followersData}
                        title={"Seller Followers"}
                        width={"300px"}
                        height={"300px"}/>
          </Col>
          <Col>
            <Histogram value={followersBelow2000Data}
                        title={"Seller Followers Below 2000"}
                        width={"300px"}
                        height={"300px"}/>
          </Col>
          <Col>
            <Histogram value={overallFeedbackData}
                        title={"Overall Positive Feedback"}
                        width={"300px"}
                        height={"300px"}/>
          </Col>
          <Col>
            <Histogram value={recentFeedbackData}
                        title={"Positive Feedback for the Past Year"}
                        width={"300px"}
                        height={"300px"}/>
          </Col>
        </Row>
        <Row>
          <Col>
            <LineChart value={allJoinDateData}
                      title={"Frequency of Ebay Join-Dates for Shoe Resellers"}
                      width={"300px"}
                      height={"400px"}
                      yaxis={"Frequency"}/>
          </Col>
        </Row>

        
      </Container>
    </div>
  );
}
