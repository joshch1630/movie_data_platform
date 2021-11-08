import { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';


// Color code
// Dark Red=139,0,0
// Dark Green=21,71,52
// Dark Yellow=218,165,32
// Dark Purple=48,25,52
// Dark Blue=2,7,93

const RatingBarChartComponent = (prop) => {

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
    const [numOfNoRating, setNumOfNoRating] = useState('...');

    useEffect(() => {
        try {
            let noRatingResult;
            let result;
            if (prop.dataResult !== undefined) {
                noRatingResult = prop.dataResult.filter(item => item.rating === 'NA');
                result = prop.dataResult.filter(item => item.rating !== 'NA');
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
            setNumOfNoRating(noRatingResult[0].movie_count);
            setChartDataSet(resultDataSet);
        } catch (err) {
            console.log(err)
        }
    }, [prop.dataResult, prop.chartRgbColor, prop.yAxis]);


    return (
        <Box>
            <Typography variant="h5" component="span">
                {prop.chartTitle}
            </Typography>

            <Bar data={chartDataSet} options={chartOptions} />
            {prop.yAxisKey === 'movie_count'
                ? <Typography component="span">
                    There are {numOfNoRating} movies with no rating result.
                </Typography>
                : <Typography component="span">
                    There are {numOfNoRating} movies with no voting.
                </Typography>}
            <Box sx={{ py: 3 }}>
                <Divider>
                </Divider>
            </Box>
        </Box>
    );
}

export default RatingBarChartComponent;