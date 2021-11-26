
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
    
    const res = [["test", "test2"]]
    for (const [ key, value ] of Object.entries(map)) {
        res.push([key, value])
    }
    return res;
 };

export default function GoogleBarChart(props) {
    const data = getFrequency(props.value)

    return (
        <div>
            <Chart
                width={'500px'}
                height={'600px'}
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
