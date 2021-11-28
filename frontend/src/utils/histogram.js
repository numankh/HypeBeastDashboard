
import React from 'react';
import '../../node_modules/react-vis/dist/style.css';
import { Chart } from "react-google-charts";

const formatData = (array) => {
    const res = [["EmptyString", "Value"]]
    array.forEach(item => {
        res.push(["", item]);
    });

    console.log(res)
    return res;
 };

export default function Histogram(props) {
    const data = formatData(props.value)

    return (
        <div>
            <Chart
                width={'500px'}
                height={'300px'}
                chartType="Histogram"
                loader={<div>Loading Chart</div>}
                data={data}
                options={{
                    title: props.title,
                    legend: { position: 'none' },
                    colors: ['green'],
                }}
                rootProps={{ 'data-testid': '2' }}
            />
        </div>
    );
}
