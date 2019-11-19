import React from 'react';
import './App.css';

import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Box from '@material-ui/core/Box';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepButton from '@material-ui/core/StepButton';

import TopColorLine from './components/TopColorLine';
import Upload from './components/Upload';
import MixSlider from './components/MixSlider';
import GoButton from './components/GoButton';

function App() {
  const logo = require('./purple_sound_wave.png');

  const useStyles = makeStyles(theme => ({
    root: {
      width: '90%',
    },
    button: {
      marginRight: theme.spacing(1),
    },
    completed: {
      display: 'inline-block',
    },
    instructions: {
      marginTop: theme.spacing(1),
      marginBottom: theme.spacing(1),
    },
  }));

  function getSteps() {
    return ['Upload track', 'Choose mix', 'Go'];
  };

  function getStepContent(step) {
    switch (step) {
      case 0:
        return <Upload />;
      case 1:
        return <MixSlider />;
      case 2:
        return <GoButton />;
      default:
        return 'Unknown step';
    }
  }
  const classes = useStyles();
  const [activeStep, setActiveStep] = React.useState(0);
  const [completed, setCompleted] = React.useState({});
  const steps = getSteps();

  const totalSteps = () => {
    return steps.length;
  };

  const completedSteps = () => {
    return Object.keys(completed).length;
  };

  const isLastStep = () => {
    return activeStep === totalSteps() - 1;
  };

  const allStepsCompleted = () => {
    return completedSteps() === totalSteps();
  };

  const handleNext = () => {
    const newActiveStep =
      isLastStep() && !allStepsCompleted()
        ? // It's the last step, but not all steps have been completed,
        // find the first step that has been completed
        steps.findIndex((step, i) => !(i in completed))
        : activeStep + 1;
    setActiveStep(newActiveStep);
  };

  const handleBack = () => {
    setActiveStep(prevActiveStep => prevActiveStep - 1);
  };

  const handleStep = step => () => {
    setActiveStep(step);
  };

  return (
    <div className="App">
      <TopColorLine />
      <header className="App-header">

        <main>
          <Container maxWidth="lg">
            <Box display="flex" justifyContent="left" alignItems="center">
              <img src={logo} className="App-logo" alt="logo" style={{ 'padding-right': 10, height: 60 }} />
              <h2>Drum Separator</h2>
            </Box>
            <p>A free tool for separating or remixing drums in tracks</p>

            <Card>
              <CardContent>
                <Stepper nonLinear activeStep={activeStep}>
                  {steps.map((label, index) => (
                    <Step key={label}>
                      <StepButton onClick={handleStep(index)} completed={completed[index]}>
                        {label}
                      </StepButton>
                    </Step>
                  ))}
                </Stepper>

                {getStepContent(activeStep)}

                <CardActions disableSpacing>
                  <Button disabled={activeStep === 0} onClick={handleBack} className={classes.button}>
                    Back
                  </Button>
                  {activeStep < steps.length - 1 && // don't show next on final step
                    <Button
                      variant="outlined"
                      onClick={handleNext}
                      className={classes.button}
                    >
                      Next
                    </Button>
                  }
                </CardActions>
              </CardContent>
            </Card>

          </Container>
        </main>
      </header>
    </div>
  );
}

export default App;
