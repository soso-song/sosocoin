import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';
import { CardActions, CardContent,IconButton } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

export default function Balance(props) {
  return (
    <>
      <Title>Balance</Title>
      <CardContent sx={{flex:1}}>
        <Typography noWrap component="p" variant="h4" sc={{flex:1}}>
            {props.balance}
        </Typography>
      </CardContent>
      <CardActions sx={{marginTop:'0'}}>
        <IconButton onClick={()=>{props.getBalance()}}>
            <RefreshIcon />
        </IconButton>
      </CardActions>
    </>
  );
}