import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import Box from '@mui/material/Box';
import settings from '../settings/settings.json';

const CameraImagery = () => {
  const [imageSrc, setImageSrc] = useState(null);

  useEffect(() => {
    const newSocket = io(settings.api.url);
    newSocket.on('camera-imagery', (frame) => {
      // Convert blob object to image URL and set it as the source
      const urlCreator = window.URL || window.webkitURL;
      const imageUrl = urlCreator.createObjectURL(new Blob([frame]));

      // Revoke previous image URL to avoid memory leak
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }

      setImageSrc(imageUrl);
    });
    return () => {
      // Clean up websocket
      newSocket.close()
      // Clean up image URL object
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }
    };
  }, [imageSrc]);

  return (
    <Box
      style={{
        position:'absolute',
        width: '70%',
        height: '70%',
        left: '50%',
        transform: 'translate(-50%, 0%)',
        border: 'solid 2px black',
        justifyContent: 'center',
        overflow: 'hidden', // Add this line to prevent scroll bars if the image is larger than the box
      }}>
      {imageSrc && (
        <img
          src={imageSrc}
          alt="Camera Feed"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }} // Updated styles for full coverage
        />
      )}
    </Box>
  );
};

export default CameraImagery;