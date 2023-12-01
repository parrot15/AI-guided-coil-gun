import {React, useState} from 'react';
import {Container, Grid, Box, Button, Stack, Typography, Divider} from '@mui/material';
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
        {/* <Grid item container sx={{
          display: 'flex',
          justifyContent: 'center',
          width: '100%',
          p: 1,
          m: 1,
        }}>
          <SearchBar />
          <h3>test</h3>
        </Grid> */}
        {/* <div style={{ width: '100%' }}>
          <Box
            sx={{
              display: 'grid',
              // gridAutoColumns: '1fr',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: 1,
            }}
          >
            <Grid item sx={{ gridRow: '1', gridColumn: 'span 8' }}>
              <SearchBar />
            </Grid>
            <Grid sx={{ gridRow: '1', gridColumn: 'span 2' }}>
              <h3>test</h3>
            </Grid>
          </Box>
        </div> */}
        {/* <Grid container>
          <Grid item>Left</Grid>                          
          <Grid item xs>                                 
            <Grid container direction="row-reverse">      
              <Grid item>Right</Grid>
            </Grid>
          </Grid>
        </Grid> */}
        {/* <Grid container spacing={3} direction="row" justify="space-between" alignItems="center">
          <Grid item xs={6}>
            <SearchBar/>
          </Grid>
          <Grid item xs={3}>
            <h3>test</h3>
          </Grid>
        </Grid> */}
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
        {/* <Stack direction="row" spacing={1} divider={<Divider orientation="vertical" flexItem />} justifyContent='space-between'>
          <Box align='left'>
              <Typography>Test 1</Typography>
          </Box>
          <Stack direction="row" justifyContent={"flex-end"} spacing={1}>
            <Box>
                <Typography sx={{ verticalAlign: 'middle', display: 'inline-flex' }}>Test 2</Typography>
            </Box>
            <Box>
                <Typography sx={{ verticalAlign: 'middle', display: 'inline-flex' }}>Test 3</Typography>
            </Box>
          </Stack>
        </Stack> */}
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
            {/* <h3>test</h3> */}
            <FireButton controlMode={controlMode} />
          </Grid>
        </Grid>
        {/* <Grid item>
          <GunMovement disabled={controlMode === 'auto-aim'} />
        </Grid> */}
      </Grid>
    </Container>
  );
}

export default App;
