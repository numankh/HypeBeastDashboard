import React from "react";
import { Chart } from "react-google-charts";

export const options = {
  title: "Number of Shoes Sold vs Time",
  hAxis: { title: "Sold Dates" },
  vAxis: { title: "Number of Shoes Sold" },
  legend: "none",
  trendlines: { 0: {} },
};

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
