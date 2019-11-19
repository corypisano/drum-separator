import React, { Component } from 'react';

import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';

class Upload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      file: ''
    };
    
    this.readFile = this.readFile.bind(this);
  }
  
  readFile(e) {
    // TODO check for file valid file & type
    // flash error if invalid
    this.setState({file: e.target.files[0]});
  }

  render() {
    return (

      <Grid style={{ 'padding-bottom': 50, 'padding-top': 50 }} container spacing={1} justify="center">
        <Grid item xs={8}>

          <input
            accept="*.mp3"
            style={{ display: 'none' }}
            id="raised-button-file"
            multiple
            type="file"
            onChange={(e) => {this.readFile(e)}}
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
}

export default Upload;