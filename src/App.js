import './App.css';
import React, { useState, useEffect } from 'react';

function App() {
  const [datas, setDatas] = useState([]);
  useEffect(() => {
    fetch('/review', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => {
        setDatas(data.datas);
      });
  }, [])

  function deleteButton(i) {
    const updatedData = [...datas.slice(0, i), ...datas.slice(i + 1)];
    setDatas(updatedData);
  }

  function saveButton() {
    fetch('/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "datas": datas }),
    })
      .then((response) => response.json())
      .then((data) => {
        setDatas(data.new_data);
        alert("Your changes are successfully saved");
      });
  }

  function changeRate(e, i) {
    const newData = [...datas];
    newData[i].rating_list = e.target.value;
    setDatas(newData);
  }

  const listingData = datas.map((data, i) => (
    <>
      <li key={i}> <b> Movie ID: </b>{data.movie_id}
        <b> Rating:</b> <input type="number" min="0" max="10" value={data.rating_list} onChange={(e) => changeRate(e, i)} />
        {data.comment_list}
        <button type="button" onClick={() => deleteButton(i)}> Delete </button> </li>
    </>
  ));
  return (
    <div class="delete">
      <h1>Your Comments:</h1>
      {listingData}
      <button type="button" onClick={() => saveButton()}> Save </button>
    </div>
  );
}

export default App;