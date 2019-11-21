import React from 'react';

import Grid from '@material-ui/core/Grid';
import Slider from '@material-ui/core/Slider';
import Box from '@material-ui/core/Box';

export default function MixSlider(props) {

  const handleSliderChange = props.handleSliderChange;
  const drumMix = props.drumMix;

  return (

    <Grid style={{ 'padding-bottom': 41, 'padding-top': 41 }} container spacing={1} justify="center">
      <Grid item xs={10}>
        <Slider
          aria-labelledby="drum-mix-slider"
          value={typeof drumMix === 'number' ? drumMix : 0}
          onChange={handleSliderChange}
          valueLabelDisplay="on"
        />
        <Box display="flex">
          <Box fontSize={16} fontWeight="fontWeightLight">No Drums</Box>
          <Box flexGrow={1}></Box>
          <Box fontSize={16} fontWeight="fontWeightLight">Only Drums</Box>
        </Box>
      </Grid>
    </Grid>
  );
}
