import {React, useState} from 'react';
import {Container, Grid } from '@mui/material';
import GunMovement from './components/GunMovement';
import CameraImagery from './components/CameraImagery';
import SearchBar from './components/SearchBar';
import ControlMode from './components/ControlMode';
import FireButton from './components/FireButton';
import './App.css';

function App() {
  const [controlMode, setControlMode] = useState('manual');

  return (
    <Container maxWidth="sm">
      <Grid container direction="column" spacing={2}>
        <Grid item style={{ textAlign: 'center' }}>
          <h1>Auto-Aiming Coil Gun</h1>
        </Grid>
        <Grid
          item
          container
          m={1}
          justifyContent="space-between"
          alignItems="center"
        >
          <Grid item>
            <SearchBar disabled={controlMode === 'manual'} />
          </Grid>
          <Grid item>
            <ControlMode mode={controlMode} setMode={setControlMode} />
          </Grid>
        </Grid>
        <Grid item>
          <CameraImagery />
        </Grid>
        <Grid
          item
          container
          m={1}
          justifyContent="space-between"
          alignItems="center"
        >
          <Grid item>
            <GunMovement disabled={controlMode === 'auto-aim'} />
          </Grid>
          <Grid item>
            <FireButton controlMode={controlMode} />
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
