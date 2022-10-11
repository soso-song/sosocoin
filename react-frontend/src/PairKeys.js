import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';
import { CardActions, CardContent,IconButton,Box} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

export default function PairKeys(props) {
  return (
    <>
      <Title>Pair Keys</Title>
      <CardContent sx={{flex:1}}>
        <Box display="flex" flexDirection='row' textAlign='center' height='100%' maxHeight='150px'>
            <Box width='50%' height='100%' paddingLeft='5px' paddingRight='5px' display='flex' flexDirection='column'>
                <Box sc={{flex:1}} height='100%' sx={{wordWrap:'break-word'}} overflow='hidden' >
                <Typography gutterBottom component="p" variant="h6" height='100%'>
                    {props.privateK ? props.privateK : 'N/A'}
                </Typography>
                </Box>
                <Typography>Private</Typography>
            </Box>
            <Box width='50%' height='100%' paddingLeft='5px' paddingRight='5px' display='flex' flexDirection='column'>
                <Box sc={{flex:1}} height='100%' sx={{wordWrap:'break-word'}} overflow='hidden' >
                <Typography gutterBottom component="p" variant="h6" height='100%'>
                    {props.publicK ? props.publicK : 'N/A'}
                </Typography>
                </Box>
                <Typography>Public</Typography>
            </Box>
        </Box>
      </CardContent>
      <CardActions sx={{marginTop:'0'}}>
        <IconButton onClick={()=>{props.getPairKeys()}}>
            <RefreshIcon />
        </IconButton>
      </CardActions>
    </>
  );
}