import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';
import { IconButton,Collapse,Box,Typography } from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import RefreshIcon from '@mui/icons-material/Refresh';

function Row(props){
    const {tx} = props;
    const [open, setOpen] = React.useState(false);
    
    const [InOpen, setInOpen] = React.useState(false);
    const [OutOpen, setOutOpen] = React.useState(false);
    return (
    <>
            <TableRow>
              <TableCell>
                <IconButton
                  aria-label="expand row"
                  size="small"
                  onClick={() => setOpen(!open)}
                >
                  {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                </IconButton>
              </TableCell>
              <TableCell>{tx.id}</TableCell>
            </TableRow>
            <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
            <Collapse in={open} timeout="auto" unmountOnExit>
                <Box sx={{margin:1}} display='flex' flexDirection='column'>
                    <Box>
                        <Typography>TxIns
                            <IconButton 
                                onClick={() => setInOpen(!InOpen)}
                            >
                                {InOpen ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                            </IconButton>
                        </Typography>
                        <Collapse in={InOpen} timeout="auto" unmountOnExit>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>TxOutId</TableCell>
                                    <TableCell>TxOutIndex</TableCell>
                                    <TableCell>Signature</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {tx.txIns.map((txIn,i) => (
                                    <TableRow>
                                    <TableCell component="th" scope="row" width='30%'>
                                        <Box sx={{maxWidth:'100px', wordBreak:'break-word'}} noWrap>
                                            {txIn.txOutId}
                                        </Box>
                                    </TableCell>
                                    <TableCell component="th" scope="row" width='30%'>
                                        <Box sx={{maxWidth:'100px', wordBreak:'break-word'}} noWrap>
                                            {txIn.txOutIndex}
                                        </Box>
                                    </TableCell>
                                    <TableCell component="th" scope="row" width='30%'>
                                        <Box sx={{maxWidth:'100px', wordBreak:'break-word'}} noWrap>
                                            {txIn.signature}
                                        </Box>
                                    </TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                        </Collapse>
                    </Box>
                    <Box>
                        <Typography>TxOuts
                            <IconButton 
                                onClick={() => setOutOpen(!OutOpen)}
                            >
                                {OutOpen ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                            </IconButton>
                        </Typography>
                        <Collapse in={OutOpen} timeout="auto" unmountOnExit>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Address</TableCell>
                                    <TableCell>Amount</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {tx.txOuts.map((txOut,i) => (
                                    <TableRow>
                                    <TableCell component="th" scope="row" width='30%'>
                                        <Box sx={{maxWidth:'100px', wordBreak:'break-word'}} noWrap>
                                            {txOut.address}
                                        </Box>
                                    </TableCell>
                                    <TableCell component="th" scope="row" width='30%'>
                                        <Box sx={{maxWidth:'100px', wordBreak:'break-word'}} noWrap>
                                            {txOut.amount}
                                        </Box>
                                    </TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                        </Collapse>
                    </Box>
                </Box>
            </Collapse>
        </TableCell>
      </TableRow>
      </>
    )
}

export default function Transactions(props) {
  
  return (
    <React.Fragment>
      <Title>Transactions
        <IconButton onClick={()=>{props.getTxs()}}><RefreshIcon/></IconButton>
      </Title>
      <Table size='small'>
        <TableHead >
          <TableRow>
            <TableCell size='small'></TableCell>
            <TableCell size='small'>Id</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.txs.map((tx,i) => (
            <Row key={i} tx={tx}/>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}