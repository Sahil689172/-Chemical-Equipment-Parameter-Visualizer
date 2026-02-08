import React, { useMemo } from 'react';
import { useTable, useSortBy, usePagination } from 'react-table';
import './DataTable.css';

function DataTable({ data, loading }) {
  const columns = useMemo(
    () => [
      {
        Header: 'Equipment Name',
        accessor: 'equipment_name',
      },
      {
        Header: 'Type',
        accessor: 'type',
      },
      {
        Header: 'Flowrate (L/min)',
        accessor: 'flowrate',
        Cell: ({ value }) => parseFloat(value).toFixed(2),
      },
      {
        Header: 'Pressure (bar)',
        accessor: 'pressure',
        Cell: ({ value }) => parseFloat(value).toFixed(2),
      },
      {
        Header: 'Temperature (°C)',
        accessor: 'temperature',
        Cell: ({ value }) => parseFloat(value).toFixed(2),
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    prepareRow,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    state: { pageIndex, pageSize },
  } = useTable(
    {
      columns,
      data: data || [],
      initialState: { pageSize: 10 },
    },
    useSortBy,
    usePagination
  );

  const showPagination = (data || []).length > 10;

  if (loading) {
    return (
      <div className="data-table-container">
        <div className="loading-message">Loading equipment data...</div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="data-table-container">
        <div className="empty-message">No equipment data available</div>
      </div>
    );
  }

  return (
    <div className="data-table-container">
      <div className="table-header">
        <h2>Equipment Data</h2>
        {data && data.length > 0 && (
          <div className="table-info">
            Showing {pageIndex * pageSize + 1} to {Math.min((pageIndex + 1) * pageSize, data.length)} of {data.length} entries
          </div>
        )}
      </div>
      <div className="table-wrapper">
        <table {...getTableProps()} className="data-table">
          <thead>
            {headerGroups.map(headerGroup => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map(column => (
                  <th
                    {...column.getHeaderProps(column.getSortByToggleProps())}
                    className={column.isSorted ? (column.isSortedDesc ? 'sort-desc' : 'sort-asc') : ''}
                  >
                    <div className="th-content">
                      {column.render('Header')}
                      <span className="sort-indicator">
                        {column.isSorted ? (column.isSortedDesc ? ' ↓' : ' ↑') : ' ⇅'}
                      </span>
                    </div>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {page.map(row => {
              prepareRow(row);
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map(cell => (
                    <td {...cell.getCellProps()}>
                      {cell.render('Cell')}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      
      {showPagination && (
        <div className="pagination">
          <div className="pagination-info">
            <span>Rows per page:</span>
            <select
              value={pageSize}
              onChange={e => {
                setPageSize(Number(e.target.value));
              }}
              className="page-size-select"
            >
              {[10, 20, 30, 50].map(size => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </div>
          
          <div className="pagination-controls">
            <button
              onClick={() => gotoPage(0)}
              disabled={!canPreviousPage}
              className="pagination-button"
            >
              {'<<'}
            </button>
            <button
              onClick={() => previousPage()}
              disabled={!canPreviousPage}
              className="pagination-button"
            >
              {'<'}
            </button>
            <span className="page-numbers">
              Page{' '}
              <strong>
                {pageIndex + 1} of {pageOptions.length}
              </strong>
            </span>
            <button
              onClick={() => nextPage()}
              disabled={!canNextPage}
              className="pagination-button"
            >
              {'>'}
            </button>
            <button
              onClick={() => gotoPage(pageCount - 1)}
              disabled={!canNextPage}
              className="pagination-button"
            >
              {'>>'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DataTable;
