import React from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import EqualizerIcon from '@material-ui/icons/Equalizer';

function GoButton() {

  return (
    <Grid style={{ 'padding-bottom': 50, 'padding-top': 50 }} container spacing={1} justify="center">
      <Grid item xs={8}>

        <Button variant="contained" color="primary">
          <EqualizerIcon style={{ 'padding-right': 5 }} /> Process
        </Button>

      </Grid>
    </Grid>
  );
}

export default GoButton;