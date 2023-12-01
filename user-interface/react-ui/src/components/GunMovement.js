import React, { useState, useEffect, useRef, useCallback } from 'react';
import { io } from 'socket.io-client';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import settings from '../settings/settings.json';

const GunMovement = ({ disabled }) => {
  const [socket, setSocket] = useState(null);
  const socketRef = useRef(socket);
  const processingKey = useRef(false);

  const sendCommand = useCallback((direction) => {
    if (socketRef.current) {
      socketRef.current.emit('gun-movement', direction);
    }
  }, []);

  const handleKeyDown = useCallback(
    (e) => {
      const keyToDirection = {
        w: 'up',
        a: 'left',
        s: 'down',
        d: 'right',
      };

      const direction = keyToDirection[e.key.toLowerCase()];

      if (direction && !processingKey.current) {
        processingKey.current = true;
        sendCommand(direction);
      }
    },
    [sendCommand],
  );

  const handleKeyUp = useCallback(
    (e) => {
      const validKeys = ['w', 'a', 's', 'd'];

      if (validKeys.includes(e.key.toLowerCase()) && processingKey.current) {
        processingKey.current = false;
        sendCommand('stop');
      }
    },
    [sendCommand],
  );

  useEffect(() => {
    const newSocket = io(settings.api.url);
    setSocket(newSocket);
    socketRef.current = newSocket;

    return () => {
      newSocket.disconnect();
    };
  }, []);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp]);

  return (
    <Grid container spacing={5} alignItems="center" justifyContent="center"       
      sx={{
      position:'absolute',
      height: 'auto',
      width: 'auto',
      top: '90%',
    }}>
      <Grid item>
        <Button
          onMouseDown={() => sendCommand('up')}
          onMouseUp={() => sendCommand('stop')}
          disabled={disabled}
        >
          Up (W)
        </Button>
      </Grid>
      <Grid item>
        <Button
          onMouseDown={() => sendCommand('down')}
          onMouseUp={() => sendCommand('stop')}
          disabled={disabled}
        >
          Down (S)
        </Button>
      </Grid>
      <Grid item>
        <Button
          onMouseDown={() => sendCommand('left')}
          onMouseUp={() => sendCommand('stop')}
          disabled={disabled}
        >
          Left (A)
        </Button>
      </Grid>
      <Grid item>
        <Button
          onMouseDown={() => sendCommand('right')}
          onMouseUp={() => sendCommand('stop')}
          disabled={disabled}
        >
          Right (D)
        </Button>
      </Grid>
    </Grid>
  );
};

export default GunMovement;
