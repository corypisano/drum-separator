import React from 'react';

import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';

export default function Upload(props) {

  const { onChange } = props;

  return (

    <Grid style={{ 'padding-bottom': 50, 'padding-top': 50 }} container spacing={1} justify="center">
      <Grid item xs={8}>

        <input
          accept="*.mp3"
          style={{ display: 'none' }}
          id="raised-button-file"
          multiple
          type="file"
          onChange={onChange}
          // onChange={(e) => {this.readFile(e)}}
        />
        <label htmlFor="raised-button-file">
          <Button variant="contained" component="span" color="primary">
            <CloudUploadIcon style={{ 'padding-right': 5 }} /> Upload
          </Button>
        </label>

      </Grid>
    </Grid>
  );
}
