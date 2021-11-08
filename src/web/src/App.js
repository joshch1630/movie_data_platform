import './App.css';
import { useState } from 'react';
import Config from './Config';
import ReactGA from 'react-ga';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import PropTypes from 'prop-types';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Slide from '@mui/material/Slide';
import useScrollTrigger from '@mui/material/useScrollTrigger';
import { createTheme } from '@mui/material/styles';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import routes from "./Router/routes";


if (process.env.NODE_ENV === 'production') {
  ReactGA.initialize(Config.GA_TRACKING_ID);
  ReactGA.pageview('Init Page View Landing');
}

const drawerWidth = 240;

const theme = createTheme({
  palette: {
    primary: {
      main: '#424242',
    }
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
  },
});

function App(props) {

  const { window } = props;
  const [mobileOpen, setMobileOpen] = useState(false);
  const [subMenuOpen, setSubMenuOpen] = useState(true);

  const handleClick = () => {
    setSubMenuOpen(!subMenuOpen);
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleDrawerClose = () => {
    setMobileOpen(false);
  };

  const drawer = (
    <Box>
      <List >
        <ListItemButton component={Link} to={'/'} key="home" onClick={handleDrawerClose}>
          <ListItemIcon >
            <img src="https://img.icons8.com/ios-filled/26/000000/home.png" alt="Home" />
          </ListItemIcon>
          <ListItemText primary="Home" />
        </ListItemButton>
      </List>

      <Divider />
      <List>
        <ListItemButton component={Link} to={'/dataFlow'} key="dataFlow" onClick={handleDrawerClose}>
          <ListItemIcon>
            <img src="https://img.icons8.com/ios-filled/26/000000/serial-tasks.png" alt="Data Flow" />
          </ListItemIcon>
          <ListItemText primary="Data Flow" />
        </ListItemButton>

        <ListItemButton onClick={handleClick}>
          <ListItemIcon>
            <img src="https://img.icons8.com/ios-filled/28/000000/combo-chart--v1.png" alt="Data Analysis" />
          </ListItemIcon>
          <ListItemText primary="Data Analysis" />
          {subMenuOpen ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={subMenuOpen} timeout="auto" unmountOnExit>

          <List disablePadding>
            <ListItemButton component={Link} to={'/imdbAnalysis'} sx={{ pl: 3 }} key="imdbAnalysis" onClick={handleDrawerClose}>
              <ListItemIcon>
                <img src="https://img.icons8.com/ios-filled/30/000000/imdb.png" alt="IMDb Analysis" />
              </ListItemIcon>
              <ListItemText primary="IMDb Analysis" />
            </ListItemButton>

            <ListItemButton component={Link} to={'/movieLensAnalysis'} sx={{ pl: 3 }} key="movieLensAnalysis" onClick={handleDrawerClose}>
              <ListItemIcon>
                <img src="https://img.icons8.com/ios-filled/26/000000/movie.png" alt="MovieLens Analysis" />
              </ListItemIcon>
              <ListItemText primary="MovieLens Analysis" />
            </ListItemButton>

          </List>

        </Collapse>
      </List>

      <Divider />
      <List>
        <ListItemButton component={Link} to={'/behindTheScenes'} key="behindTheScenes" onClick={handleDrawerClose}>
          <ListItemIcon>
            <img src="https://img.icons8.com/ios-filled/28/000000/drafting-compass2.png" alt="Behind The Scenes" />
          </ListItemIcon>
          <ListItemText primary="Behind The Scenes" />
        </ListItemButton>
      </List>

      <Box sx={{ pl: 2 }}><a target='_blank' rel="noreferrer" href="https://icons8.com/">Icons by Icons8</a></Box>

    </Box>
  );

  const container = window !== undefined ? () => window().document.body : undefined;

  function HideOnScroll(props) {
    const { children } = props;
    const trigger = useScrollTrigger();

    return (
      <Slide appear={false} direction="down" in={!trigger}>
        {children}
      </Slide>
    );
  }

  HideOnScroll.propTypes = {
    children: PropTypes.element.isRequired,
  };


  return (
    <Router>

      <ThemeProvider theme={theme}>
        <Box sx={{ display: 'flex' }}>
          <CssBaseline />

          <HideOnScroll {...props}>
            <AppBar
              position="fixed"
              sx={{
                width: { md: `calc(100% - ${drawerWidth}px)` },
                ml: { md: `${drawerWidth}px` },
              }}
            >
              <Toolbar variant="dense">
                <IconButton
                  color="inherit"
                  aria-label="open drawer"
                  edge="start"
                  onClick={handleDrawerToggle}
                  sx={{ mr: 2, display: { md: 'none' } }}
                >
                  <MenuIcon />
                </IconButton>
                <Typography variant="h6" noWrap component="span">
                  Moive Data Platform
                </Typography>
              </Toolbar>
            </AppBar>
          </HideOnScroll>

          <Box
            component="nav"
            sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}>
            <Drawer
              container={container}
              variant="temporary"
              open={mobileOpen}
              onClose={handleDrawerToggle}
              ModalProps={{
                keepMounted: true,
              }}
              sx={{
                display: { xs: 'block', md: 'none' },
                '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
              }}
            >
              {drawer}
            </Drawer>
            <Drawer
              variant="permanent"
              sx={{
                display: { xs: 'none', md: 'block' },
                '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
              }}
              open
            >
              {drawer}
            </Drawer>
          </Box>
          <Box
            component="main"
            sx={{ flexGrow: 1, py: 5, width: { md: `calc(100% - ${drawerWidth}px)` } }}
          >
            <Switch>
              {routes.map((route, index) => (
                // Render more <Route>s with the same paths as
                // above, but different components this time.
                <Route
                  key={index}
                  path={route.path}
                  exact={route.exact}
                  children={<route.main />}
                />
              ))}
            </Switch>

          </Box>
        </Box>
      </ThemeProvider>
    </Router>
  );
}

export default App;
