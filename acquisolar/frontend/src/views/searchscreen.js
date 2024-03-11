import React, { useCallback, useState, useEffect } from 'react';
import Header from './viewcomponents/header';
import { useNavigate, useLocation } from 'react-router-dom';
import QueryResult from './viewcomponents/queryresult';
import { Document, Page, pdfjs } from 'react-pdf';
import backButton from './../icons/backbutton.png';

// Set the workerSrc for pdfjs
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const Search = () => {
    const navigate = useNavigate()
    const location = useLocation();
    const [filename, setFilename] = useState("");
    const [searchText, setSearchText] = useState("");
    const [searchResult, setSearchResult] = useState("");
    const [occurrences, setOccurrences] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [searchQueryResult, setSearchQueryResult] = useState(null);

    useEffect(() => {
        if (location.state && location.state.filename) {
          setFilename(location.state.filename)
        }
    }, [location]);

    useEffect(() => {
        console.log(searchQueryResult);
    }, [searchQueryResult]); 

      const handleSearch = async () => {
        
        try {
            const response = await fetch('http://localhost:3001/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: searchText, file: filename }),
            });
            const textResponse = await response.text(); // Assuming the response is a stream of text
            console.log(textResponse)
            setSearchQueryResult(textResponse);
        } catch (error) {
            console.error('Failed to fetch search results:', error);
        }

        console.log(searchQueryResult)


        const url = `http://localhost:3001/get-pdf/${filename}`;
        let pdf = await pdfjs.getDocument(url).promise;
        let foundPages = [];
    
        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const text = textContent.items.map(item => item.str).join(" ");
            if (text.match(new RegExp(searchText, "gi"))) {
                foundPages.push(i);
            }
        }
    
        setOccurrences(foundPages);
        setCurrentPage(foundPages[0] || 1); // Set to first found page or back to 1 if no occurrence
        setSearchResult(`Found "${searchText}" ${foundPages.length} times.`);


        console.log(searchQueryResult)
    };

    const goToNextOccurrence = () => {
        const currentIndex = occurrences.indexOf(currentPage);
        const nextIndex = (currentIndex + 1) % occurrences.length; // Loop back to the first occurrence
        setCurrentPage(occurrences[nextIndex]);
        console.log(currentPage + ' page')
    };
    
    const goToPrevOccurrence = () => {
        const currentIndex = occurrences.indexOf(currentPage);
        const prevIndex = (currentIndex - 1 + occurrences.length) % occurrences.length; // Loop to the last occurrence
        setCurrentPage(occurrences[prevIndex]);
        console.log(currentPage + ' page')
    };
    const handleBack = () => {
        navigate('/folders');
      }

return (
    <div style={styles.container}>
        <Header/>
        <img src={backButton} alt="Backbutton" style={styles.imageIcon} onClick={handleBack}/>
        <div style={styles.content}>
            <div style={styles.searchContainer}>
                <div style={styles.searchBar}>
                    <input
                        type="text"
                        placeholder="Search..."
                        style={styles.searchInput}
                        value={searchText}
                        onChange={(e) => setSearchText(e.target.value)}
                    />
                    <button style={styles.searchButton} onClick={handleSearch}>Search</button>
                </div>
                <QueryResult querySearchResult={searchQueryResult} />
            </div>
            <div style={styles.pdfContainer}>
                {/* Render the PDF Document */}
                {occurrences.length > 0 && (
                    <div>
                        {occurrences.length} matches found
                        <button style={styles.pageButton} onClick={goToPrevOccurrence}>Previous</button>
                        <button style={styles.pageButton} onClick={goToNextOccurrence}>Next</button>
                    </div>
                )}
                <iframe
                    key={currentPage}
                    src={`http://localhost:3001/get-pdf/${filename}#page=${currentPage}`}
                    width="100%"
                    height="600px"
                    style={{ border: 'none' }}
                >
                    This browser does not support PDFs. Please download the PDF to view it: <a href={`http://localhost:3001/get-pdf/${filename}`}>Download PDF</a>.
                </iframe>
            </div>
        </div>
    </div>
);
};

const styles = {
    container: {
        fontFamily: 'Arial, sans-serif',
        height: '100vh',
        width: '100%',
        backgroundColor: '#FFFFFF',
        display: 'flex',
        flexDirection: 'column',
    },
    content: {
        display: 'flex',
        flexDirection: 'row',
    },
    pdfContainer: {
        display: 'flex',
        width: '65%',
        justifyContent: 'center',
        backgroundColor: 'white',
        marginTop: '2%',
        margin: 15,
        flexDirection: 'column',
    },
    searchContainer: {
        display: 'flex',
        width: '35%',
        backgroundColor: 'white',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        marginLeft: "2%",
        marginTop: '2%',
    },
    searchText: {
        color: 'grey',
    },
    searchBar: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'flex-start',
        alignItems: 'center',
    },
    searchButton: {
        padding: '10px 20px',
        fontSize: '16px',
        backgroundColor: '#156CF7',
        color: 'white',
        border: 'none',
        borderRadius: '15px',
        cursor: 'pointer',
        outline: 'none',
        margin: '4px'
      },
    searchInput: {
        height: '40px',
        fontSize: '18px',
        padding: '0 15px',
        backgroundColor: '#F3F3F3',
        border: 0,
        borderRadius: '15px',
        marginRight: '10px',
        outline: 'none',
    },
    pageButton: {
        padding: '5px 10px',
        fontSize: '14px',
        backgroundColor: '#156CF7',
        color: 'white',
        border: 'none',
        borderRadius: '15px',
        cursor: 'pointer',
        outline: 'none',
        margin: '4px',
    },
    imageIcon: {
        width: '40px', 
        height: '40px', 
        objectFit: 'contain', 
      },

};

export default Search;