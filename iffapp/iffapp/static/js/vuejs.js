new Vue({
  delimiters: ['${', '}$'],
  el: '#app',
  data: {
    message: 'This is where Vue.js will do its magic!'
  }
})

new Vue({

  http: {
    root: 'http://localhost:8000',
    headers: {
      Authorization: 'Basic YXBpOnBhc3N3b3Jk'
    }
  }

})
