import React, { useState } from 'react';

function QueryResult() {
  const [queryResult, setQueryResult] = useState('');

  return (
    <div>
      <textarea
        value={queryResult}
        readOnly
        placeholder="Enter a prompt in the searchbar."
        style={styles.textArea}
      />
    </div>
  );
}

const styles = {
  textArea: {
    width: '300px', // Width of the square, adjust as needed
    height: '300px', // Height to make it square-shaped
    padding: '10px',
    margin: '10px',
    borderRadius: '15px', // Rounded edges
    border: '1px solid #ccc', // Border color
    outline: 'none', // Removes the default focus outline
    fontSize: '16px', // Text size
    backgroundColor: '#f9f9f9', // Light grey background to indicate non-editability
    resize: 'none', // Prevents resizing
    overflowY: 'auto', // Adds vertical scroll if content overflows
    boxSizing: 'border-box', // Includes padding and border in the element's total width and height
  },
};

export default QueryResult;