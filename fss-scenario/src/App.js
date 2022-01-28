function App() {
  
  fetch('./test.json', {
    headers: {
      'Accept': 'application/json'
    }
  })
    .then(res => res.json())
    .then(data => console.log(data));

  return (
    <div>Hello</div>
  );
}

export default App;
