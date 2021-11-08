
import { useState, useEffect } from 'react';
import ReactGA from 'react-ga';
import DataService from '../Service/DataApiService';
import YearBarChartComponent from "./Chart/YearBarChartComponent";
import CommentComponent from "./CommentComponent";
import LinearProgress from '@mui/material/LinearProgress';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import PropTypes from 'prop-types';
import RatingBarChartComponent from './Chart/RatingBarChartComponent';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Grid from '@mui/material/Grid';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import GenresPieChartComponent from './Chart/GenresPieChartComponent';


function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <Box
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3, pt: 0 }}>
                    <Typography component="span">{children}</Typography>
                </Box>
            )}
        </Box>
    );
}

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
};

const MovieLensAnalysisComponent = () => {
    const [tabValue, setTabValue] = useState(0);
    const [isLoaded, setIsLoaded] = useState(false);
    const [dataResult, setDataResult] = useState();

    // Filter
    const [yearWIthRating, setYearWIthRating] = useState('');
    const handleYearWithRatingChange = (event) => {
        setYearWIthRating(event.target.value);

        let defaultValue = "movie_lens_by_year";
        setYearWIthGenres(defaultValue);
        setYearWIthAdult(defaultValue);

        getChartData(event.target.value)
    };

    const [yearWIthGenres, setYearWIthGenres] = useState('');
    const handleYearWithGenresChange = (event) => {
        setYearWIthGenres(event.target.value);

        let defaultValue = "movie_lens_by_year";
        setYearWIthRating(defaultValue);
        setYearWIthAdult(defaultValue);

        getChartData(event.target.value)
    };

    const [yearWIthAdult, setYearWIthAdult] = useState('');
    const handleYearWithAdultChange = (event) => {
        setYearWIthAdult(event.target.value);

        let defaultValue = "movie_lens_by_year";
        setYearWIthRating(defaultValue);
        setYearWIthGenres(defaultValue);

        getChartData(event.target.value)
    };

    const [ratingWIthGenres, setRatingWIthGenres] = useState('');
    const handleRatingWithGenresChange = (event) => {
        setRatingWIthGenres(event.target.value);

        let defaultValue = "movie_lens_by_rating";
        setRatingWIthAdult(defaultValue);

        getChartData(event.target.value)
    };

    const [ratingWIthAdult, setRatingWIthAdult] = useState('');
    const handleRatingWithAdultChange = (event) => {
        setRatingWIthAdult(event.target.value);

        let defaultValue = "movie_lens_by_rating";
        setRatingWIthGenres(defaultValue);

        getChartData(event.target.value)
    };

    const [genresWIthAdult, setGenresWIthAdult] = useState('');
    const handleGenresWithAdultChange = (event) => {
        setGenresWIthAdult(event.target.value);
        getChartData(event.target.value)
    };

    async function getChartData(dataTitle) {
        try {
            let result = await DataService.getChartDataApi(dataTitle);
            setDataResult(result);
            setIsLoaded(true);
        } catch (err) {
            console.log(err)
        }
    }

    useEffect(() => {
        getChartData("movie_lens_by_year");

        if (process.env.NODE_ENV === 'production') {
            ReactGA.pageview('MovieLens Analysis page view');
        }

    }, []);

    const handleTabChange = (event, newTabValue) => {
        setIsLoaded(false);
        let dataTitle;
        switch (newTabValue) {
            case 0:
                dataTitle = "movie_lens_by_year";
                break;
            case 1:
                dataTitle = "movie_lens_by_rating";
                break;
            case 2:
                dataTitle = "movie_lens_by_genres";
                break;
            default:
                dataTitle = "movie_lens_by_year";
                break;
        }
        getChartData(dataTitle);
        setTabValue(newTabValue);
    };

    function a11yProps(index) {
        return {
            id: `simple-tab-${index}`,
            'aria-controls': `simple-tabpanel-${index}`,
        };
    }

    return (
        <Box>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={tabValue} variant="scrollable" onChange={handleTabChange} aria-label="basic tabs example">
                    <Tab label="By Year " {...a11yProps(0)} />
                    <Tab label="By Rating " {...a11yProps(1)} />
                    <Tab label="By Genres " {...a11yProps(2)} />
                </Tabs>
            </Box>

            <TabPanel value={tabValue} index={0}>
                <Accordion sx={{ my: 2 }}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="year-panel1a-content"
                        id="year-panel1a-header">
                        <Typography component="span">Filter</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={2}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="rating-by-year-select-label">Rating</InputLabel>
                                        <Select
                                            labelId="rating-by-year-select-label"
                                            id="rating-by-year-select"
                                            value={yearWIthRating}
                                            label="Rating"
                                            onChange={handleYearWithRatingChange}>
                                            {[{ val: "movie_lens_by_year", lable: "All" },
                                            { val: "movie_lens_rating_4.5_to_5_by_year", lable: "4.5 - 5" },
                                            { val: "movie_lens_rating_4_to_4.5_by_year", lable: "4 - 4.5" },
                                            { val: "movie_lens_rating_3.5_to_4_by_year", lable: "3.5 - 4" },
                                            { val: "movie_lens_rating_3_to_3.5_by_year", lable: "3 - 3.5" },
                                            { val: "movie_lens_rating_2.5_to_3_by_year", lable: "2.5 - 3" },
                                            { val: "movie_lens_rating_2_to_2.5_by_year", lable: "2 - 2.5" },
                                            { val: "movie_lens_rating_1.5_to_2_by_year", lable: "1.5 - 2" },
                                            { val: "movie_lens_rating_1_to_1.5_by_year", lable: "1 - 1.5" },
                                            { val: "movie_lens_rating_0.5_to_1_by_year", lable: "0.5 - 1" },
                                            { val: "movie_lens_rating_0_to_0.5_by_year", lable: "0 - 0.5" }].map(function (item) {
                                                return <MenuItem key={item.val} value={item.val}>{item.lable}</MenuItem>;
                                            })}
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={3}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="genres-by-year-select-label">Genres</InputLabel>
                                        <Select
                                            labelId="genres-by-year-select-label"
                                            id="genres-by-year-select"
                                            value={yearWIthGenres}
                                            label="Genres"
                                            onChange={handleYearWithGenresChange}>
                                            {[{ val: "movie_lens_by_year", lable: "All" },
                                            { val: "movie_lens_genres_Action_by_year", lable: "Action" },
                                            { val: "movie_lens_genres_Adventure_by_year", lable: "Adventure" },
                                            { val: "movie_lens_genres_Animation_by_year", lable: "Animation" },
                                            { val: "movie_lens_genres_Biography_by_year", lable: "Biography" },
                                            { val: "movie_lens_genres_Comedy_by_year", lable: "Comedy" },
                                            { val: "movie_lens_genres_Crime_by_year", lable: "Crime" },
                                            { val: "movie_lens_genres_Documentary_by_year", lable: "Documentary" },
                                            { val: "movie_lens_genres_Drama_by_year", lable: "Drama" },
                                            { val: "movie_lens_genres_Family_by_year", lable: "Family" },
                                            { val: "movie_lens_genres_Fantasy_by_year", lable: "Fantasy" },
                                            { val: "movie_lens_genres_Film-Noir_by_year", lable: "Film-Noir" },
                                            { val: "movie_lens_genres_History_by_year", lable: "History" },
                                            { val: "movie_lens_genres_Horror_by_year", lable: "Horror" },
                                            { val: "movie_lens_genres_Music_by_year", lable: "Music" },
                                            { val: "movie_lens_genres_Musical_by_year", lable: "Musical" },
                                            { val: "movie_lens_genres_Mystery_by_year", lable: "Mystery" },
                                            { val: "movie_lens_genres_Romance_by_year", lable: "Romance" },
                                            { val: "movie_lens_genres_Sci-Fi_by_year", lable: "Sci-Fi" },
                                            { val: "movie_lens_genres_Sport_by_year", lable: "Sport" },
                                            { val: "movie_lens_genres_Thriller_by_year", lable: "Thriller" },
                                            { val: "movie_lens_genres_War_by_year", lable: "War" },
                                            { val: "movie_lens_genres_Western_by_year", lable: "Western" }].map(function (item) {
                                                return <MenuItem key={item.val} value={item.val}>{item.lable}</MenuItem>;
                                            })}
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={2}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="adult-by-year-select-label">18+</InputLabel>
                                        <Select
                                            labelId="adult-by-year-select-label"
                                            id="adult-by-year-select"
                                            value={yearWIthAdult}
                                            label="Adult"
                                            onChange={handleYearWithAdultChange}>
                                            <MenuItem key="movie_lens_by_year" value="movie_lens_by_year">All</MenuItem>
                                            <MenuItem key="movie_lens_is_adult_by_year" value="movie_lens_is_adult_by_year">Only for adult</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                        </Grid>
                    </AccordionDetails>
                </Accordion>

                <h2 >{isLoaded ? null : <LinearProgress />}</h2>
                <YearBarChartComponent
                    chartTitle="Number of Moive by Year"
                    dataResult={dataResult}
                    xAxis="Year"
                    yAxis="Number of Moive"
                    xAxisKey="year"
                    yAxisKey="movie_count"
                    chartRgbColor="2,7,93" />
                <YearBarChartComponent
                    chartTitle="Average Rating by Year"
                    dataResult={dataResult}
                    xAxis="Year"
                    yAxis="Average Rating"
                    xAxisKey="year"
                    yAxisKey="avg_rating"
                    chartRgbColor="218,165,32" />
                <YearBarChartComponent
                    chartTitle="Number of Vote by Year"
                    dataResult={dataResult}
                    xAxis="Year"
                    yAxis="Number of Vote"
                    xAxisKey="year"
                    yAxisKey="vote_count"
                    chartRgbColor="21,71,52" />
                <CommentComponent sectionId="movie_lens_by_year"></CommentComponent>
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
                <Accordion sx={{ my: 2 }}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="rating-panel1a-content"
                        id="rating-panel1a-header">
                        <Typography component="span">Filter</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={3}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="genres-by-rating-select-label">Genres</InputLabel>
                                        <Select
                                            labelId="genres-by-rating-select-label"
                                            id="genres-by-rating-select"
                                            value={ratingWIthGenres}
                                            label="Genres"
                                            onChange={handleRatingWithGenresChange}>
                                            {[{ val: "movie_lens_by_rating", lable: "All" },
                                            { val: "movie_lens_genres_Action_by_rating", lable: "Action" },
                                            { val: "movie_lens_genres_Adventure_by_rating", lable: "Adventure" },
                                            { val: "movie_lens_genres_Animation_by_rating", lable: "Animation" },
                                            { val: "movie_lens_genres_Biography_by_rating", lable: "Biography" },
                                            { val: "movie_lens_genres_Comedy_by_rating", lable: "Comedy" },
                                            { val: "movie_lens_genres_Crime_by_rating", lable: "Crime" },
                                            { val: "movie_lens_genres_Documentary_by_rating", lable: "Documentary" },
                                            { val: "movie_lens_genres_Drama_by_rating", lable: "Drama" },
                                            { val: "movie_lens_genres_Family_by_rating", lable: "Family" },
                                            { val: "movie_lens_genres_Fantasy_by_rating", lable: "Fantasy" },
                                            { val: "movie_lens_genres_Film-Noir_by_rating", lable: "Film-Noir" },
                                            { val: "movie_lens_genres_History_by_rating", lable: "History" },
                                            { val: "movie_lens_genres_Horror_by_rating", lable: "Horror" },
                                            { val: "movie_lens_genres_Music_by_rating", lable: "Music" },
                                            { val: "movie_lens_genres_Musical_by_rating", lable: "Musical" },
                                            { val: "movie_lens_genres_Mystery_by_rating", lable: "Mystery" },
                                            { val: "movie_lens_genres_Romance_by_rating", lable: "Romance" },
                                            { val: "movie_lens_genres_Sci-Fi_by_rating", lable: "Sci-Fi" },
                                            { val: "movie_lens_genres_Sport_by_rating", lable: "Sport" },
                                            { val: "movie_lens_genres_Thriller_by_rating", lable: "Thriller" },
                                            { val: "movie_lens_genres_War_by_rating", lable: "War" },
                                            { val: "movie_lens_genres_Western_by_rating", lable: "Western" }].map(function (item) {
                                                return <MenuItem key={item.val} value={item.val}>{item.lable}</MenuItem>;
                                            })}
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={2}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="adult-by-rating-select-label">18+</InputLabel>
                                        <Select
                                            labelId="adult-by-rating-select-label"
                                            id="adult-by-rating-select"
                                            value={ratingWIthAdult}
                                            label="Adult"
                                            onChange={handleRatingWithAdultChange}>
                                            <MenuItem key="movie_lens_by_rating" value="movie_lens_by_rating">All</MenuItem>
                                            <MenuItem key="movie_lens_is_adult_by_rating" value="movie_lens_is_adult_by_rating">Only for adult</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                        </Grid>
                    </AccordionDetails>
                </Accordion>

                <h2 >{isLoaded ? null : <LinearProgress />}</h2>
                <RatingBarChartComponent
                    chartTitle="Number of Moive by Rating"
                    dataResult={dataResult}
                    xAxis="Rating"
                    yAxis="Number of Moive"
                    xAxisKey="rating"
                    yAxisKey="movie_count"
                    chartRgbColor="2,7,93" />
                <RatingBarChartComponent
                    chartTitle="Number of Vote by Rating"
                    dataResult={dataResult}
                    xAxis="Rating"
                    yAxis="Number of Vote"
                    xAxisKey="rating"
                    yAxisKey="vote_count"
                    chartRgbColor="21,71,52" />
                <CommentComponent sectionId="movie_lens_by_rating"></CommentComponent>
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
                <Accordion sx={{ my: 2 }}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="genres-panel1a-content"
                        id="genres-panel1a-header">
                        <Typography component="span">Filter</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={2}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="adult-by-genres-select-label">18+</InputLabel>
                                        <Select
                                            labelId="adult-by-genres-select-label"
                                            id="adult-by-genres-select"
                                            value={genresWIthAdult}
                                            label="Adult"
                                            onChange={handleGenresWithAdultChange}>
                                            <MenuItem key="movie_lens_by_genres" value="movie_lens_by_genres">All</MenuItem>
                                            <MenuItem key="movie_lens_is_adult_by_genres" value="movie_lens_is_adult_by_genres">Only for adult</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                        </Grid>
                    </AccordionDetails>
                </Accordion>
                <h2 >{isLoaded ? null : <LinearProgress />}</h2>
                <GenresPieChartComponent
                    chartTitle="Number of Moive by Genres"
                    dataResult={dataResult}
                    dataKey="movie_count"
                    labelKey="genre" />
                <GenresPieChartComponent
                    chartTitle="Average Rating by Genres"
                    dataResult={dataResult}
                    dataKey="avg_rating"
                    labelKey="genre" />
                <GenresPieChartComponent
                    chartTitle="Number of Vote by Genres"
                    dataResult={dataResult}
                    dataKey="vote_count"
                    labelKey="genre" />
                <CommentComponent sectionId="movie_lens_by_genres"></CommentComponent>
            </TabPanel>

        </Box>
    );
}

export default MovieLensAnalysisComponent;