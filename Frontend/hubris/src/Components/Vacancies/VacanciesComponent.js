import React, { useState, useEffect } from 'react';
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const Vacancies = () => {
  const [data, setData] = useState([{}]);
  const [text, setText] = useState([{}]);
  useEffect(() => {
    getVacancies();
  }, []);

  const getVacancies = () => {
    axios.get('vacancies/api/v1').then((response) => {
      setData(response.data)
    })
  }

  const deleteVacancy = (vacancyId) => {
    axios.delete(`vacancies/api/v1/${vacancyId}`
    ).then(() => getVacancies());
  }

  const createVacancy = (props) => {
    axios.post('vacancies/api/v1', { title: props.text }
    ).then(() => getVacancies());
  }

  const handleMessageChange = (e) => {
    setText(e.target.value);
  };

  return (
    <div>
      <ul>
        {data.map((item, pos) => (
          <li key={pos}>
            <a>{item.title}</a>
            <button onClick={() => deleteVacancy(item.id)}>Удалить</button>
          </li>
        ))}
      </ul>
      <input type="text" onChange={handleMessageChange}></input>
      <button onClick={() => createVacancy({ text })}>Создать</button>
    </div>
  );
};


export default Vacancies