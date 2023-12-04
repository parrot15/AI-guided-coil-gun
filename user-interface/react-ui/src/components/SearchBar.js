import React, { useState, useEffect } from 'react';
import { Box, TextField, Button } from '@mui/material';
import settings from '../settings/settings.json';

const SearchBar = ({ disabled }) => {
  const [prompt, setPrompt] = useState('');

  useEffect(() => {
    if (disabled) {
      // When Manual mode is set, clear the prompt and send an empty string
      setPrompt('');
      sendPrompt('');
    }
  }, [disabled]);

  const sendPrompt = async (prompt) => {
    try {
      const response = await fetch(
        `${settings.api.url}/object-detection/prompt`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt }),
        },
      );
      const data = await response.json();
      console.log(`response:\n${JSON.stringify(data)}`);
    } catch (error) {
      console.error('Error sending prompt to backend:', error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await sendPrompt(prompt);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <form onSubmit={handleSubmit} style={{ display: 'flex' }}>
        <TextField
          label="Enter object to detect"
          variant="outlined"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled={disabled}
          sx={{ marginRight: 1 }}
          autoComplete="off"
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={disabled}
        >
          Detect
        </Button>
      </form>
    </Box>
  );
};

export default SearchBar;
