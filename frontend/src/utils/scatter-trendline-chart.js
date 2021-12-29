import React from "react";
import { Chart } from "react-google-charts";

export const options = {
  title: "Number of Shoes Sold vs Time",
  hAxis: { title: "Sold Dates" },
  vAxis: { title: "Number of Shoes Sold" },
  legend: "none",
  trendlines: { 0: {} },
};

export const data = [
  ["Diameter", "Age"],
  [8, 37],
  [4, 19.5],
  [11, 52],
  [4, 22],
  [3, 16.5],
  [6.5, 32.8],
  [14, 72],
];

export default function scatterChart(props) {
  console.log(props.data)

  return (
    <Chart
      chartType="ScatterChart"
      width="100%"
      height="400px"
      data={props.data}
      options={options}
    />
  );
}
