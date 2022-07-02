import './App.css';
import { useState, useEffect } from "react";
import { useTable } from "react-table";
import axios from 'axios';

// Initialize list of columns
const columns = [
  {
    Header: "Number",
    accessor: "id",
  },
  {
    Header: "Code",
    accessor: "num",
  },
  {
    Header: "Price, $",
    accessor: "priced",
  },
  {
    Header: "Price, ₽",
    accessor: "pricer",
  },
  {
    Header: "Date",
    accessor: "date",
  },
];

// Headers for axios request
const headers = {
  'Content-Type': 'application/json',
  "Access-Control-Allow-Origin": "*"
}

function App() {
  // Get data from backend
  const [data, setData] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      await axios.get("http://localhost:5000/entries", {
        headers: headers
      })
          .then(res => {
            const entries = res.data;
            setData(entries)
      })
    };

    fetchData();
  }, []);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({
    columns,
    data,
  });
  return (
    <div className="App">
      <header className="App-header">
        <img src="http://localhost:5000/entries/chart" className="chart"/>
        <table {...getTableProps()}>
          <thead>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <th {...column.getHeaderProps()}>{column.render("Header")}</th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row, i) => {
              prepareRow(row);
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map((cell) => {
                    return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>;
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </header>
    </div>
  );
}

export default App;
