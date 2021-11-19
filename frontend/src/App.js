import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

const baseURL = "/shoe/size/9";

export default function App() {
  const [shoes, setShoes] = React.useState([]);

  React.useEffect(() => {
    axios.get(baseURL).then((response) => {
      setShoes(response.data);
    });
  }, []);

  if (!shoes) return null;

  const listItems = shoes.map((shoe) =>
    <div>
      <p>{shoe.name}</p>
      <p>{shoe.item_description}</p>
      <p>{shoe.url}</p>
      <p>---------------------------------</p>
    </div>
  );

  return (
    <div>
      <ul>{listItems}</ul>
    </div>
  );
}
