import { useEffect } from 'react';
import ReactGA from 'react-ga';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import { Link } from "react-router-dom";
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';


const HomeComponent = () => {

    useEffect(() => {
        if (process.env.NODE_ENV === 'production') {
          ReactGA.pageview('Home page view');
        }
      }, []);

    return (
        <Box sx={{ flexGrow: 1, p: 2 }}>
            <Typography pb={2} sx={{ fontStyle: 'italic', fontWeight: 'bold' }}>More than 100 million IMDb and MovieLens items were processed!</Typography>
            <Grid container spacing={2}>
                <Grid item xs={12} md={12}>
                    <Button variant="outlined" component={Link} to={'/dataFlow'} key="dataFlow" size="large" sx={{ width: '100%', height: '65px' }}>
                        <Stack direction="row" spacing={2}>
                            <img src="https://img.icons8.com/ios-filled/26/000000/serial-tasks.png" alt="Data Flow" />
                            <Box>Data Flow</Box>
                        </Stack>
                    </Button>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Button variant="outlined" component={Link} to={'/imdbAnalysis'} key="imdbAnalysis" size="large" sx={{ width: '100%', height: '65px' }}>
                        <Stack direction="row" spacing={2}>
                            <img src="https://img.icons8.com/ios-filled/30/000000/imdb.png" alt="IMDb Analysis" />
                            <Box>IMDb Analysis</Box>
                        </Stack>
                    </Button>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Button variant="outlined" component={Link} to={'/movieLensAnalysis'} key="movieLensAnalysis" size="large" sx={{ width: '100%', height: '65px' }}>
                        <Stack direction="row" spacing={2}>
                            <img src="https://img.icons8.com/ios-filled/26/000000/movie.png" alt="MovieLens Analysis" />
                            <Box>MovieLens Analysis</Box>
                        </Stack>
                    </Button>
                </Grid>
                <Grid item xs={12} md={12}>
                    <Button variant="outlined" component={Link} to={'/behindTheScenes'} key="behindTheScenes" size="large" sx={{ width: '100%', height: '65px' }}>
                        <Stack direction="row" spacing={2}>
                            <img src="https://img.icons8.com/ios-filled/28/000000/drafting-compass2.png" alt="Behind The Scenes" />
                            <Box>Behind The Scenes</Box>
                        </Stack>
                    </Button>
                </Grid>
            </Grid>
        </Box>
    );
}

export default HomeComponent;