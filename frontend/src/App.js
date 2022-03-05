import axios from 'axios';
import React, { useState, useEffect } from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Typography from '@mui/material/Typography';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';


function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [dense, setDense] = React.useState(false);
  const [movies, setMovies] = React.useState([]);
  const [movie, setMovie] = React.useState('');
  const [recommendMovies, setRecommendMovies] = React.useState([]);

    useEffect(() => {
      async function fetchData() {
          const response = await axios.get('http://127.0.0.1:8000/movies/');
          setMovies(response.data.movies);
          setIsLoading(false);
      }
      fetchData();
  }, [])


  async function get_recommended_movies(movie) {
    const response = await axios.get(`http://127.0.0.1:8000/recommender/${movie}/`);
    setRecommendMovies(response.data.movies);
  }

  const handleChange = (event) => {
    var movie = event.target.value;
    setMovie(movie);
    get_recommended_movies(movie);
  };

  return (
    <div className="">
      <Grid 
      container
      spacing={2}
      columns={{ xs: 4, md: 12 }}
      direction="column"
      alignItems="center"
      justifyContent="center"
      style={{ minHeight: '100vh' }}
      >
      
      {
        isLoading && <div><p>Loading</p></div>
      }
      <FormControl sx={{ width: '25ch' }}>
      <InputLabel id="demo-simple-select-label">Select movie</InputLabel>
      <Select
        labelId="demo-simple-select-label"
        id="demo-simple-select"
        value={movie}
        label={movie}
        onChange={handleChange}
      >
        {movies && movies.map((movie) => (
          <MenuItem value={movie}>{movie}</MenuItem>
        ))}
      </Select>
    </FormControl>
        <Grid item xs={12} md={6}>
          <Typography sx={{ mt: 4, mb: 2 }} variant="h6" component="div">
            {recommendMovies &&
              <>
              Recommended For you
              </>
            }
          </Typography>
            <List dense={dense}>
              {recommendMovies && recommendMovies.map((movie) => (
                <ListItem>
                  <ListItemText
                    primary={movie}
                    />
                </ListItem>
              ))
              }
            </List>
        </Grid>

      </Grid>
    </div>
  );
}

export default App;
