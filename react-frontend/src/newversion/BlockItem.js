import './App.css';

function BlockItem(props) {
  return (
    <tr className="block-item">
      <td>
        <p><a>{props.block.index}</a></p>
        <small>{props.block.timestamp} secs ago</small>
      </td>
      <td>
        <p>Fee Recipient <a>xx</a></p>
        <p><a>txns</a> <small>in x secs</small></p>
      </td>
      <td>
        <p>col3</p>
      </td>
    </tr>
  );
}

export default BlockItem;