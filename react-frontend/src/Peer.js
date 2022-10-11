import * as React from 'react';
import Title from './Title';
import { Divider, Paper,IconButton,InputBase,List, Collapse } from '@mui/material';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import AddIcon from '@mui/icons-material/Add';
import RefreshIcon from '@mui/icons-material/Refresh';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

export default function Peer(props) {
  const [open, setOpen] = React.useState(true);
  const [newPeer, setNewPeer] = React.useState('');
  const handleClick = () => {
    setOpen(!open);
  };

  return (
    <React.Fragment>
      <Title>Peer</Title>
        <Paper
          component="form"
          sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', margin:'auto',marginTop:'0',marginBottom:'10px',width:'400px'}}
        >
          <InputBase
            sx={{ ml: 1, flex: 1 }}
            placeholder="Add peer"
            inputProps={{ 'aria-label': 'search google maps' }}
            onChange={(e) => setNewPeer(e.target.value)}
          />
          <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
          <IconButton onClick={()=>{props.addPeerNode(newPeer)}} color="primary" sx={{ p: '10px' }} aria-label="directions">
            <AddIcon />
          </IconButton>
          <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
          <IconButton onClick={()=>{props.getPeerNodes()}} color="primary" sx={{ p: '10px' }} aria-label="directions">
            <RefreshIcon />
          </IconButton>
          <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
          <IconButton  onClick={handleClick}>
          {open? <ExpandLess /> : <ExpandMore />}
        </IconButton>
        </Paper>
        <Divider varient="middle"/>
        <Collapse in={open} timeout="auto" unmountOnExit sx={{overflow:'auto'}}>
          <List component="div" disablePadding>
            {
              Array.isArray(props.peers) && props.peers.length > 0 ? (props.peers.map((peer,i) => (
                <ListItem key={i}>
                  <ListItemText>{peer}</ListItemText>
                </ListItem>
              ))) : ''
            }
          </List>
        </Collapse>
    </React.Fragment>
  );
}