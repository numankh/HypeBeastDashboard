import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../../node_modules/react-vis/dist/style.css';
import {XYPlot,
        VerticalGridLines,
        HorizontalGridLines,
        XAxis,
        YAxis,
        VerticalBarSeries} from 'react-vis';


function Test(props) {
    const res = [];
    for (const [ key, value ] of Object.entries(props.value)) {
        let dict = {
            x: key,
            y: value
        };
        res.push(dict)
    }
    
    return(
        <XYPlot xType="ordinal" width={600} height={300} xDistance={300}>
            <VerticalGridLines />
            <HorizontalGridLines />
            <XAxis />
            <YAxis />
            <VerticalBarSeries className="vertical-bar-series-example" data={res} />
        </XYPlot>
    );
}

export default function BarGraph({parentToChild}) {
  return (
    <div>
        <Test value={parentToChild}/>
    </div>
  );
}
