import { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import Slider from '@mui/material/Slider';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';

// Color code
// Dark Red=139,0,0
// Dark Green=21,71,52
// Dark Yellow=218,165,32
// Dark Purple=48,25,52
// Dark Blue=2,7,93

function valuetext(value) {
    return `${value}`;
}

const YearBarChartComponent = (prop) => {

    const [chartDataSet, setChartDataSet] = useState([]);
    const chartOption = {
        parsing: {
            xAxisKey: prop.xAxisKey,
            yAxisKey: prop.yAxisKey,
        },
        plugins: {
            title: {
                display: true,
                position: 'bottom',
                text: prop.xAxis
            }
        }
    }
    const [chartOptions] = useState(chartOption);
    const [chartKey, setChartKey] = useState(1);

    const minDistance = 20;
    const yearRangeMin = 1950;
    const yearRangeMax = (new Date()).getFullYear() - 1;
    const [yearRange, setYearRange] = useState([yearRangeMin, yearRangeMax]);
    const [yearRangeCommitted, setYearRangeCommitted] = useState([yearRangeMin, yearRangeMax]);

    useEffect(() => {
        try {
            let result = prop.dataResult;
            if (result !== undefined) {
                result = result.filter(item => item.year >= yearRangeCommitted[0] && item.year <= yearRangeCommitted[1]);
            }
            let resultDataSet = {
                datasets: [
                    {
                        label: prop.yAxis,
                        data: result,
                        backgroundColor: 'rgb(' + prop.chartRgbColor + ')',
                        borderColor: 'rgba(' + prop.chartRgbColor + ', 0.2)',
                    },
                ],
            };
            setChartDataSet(resultDataSet);
            setChartKey(Math.random());
        } catch (err) {
            console.log(err)
        }
    }, [prop.dataResult, yearRangeCommitted, prop.chartRgbColor, prop.yAxis]);

    const handleYearRangeChange = (event, newValue, activeThumb) => {

        if (!Array.isArray(newValue)) {
            return;
        }
        if (newValue[1] - newValue[0] < minDistance) {
            if (activeThumb === 0) {
                const clamped = Math.min(newValue[0], yearRangeMax - minDistance);
                setYearRange([clamped, clamped + minDistance]);
            } else {
                if (newValue[0] !== yearRangeMin && newValue[1] >= yearRangeMin + minDistance) {
                    const clamped = Math.max(newValue[1], minDistance);
                    setYearRange([clamped - minDistance, clamped]);
                }
            }
        } else {
            setYearRange(newValue);
        }
    };

    const handleYearRangeChangeCommitted = (event) => {
        setYearRangeCommitted(yearRange);
    };

    return (
        <Box>
            <Typography variant="h5" component="div">
                {prop.chartTitle}
            </Typography>
            <Box sx={{ mx: 3, mt: 5 }}>
                <Slider
                    getAriaLabel={() => 'Year Range'}
                    max={yearRangeMax}
                    min={yearRangeMin}
                    value={yearRange}
                    onChange={handleYearRangeChange}
                    onChangeCommitted={handleYearRangeChangeCommitted}
                    valueLabelDisplay="on"
                    getAriaValueText={valuetext}
                    disableSwap
                />
            </Box>
            <Bar key={chartKey} data={chartDataSet} options={chartOptions} />
            <Box sx={{ py: 3 }}>
                <Divider>
                </Divider>
            </Box>
        </Box>
    );
}

export default YearBarChartComponent;