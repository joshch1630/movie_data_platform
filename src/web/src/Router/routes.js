import React from "react";
import HomeComponent from "../Components/HomeComponent";
import DataFlowComponent from "../Components/DataFlowComponent";
import IMDbAnalysisComponent from "../Components/IMDbAnalysisComponent";
import MovieLensAnalysisComponent from "../Components/MovieLensAnalysisComponent";
import BehindTheScenesComponent from "../Components/BehindTheScenesComponent";
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';


const routes = [
  {
    path: "/",
    exact: true,
    name: "Home",
    toolbar: () => <Box>Home</Box>,
    main: () =>
      <Box>
        <Divider sx={{ pt: 2 }}><strong>Home</strong></Divider>
        <HomeComponent />
      </Box>
  },
  {
    path: "/dataFlow",
    name: "Data Flow",
    toolbar: () => <Box>Data Flow</Box>,
    main: () =>
      <Box>
        <Divider sx={{ pt: 2 }}><strong>Data Flow</strong></Divider>
        <DataFlowComponent />
      </Box>
  },
  {
    path: "/imdbAnalysis",
    name: "IMDb Analysis",
    toolbar: () => <Box>IMDb Analysis</Box>,
    main: () =>
      <Box>
        <Divider sx={{ pt: 2 }}><strong>IMDb Analysis</strong></Divider>
        <IMDbAnalysisComponent />
      </Box>
  },
  {
    path: "/movieLensAnalysis",
    name: "MovieLens Analysis",
    toolbar: () => <Box>MovieLens Analysis</Box>,
    main: () =>
      <Box>
        <Divider sx={{ pt: 2 }}><strong>MovieLens Analysis</strong></Divider>
        <MovieLensAnalysisComponent />
      </Box>
  },
  {
    path: "/behindTheScenes",
    name: "Behind The Scenes",
    toolbar: () => <Box>Behind The Scenes</Box>,
    main: () =>
      <Box>
        <Divider sx={{ pt: 2 }}><strong>Behind The Scenes</strong></Divider>
        <BehindTheScenesComponent />
      </Box>
  }
];

export default routes;