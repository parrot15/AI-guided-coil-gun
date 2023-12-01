import React, { useState, useEffect, useRef} from 'react';
import { io } from 'socket.io-client';
import Box from '@mui/material/Box';
import settings from '../settings/settings.json';

const CameraImagery = () => {
  // const [socket, setSocket] = useState(null);
  // const canvasRef = useRef();
  // const [imageData, setImageData] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  // const [boundingBoxList, setBoundingBoxList] = useState(null);

  useEffect(() => {
    const newSocket = io(settings.api.url);
    // const newSocket = io(settings.api.url, { transports: ['websocket'] });
  //   const newSocket = io(settings.api.url, {
  //     reconnectionDelay: 1000,
  //     reconnection:true,
  //     reconnectionAttempts: 10,
  //     transports: ['websocket'],
  //     agent: false, // [2] Please don't set this to true
  //     upgrade: false,
  //     rejectUnauthorized: false
  //  });
    // setSocket(newSocket);
    newSocket.on('camera-imagery', (frame) => {
      // Convert blob object to image URL and set it as the source
      const urlCreator = window.URL || window.webkitURL;
      const imageUrl = urlCreator.createObjectURL(new Blob([frame]));
      // const imageUrl = urlCreator.createObjectURL(frame);

      // Revoke previous image URL to avoid memory leak
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }

      setImageSrc(imageUrl);
      // setImageData(frame);
    });
    // newSocket.on('gpu-bounding-box', (boundingBoxList) => {
    //   setBoundingBoxList(boundingBoxList);
    // });
    return () => {
      // Clean up websocket
      newSocket.close()
      // Clean up image URL object
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }
    };
  // }, [setSocket, imageSrc]);
  }, [imageSrc]);

  // function drawBoundingBoxes(){
  //   const context = canvasRef.current.getContext("2d");
  //   context.strokeStyle = "white";
  //   context.lineWidth = 2;
  //   context.strokeRect(50, 30, 110, 90);
  //   context.strokeRect(170, 65, 100, 80);
  // };

  // useEffect(() => {
  //     drawBoundingBoxes();
  // }, []);

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