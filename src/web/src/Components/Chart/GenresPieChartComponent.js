import { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';


// Color code
const GENRES_COLOR_CODE = {
    "Action": "#ff0000",
    "Adventure": "#b03060",
    "Animation": "#dda0dd",
    "Biography": "#483d8b",
    "Comedy": "#adff2f",
    "Crime": "#8fbc8f",
    "Documentary": "#808000",
    "Drama": "#1e90ff",
    "Family": "#0000ff",
    "Fantasy": "#ff8c00",
    "Film-Noir": "#2f4f4f",
    "History": "#228b22",
    "Horror": "#800000",
    "Music": "#ffa07a",
    "Musical": "#ba55d3",
    "Mystery": "#00008b",
    "Romance": "#ff00ff",
    "Sci-Fi": "#ffd700",
    "Sport": "#00ff7f",
    "Thriller": "#00ffff",
    "War": "#87cefa",
    "Western": "#ffe4e1"
}

const GenresPieChartComponent = (prop) => {

    const [chartDataSet, setChartDataSet] = useState([]);

    useEffect(() => {
        try {
            let labelList = [];
            let backgroundColorList = [];
            let dataList = [];
            let result = prop.dataResult.filter(item => item.genre !== 'NA');;
            for (let key in result) {
                let item = result[key];
                dataList.push(item[prop.dataKey]);
                backgroundColorList.push(GENRES_COLOR_CODE[item[prop.labelKey]]);
                labelList.push(item[prop.labelKey]);
            }

            const data = {
                labels: labelList,
                datasets: [{
                    data: dataList,
                    backgroundColor: backgroundColorList,
                    hoverOffset: 4
                }]
            };
            setChartDataSet(data);
        } catch (err) {
            console.log(err)
        }
    }, [prop.dataResult, prop.dataKey, prop.labelKey]);


    return (
        <Box>
            <Typography variant="h5" component="div">
                {prop.chartTitle}
            </Typography>

            <Grid container spacing={2}>
                <Grid item lg={2} xl={3}></Grid>
                <Grid item xs={12} lg={8} xl={6}>
                    <Pie data={chartDataSet} />
                </Grid>
                <Grid item lg={2} xl={3}></Grid>
            </Grid>

            <Box sx={{ py: 3 }}>
                <Divider>
                </Divider>
            </Box>
        </Box>
    );
}

export default GenresPieChartComponent;