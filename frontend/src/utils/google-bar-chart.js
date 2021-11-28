
import React from 'react';
import '../../node_modules/react-vis/dist/style.css';
import { Chart } from "react-google-charts";

const getFrequency = (array) => {
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

    
    const res = [["test", "test2"]]
    sorted.forEach(function (item, index) {
        res.push([item, map[item]]);
    });
    return res;
 };

export default function GoogleBarChart(props) {
    const data = getFrequency(props.value)

    return (
        <div>
            <Chart
                width={props.width}
                height={props.height}
                chartType="ColumnChart"
                loader={<div>Loading Chart</div>}
                data={data}
                options={{
                    title: props.title,
                    chartArea: { width: '80%' },
                    hAxis: {
                    title: props.xaxis,
                    minValue: 0,
                    },
                    vAxis: {
                    title: props.yaxis,
                    },
                }}
                // For tests
                rootProps={{ 'data-testid': '1' }}
            />
        </div>
    );
}
