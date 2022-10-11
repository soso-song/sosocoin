import * as React from 'react';
import Title from './Title';
import {Grid, TextField,Box,Button} from '@mui/material';

export default function SendTx(props) {
  const [amount, setAmount] = React.useState(0);
  const [receiver, setReceiver] = React.useState('');
  return (
    <>
      <Title>Send Transactions</Title>
      <Box sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  type="text"
                  id="receiver"
                  label="Receiver"
                  name="receiver"
                  onChange={(e) => setReceiver(e.target.value)}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="amount"
                  label="Amount"
                  type="number"
                  id="amount"
                  onChange={(e) => setAmount(e.target.value)}
                />
              </Grid>
            </Grid>
            <Button
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              onClick={()=>{props.sendTransaction(receiver,amount)}}
            >
              Send
            </Button>
          </Box>
    </>
  );
}