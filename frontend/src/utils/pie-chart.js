
import React from 'react';
import '../../node_modules/react-vis/dist/style.css';
import { Chart } from "react-google-charts";

export default function PieChart(props) {
    let tot_free_shipping = 0;
    let tot_not_free_shipping = 0;

    props.value.forEach(function (item, index) {
        if(item) {
            tot_free_shipping += 1;
        } else {
            tot_not_free_shipping += 1;
        }
    });

    return (
        <div>
            <Chart
                width={'400px'}
                height={'300px'}
                chartType="PieChart"
                loader={<div>Loading Chart</div>}
                data={[
                    ['Task', 'Hours per Day'],
                    [props.feature1, tot_free_shipping],
                    [props.feature2, tot_not_free_shipping],
                ]}
                options={{
                    title: props.title,
                }}
                rootProps={{ 'data-testid': '1' }}
            />
        </div>
    );
}
