new Vue({
  delimiters: ['${', '}$'],
  el: '#app',
  data: {
    message: 'This is where Vue.js will do its magic!',
    ifflists_current: [],
    ifflists_completed: [],
    loading: false,
    currentIfflist: {},
    newIfflist: { 'get-to-do': null, 'todo_set': null },
  },
  http: {
    root: 'http://localhost:8000',
    headers: {
      Authorization: 'Basic YXBpOnBhc3N3b3Jk'
    }
  },
 mounted: function() {
    this.getIfflists();
  },
 methods: {
   getIfflists: function () {
     this.loading = true;
     this.$http.get('api/')
         .then((response) => {
           for (let i = 0; i < response.body.length; i++) {
             if (response.body[i].is_completed === false) {
               this.ifflists_current.push(response.body[i]);
             } else {
               this.ifflists_completed.push(response.body[i]);
             }
           }
           console.log(response.body);
           this.loading = false;
         })
         .catch((err) => {
           this.loading = false;
           console.log(err);
         })
   },
   getIfflist: function (id) {
     this.loading = true;
     this.$http.get('/api/${id}$/')
         .then((response) => {
           this.currentIfflist = response.data;
           this.loading = false;
         })
         .catch((err) => {
           this.loading = false;
           console.log(err);
         })
   },
   addIfflist: function () {
     this.loading = true;
     this.$http.post('/api/', this.newIfflist)
         .then((response) => {
           this.loading = false;
           this.getIfflists();
         })
         .catch((err) => {
           this.loading = false;
           console.log(err);
         })
   },
   updateIfflist: function () {
     this.loading = true;
     this.$http.put('/api/${this.currentIfflist.ifflist_id}$/', this.currentIfflist)
         .then((response) => {
           this.loading = false;
           this.currentIfflist = response.data;
           this.getIfflists();
         })
         .catch((err) => {
           this.loading = false;
           console.log(err);
         })
   },
   deleteIfflist: function (id) {
     this.loading = true;
     this.$http.delete('/api/${id}$/')
         .then((response) => {
           this.loading = false;
           this.getIfflists();
         })
         .catch((err) => {
           this.loading = false;
           console.log(err);
         })
   },
 },

});

