import React, { useState, useEffect } from 'react';

function QueryResult({ querySearchResult }) { // Destructure props correctly
  const [queryResult, setQueryResult] = useState('');

  useEffect(() => {
    const resultString = typeof querySearchResult === 'string' ? querySearchResult : '';
    setQueryResult(resultString);
  }, [querySearchResult]);

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
    width: '100%',
    height: '500px',
    padding: '10px',
    borderRadius: '15px', 
    marginTop: 10,
    border: '1px solid #ccc', 
    outline: 'none', 
    fontSize: '16px',
    fontFamily: 'Arial',
    backgroundColor: '#f9f9f9', 
    resize: 'none', 
    overflowY: 'auto', 
    boxSizing: 'border-box', 
  },
};

export default QueryResult;