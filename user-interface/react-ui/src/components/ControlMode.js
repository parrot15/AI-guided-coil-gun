import React from 'react';
import {
  FormControl,
  RadioGroup,
  FormControlLabel,
  Radio,
} from '@mui/material';

const ControlMode = ({ mode, setMode }) => {
  const handleModeChange = (event) => {
    setMode(event.target.value);
  };

  return (
    <FormControl component="fieldset">
      <RadioGroup
        row
        aria-label="control-mode"
        name="control-mode"
        value={mode}
        defaultValue="manual"
        onChange={handleModeChange}
      >
        <FormControlLabel value="manual" control={<Radio />} label="Manual" />
        <FormControlLabel
          value="auto-aim"
          control={<Radio />}
          label="Auto-aim"
        />
      </RadioGroup>
    </FormControl>
  );
};

export default ControlMode;
