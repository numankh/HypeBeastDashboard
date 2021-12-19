import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import '../node_modules/react-vis/dist/style.css';
// import '../routes/node_modules/bootstrap/dist/css/bootstrap.min.css';
import {Container, Row, Col} from 'react-bootstrap';
import Navbar from './layout/Navbar';
import PieChart from './utils/pie-chart';
import GoogleBarGraph from './utils/google-bar-chart';
import Histogram from './utils/histogram';


import { Link } from "react-router-dom";

export default function App() {
  return (
    <div>
      <Navbar />
      <h1>Landing Page</h1>
      {/* <nav
        style={{
          borderBottom: "solid 1px",
          paddingBottom: "1rem"
        }}
      >
        <Link to="/invoices">Invoices</Link> |{" "}
        <Link to="/expenses">Expenses</Link>
      </nav> */}
    </div>
  );
}

// export default function App() {
//   // const [shoeSizes, setShoeSizes] = React.useState([]); // for child comp
//   // const [freeShipping, setFreeShipping] = React.useState([]);
//   // const [itemOffer, setItemOffer] = React.useState([]);
//   // const [itemBid, setItemBid] = React.useState([]);
//   // const [totalImages, setTotalImages] = React.useState([]);
//   // const [shoePrices, setShoePrices] = React.useState([]);
//   // const [sellerRatings, setSellerRatings] = React.useState([]);
//   // const [freScores, setFreScores] = React.useState([]);
//   // const [gradeScores, setGradeScores] = React.useState([]);

//   // React.useEffect(() => {
//   //   axios.get("/size/adult").then((response) => {
//   //     setShoeSizes(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/free_shipping").then((response) => {
//   //     setFreeShipping(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/item_offer").then((response) => {
//   //     setItemOffer(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/item_bid").then((response) => {
//   //     setItemBid(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/total_item_images").then((response) => {
//   //     setTotalImages(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/price").then((response) => {
//   //     setShoePrices(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/seller_rating").then((response) => {
//   //     setSellerRatings(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/item_description/fre_score").then((response) => {
//   //     setFreScores(response.data);
//   //   });
//   // }, []);

//   // React.useEffect(() => {
//   //   axios.get("/item_description/avg_grade_score").then((response) => {
//   //     setGradeScores(response.data);
//   //   });
//   // }, []);


//   return (
//     <div>
//       {/* <Navbar /> */}
//       <h1>WHATS UP DUDE</h1>

//       {/* <Container>
//         <Row>
//           <Col>
//             <PieChart value={freeShipping}
//                       title={"Free Shipping Offered"}
//                       feature1={"Free Shipping"}
//                       feature2={"No Free Shipping"}
//             />
//           </Col>
//           <Col>
//             <PieChart value={itemOffer}
//                       title={"Item Offer Provided"}
//                       feature1={"Item Offer"}
//                       feature2={"No Item Offer"}
//             />
//           </Col>
//           <Col>
//             <PieChart value={itemBid}
//                       title={"Item Bid Provided"}
//                       feature1={"Item Bid"}
//                       feature2={"No Item Bid"}
//             />
//           </Col>
//         </Row>
//         <Row>
//           <Col>
//             <GoogleBarGraph value={totalImages}
//                             title={"Total Seller Provided Item Images"}
//                             xaxis={"Total Images"}
//                             yaxis={"Frequency"}
//                             width={'400px'}
//                             height={'500px'}/>
//           </Col>
//           <Col>
//             <GoogleBarGraph value={shoeSizes}
//                             title={"Distribution of Adult Shoe Size"}
//                             xaxis={"Adult Shoe Size"}
//                             yaxis={"Frequency"}
//                             width={'800px'}
//                             height={'500px'}/>
//           </Col>

//         </Row>
//         <Row>
//           <Col>
//             <Histogram value={shoePrices}
//                        title={"Shoe Prices"}
//                        width={"800px"}
//                        height={"500px"}/>
//           </Col>
//           <Col>
//             <Histogram value={sellerRatings}
//                        title={"Seller Ratings"}
//                        width={"800px"}
//                        height={"500px"}/>
//           </Col>
//         </Row>
//         <Row>
//           <Col>
//             <Histogram value={freScores}
//                        title={"Flesch Reading Ease Scores for Shoe Descriptions (complex descriptions have low scores)"}
//                        width={"800px"}
//                        height={"500px"}/>
//           </Col>
//           <Col>
//             <Histogram value={gradeScores}
//                        title={"Average Grade Readability Scores for Shoe Descriptions (complex descriptions have high scores)"}
//                        width={"800px"}
//                        height={"500px"}/>
//           </Col>
//         </Row>
//       </Container> */}
//     </div>
//   );
// }
