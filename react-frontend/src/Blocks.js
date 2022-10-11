import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';
import { IconButton,Collapse,Box,Typography, Button } from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import RefreshIcon from '@mui/icons-material/Refresh';

function Row(props){
  const {block} = props;
  const [open, setOpen] = React.useState(false);
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
              <TableCell>{block.index}</TableCell>
              <TableCell>{block.timestamp}</TableCell>
              <TableCell>
                <Box sx={{wordBreak:'break-word'}}>
                  {block.previousHash}
                </Box>
              </TableCell>
              <TableCell sx={{maxWidth:'100px'}}>{block.difficulty}</TableCell>
              <TableCell sx={{maxWidth:'100px'}}>{block.nonce}</TableCell>
            </TableRow>
            <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div">
                Transactions
              </Typography>
              <Table size="small" aria-label="purchases">
                <TableHead>
                  <TableRow>
                    <TableCell>Id</TableCell>
                    <TableCell>TxIns</TableCell>
                    <TableCell>TxOuts</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {block.data.map((tx,j) => (
                    <TableRow>
                      <TableCell component="th" scope="row" width='30%'>
                        <Box sx={{maxWidth:'200px', wordBreak:'break-word'}} noWrap>
                          {tx.id}
                        </Box>
                      </TableCell>
                      <TableCell noWrap>
                        <Box sx={{maxWidth:'300px', wordBreak:'break-word'}} noWrap>
                          <p>{JSON.stringify(tx.txIns)}</p>
                        </Box>
                      </TableCell>
                      <TableCell noWrap>
                        <Box sx={{maxWidth:'300px', wordBreak:'break-word'}} noWrap><p>{JSON.stringify(tx.txOuts)}</p></Box></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
      </>
  )
}

export default function Blocks(props) {
  const [open, setOpen] = React.useState(false);
  
  return (
    <React.Fragment>
      <Title>Blocks
        <IconButton onClick={()=>{props.getBlocks()}}><RefreshIcon/></IconButton>
        <Button onClick={()=>{props.syncPeers()}}>Sync Block with Peers</Button>
      </Title>
      <Table size='small'>
        <TableHead >
          <TableRow>
            <TableCell size='small'></TableCell>
            <TableCell size='small'>Index</TableCell>
            <TableCell size='small'>TimeStamp</TableCell>
            <TableCell size='small'  noWrap>PreviousHash</TableCell>
            <TableCell size='small'>Difficulty</TableCell>
            <TableCell size='small'>nonce</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.blocks.map((block,i) => (
            <Row key={i} block={block} />
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}