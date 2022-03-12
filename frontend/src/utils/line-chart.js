import React from "react";
import { Chart } from "react-google-charts";

const getFrequency = (yaxis, array) => {
  const map = {};
  array.forEach(item => {
     if(map[item]){
        map[item]++;
     }else{
        map[item] = 1;
     }
  });

  const temp = Object.keys(map);
  const sorted = temp.sort(function(a, b){
      return a - b;
    });

  
  const res = [["test", yaxis]]
  sorted.forEach(function (item, index) {
      res.push([item, map[item]]);
  });
  return res;
};

export default function LineChart(props) {
  const data = getFrequency(props.yaxis, props.value)

  return (
    <Chart
      chartType="LineChart"
      width="100%"
      height={props.height}
      data={data}
      options={{
        title: props.title,
        curveType: "function",
        legend: { position: "bottom" }
      }}
    />
  );
}
