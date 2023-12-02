import React from 'react';
import { Button } from '@mui/material';
import settings from '../settings/settings.json';

const FireButton = ({ controlMode }) => {
  const sendFireCommand = async () => {
    try {
      const response = await fetch(`${settings.api.url}/fire-projectile`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ controlMode }),
      });
      const data = await response.json();
      console.log(`response:\n${JSON.stringify(data)}`);
    } catch (error) {
      console.error('Error sending prompt to backend:', error);
    }
  };

  const handleSubmit = async (event) => {
      event.preventDefault();
      await sendFireCommand();
  };

  return (
    <Button 
      variant="contained"
      color="error"
      onClick={handleSubmit}
      alignItems="center" justifyContent="center"
      sx={{
        position:'absolute',
        height: 'auto',
        width: 'auto',
        top: '90%',
      }}
    >
      Fire
    </Button>
  );
};

export default FireButton;
