import * as React from 'react';
import {Box,Button,Typography, IconButton,Collapse} from '@mui/material';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

export default function Mining(props) {
  const [open, setOpen] = React.useState(true);
  const handleClick = () => {
    setOpen(!open);
  };
  return (
    <Box sx={{ mt: 3,width:500,margin:'auto'}}>
        <Typography>Flask saying my port = {window.token}</Typography>
        <Typography>{props.message}</Typography>
        <Button
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          onClick={()=>{props.startMining()}}
        >
            Start Mining
        </Button>
        { props.miningState ? (
            <>
        <Typography>Mining States 
            <IconButton  onClick={handleClick}>
            {open? <ExpandLess /> : <ExpandMore />}
            </IconButton>
        </Typography>
        <Collapse in={open} timeout="auto" unmountOnExit>
            <Typography variant='caption'>{props.miningState}</Typography>
        </Collapse>
        </>
        ) : ''}
    </Box>
  );
}