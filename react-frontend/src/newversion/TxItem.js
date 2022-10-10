import './App.css';

function TxItem(props) {
  return (
    <tr className="tx-item">
      <td>
        <p><a></a></p>
        <small></small>
      </td>
      <td>
        <p>From <a>xxx</a></p>
        <p>To <a>xxx</a></p>
      </td>
      <td>
        <p>col3</p>
      </td>
    </tr>
  );
}

export default TxItem;